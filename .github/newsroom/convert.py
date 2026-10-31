#!/usr/bin/env python3
"""
convert.py — 把 Apps Script 送來的新聞稿 Email 轉成 NewsRoom 文章

輸入（由 Apps Script 提交到 newsroom/<message_id> 分支）:
    newsroom-inbox/<message_id>/email.eml   原始信件
    newsroom-inbox/<message_id>/meta.json   來源資訊（source_type 等）

輸出:
    _newsroom/YYYY-MM-DD-<slug>.md
    assets/img/newsroom/<slug>-NN.jpg
    newsroom-inbox/<message_id>/result.json   處理結果（status: created / skipped / error）
    newsroom-inbox/<message_id>/pr_body.md    PR 說明（status 為 created 時）

用法:
    python .github/newsroom/convert.py newsroom-inbox
    python .github/newsroom/convert.py newsroom-inbox --llm-output sample.json   # 測試用，不呼叫 API
"""

import argparse
import base64
import email
import io
import json
import re
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from email import policy
from email.utils import parsedate_to_datetime
from pathlib import Path

import anthropic
import html2text
from bs4 import BeautifulSoup
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[2]
PROMPT_PATH = Path(__file__).with_name("prompt.md")
POSTS_DIR = ROOT / "_newsroom"
IMG_DIR = ROOT / "assets" / "img" / "newsroom"
IMG_URL = "/assets/img/newsroom"

TAIPEI = timezone(timedelta(hours=8))
MODEL = "claude-opus-5-5"
MAX_IMAGE_EDGE = 1920
MIN_IMAGE_EDGE = 300  # smaller images are logos, icons or tracking pixels
THUMB_EDGE = 768
MAX_THUMBS = 20
MAX_LINKS = 60
CLOUD_HOSTS = ("drive.google.com", "docs.google.com", "wetransfer.com", "we.tl", "dropbox.com", "onedrive.live.com", "1drv.ms")
TRACKING_PARAMS = re.compile(r"^(utm_|fbclid$|gclid$|mc_cid$|mc_eid$|_hsenc$|_hsmi$)")

SCHEMA = {
    "type": "object",
    "properties": {
        "is_press_release": {"type": "boolean"},
        "skip_reason": {"type": "string"},
        "title": {"type": "string"},
        "lead": {"type": "string"},
        "slug": {"type": "string"},
        "description": {"type": "string"},
        "brand": {"type": "string"},
        "source_name": {"type": "string"},
        "tags": {"type": "array", "items": {"type": "string"}},
        "publish_at": {"type": "string"},
        "body_markdown": {"type": "string"},
        "cover_image": {"type": "integer"},
        "images": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "n": {"type": "integer"},
                    "placement": {"type": "string", "enum": ["inline", "gallery", "drop"]},
                    "caption": {"type": "string"},
                },
                "required": ["n", "placement", "caption"],
                "additionalProperties": False,
            },
        },
        "warnings": {"type": "array", "items": {"type": "string"}},
    },
    "required": [
        "is_press_release", "skip_reason", "title", "lead", "slug", "description", "brand",
        "source_name", "tags", "publish_at", "body_markdown", "cover_image", "images", "warnings",
    ],
    "additionalProperties": False,
}


# ---------------------------------------------------------------- email parsing

def decode_filename(part):
    name = part.get_filename() or ""
    return name.strip().replace("\n", " ").replace("\r", "")


def load_image(data):
    """Open image bytes, or return None for anything Pillow can't read."""
    try:
        img = Image.open(io.BytesIO(data))
        img.load()
        return ImageOps.exif_transpose(img)
    except Exception:
        return None


def parse_email(path):
    msg = email.message_from_bytes(path.read_bytes(), policy=policy.default)
    html_body = text_body = None
    images, docx = [], []

    for part in msg.walk():
        if part.is_multipart():
            continue
        ctype = part.get_content_type()
        filename = decode_filename(part)
        disposition = part.get_content_disposition()

        if ctype == "text/html" and disposition != "attachment" and html_body is None:
            html_body = part.get_content()
        elif ctype == "text/plain" and disposition != "attachment" and text_body is None:
            text_body = part.get_content()
        elif ctype.startswith("image/") or re.search(r"\.(jpe?g|png|gif|webp|heic)$", filename, re.I):
            data = part.get_payload(decode=True) or b""
            img = load_image(data)
            if img is None:
                continue
            images.append({
                "filename": filename or f"image-{len(images) + 1}",
                "content_id": (part.get("Content-ID") or "").strip("<> "),
                "data": data,
                "image": img,
            })
        elif filename.lower().endswith(".docx"):
            docx.append(part.get_payload(decode=True) or b"")

    try:
        date = parsedate_to_datetime(msg["Date"]).astimezone(TAIPEI)
    except Exception:
        date = datetime.now(TAIPEI)

    return {
        "subject": str(msg["Subject"] or ""),
        "from": str(msg["From"] or ""),
        "date": date,
        "html": html_body,
        "text": text_body,
        "images": images,
        "docx": docx,
    }


def docx_text(data):
    try:
        import docx  # python-docx
        doc = docx.Document(io.BytesIO(data))
        return "\n\n".join(p.text for p in doc.paragraphs if p.text.strip())
    except Exception:
        return ""


def fetch_remote_image(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 NewsRoomBot"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read(20 * 1024 * 1024)
    except Exception:
        return None


def html_to_text(html, images):
    """Convert the HTML body to Markdown-ish text, keeping [[IMAGE n]] where images sat."""
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["style", "script", "head", "title"]):
        tag.decompose()

    by_cid = {img["content_id"]: i for i, img in enumerate(images) if img["content_id"]}
    for tag in soup.find_all("img"):
        src = (tag.get("src") or "").strip()
        index = None
        if src.lower().startswith("cid:"):
            index = by_cid.get(src[4:].strip("<> "))
        elif src.lower().startswith(("http://", "https://")):
            data = fetch_remote_image(src)
            img = load_image(data) if data else None
            if img is not None and max(img.size) >= MIN_IMAGE_EDGE:
                name = Path(urllib.parse.urlparse(src).path).name or f"remote-{len(images) + 1}"
                images.append({"filename": name, "content_id": "", "data": data, "image": img})
                index = len(images) - 1
        tag.replace_with(f"\n\n[[IMAGE {index + 1}]]\n\n" if index is not None else "")

    converter = html2text.HTML2Text()
    converter.body_width = 0
    converter.ignore_images = True
    converter.unicode_snob = True
    converter.protect_links = True
    return converter.handle(str(soup))


# ---------------------------------------------------------------- links

def strip_tracking(url):
    parts = urllib.parse.urlsplit(url)
    query = [(k, v) for k, v in urllib.parse.parse_qsl(parts.query, keep_blank_values=True) if not TRACKING_PARAMS.match(k)]
    return urllib.parse.urlunsplit(parts._replace(query=urllib.parse.urlencode(query)))


def resolve_url(url):
    """Follow redirects (tracking short links) and return the final URL without tracking parameters."""
    try:
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "Mozilla/5.0 NewsRoomBot"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            final = resp.geturl()
    except Exception:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 NewsRoomBot"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                final = resp.geturl()
        except Exception:
            final = url
    return strip_tracking(final)


def resolve_links(text):
    urls = list(dict.fromkeys(re.findall(r"https?://[^\s<>()\[\]\"'，。、）]+", text)))[:MAX_LINKS]
    mapping = {u: resolve_url(u) for u in urls}
    for old, new in sorted(mapping.items(), key=lambda kv: -len(kv[0])):
        if old != new:
            text = text.replace(old, new)
    cloud = [u for u in mapping.values() if (urllib.parse.urlsplit(u).hostname or "").endswith(CLOUD_HOSTS)]
    return text, list(dict.fromkeys(cloud))


# ---------------------------------------------------------------- images

def thumbnail_b64(img):
    thumb = img.convert("RGB")
    thumb.thumbnail((THUMB_EDGE, THUMB_EDGE))
    buf = io.BytesIO()
    thumb.save(buf, "JPEG", quality=70)
    return base64.b64encode(buf.getvalue()).decode()


def save_image(img, slug, number):
    """Resize to MAX_IMAGE_EDGE and save; PNG only when the image really uses transparency."""
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    has_alpha = img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info)
    if has_alpha and img.convert("RGBA").getextrema()[3][0] < 255:
        out = img.convert("RGBA")
        out.thumbnail((MAX_IMAGE_EDGE, MAX_IMAGE_EDGE))
        name = f"{slug}-{number:02d}.png"
        out.save(IMG_DIR / name, "PNG", optimize=True)
    else:
        out = img.convert("RGB")
        out.thumbnail((MAX_IMAGE_EDGE, MAX_IMAGE_EDGE))
        name = f"{slug}-{number:02d}.jpg"
        out.save(IMG_DIR / name, "JPEG", quality=82, progressive=True, optimize=True)
    return f"{IMG_URL}/{name}"


# ---------------------------------------------------------------- Claude

def build_request(mail, body, images):
    listing = "\n".join(
        f"- 圖片 {i + 1}：檔名「{img['filename']}」，{img['image'].size[0]}x{img['image'].size[1]}"
        for i, img in enumerate(images)
    ) or "（這封信沒有圖片）"
    text = (
        f"<email>\n主旨：{mail['subject']}\n寄件者：{mail['from']}\n"
        f"日期：{mail['date'].isoformat()}\n\n{body}\n</email>\n\n"
        f"信件中的圖片：\n{listing}\n\n以下依序附上圖片縮圖。"
    )
    content = [{"type": "text", "text": text}]
    for i, img in enumerate(images[:MAX_THUMBS]):
        content.append({"type": "text", "text": f"圖片 {i + 1}："})
        content.append({"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": thumbnail_b64(img["image"])}})
    return content


def call_claude(content):
    client = anthropic.Anthropic()
    with client.beta.messages.stream(
        model=MODEL,
        max_tokens=64000,
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
        output_config={"effort": "medium", "format": {"type": "json_schema", "schema": SCHEMA}},
        system=PROMPT_PATH.read_text(encoding="utf-8"),
        messages=[{"role": "user", "content": content}],
    ) as stream:
        message = stream.get_final_message()

    if message.stop_reason == "refusal":
        raise RuntimeError("Claude 拒絕處理這封信（refusal）")
    if message.stop_reason == "max_tokens":
        raise RuntimeError("輸出超過長度上限，新聞稿可能太長")
    text = next(block.text for block in message.content if block.type == "text")
    return json.loads(text)


# ---------------------------------------------------------------- output

def clean_slug(slug, fallback):
    slug = re.sub(r"[^a-z0-9-]+", "-", (slug or "").lower()).strip("-")
    slug = re.sub(r"-{2,}", "-", slug)[:60].strip("-")
    return slug or fallback


def parse_publish_at(value, fallback):
    if not value:
        return fallback
    try:
        dt = datetime.fromisoformat(value)
        return (dt if dt.tzinfo else dt.replace(tzinfo=TAIPEI)).astimezone(TAIPEI)
    except ValueError:
        return fallback


def unique_path(date, slug):
    path = POSTS_DIR / f"{date:%Y-%m-%d}-{slug}.md"
    n = 2
    while path.exists():
        path = POSTS_DIR / f"{date:%Y-%m-%d}-{slug}-{n}.md"
        n += 1
    return path


def figure(url, caption):
    alt = caption.replace("[", "(").replace("]", ")")
    return f"![{alt}]({url})\n_{caption}_" if caption else f"![{alt}]({url})"


def render(result, mail, images, message_id):
    warnings = list(result.get("warnings") or [])
    slug = clean_slug(result["slug"], f"press-release-{message_id[-8:]}")
    date = parse_publish_at(result.get("publish_at"), mail["date"])
    path = unique_path(date, slug)
    slug = path.stem[11:]  # keep image names in step with a de-duplicated file name

    plan = {item["n"]: item for item in result.get("images") or [] if 1 <= item["n"] <= len(images)}
    body = result["body_markdown"].strip()
    saved, number = {}, 0

    def save(n):
        nonlocal number
        if n not in saved:
            number += 1
            saved[n] = save_image(images[n - 1]["image"], slug, number)
        return saved[n]

    def replace_marker(match):
        n = int(match.group(1))
        item = plan.get(n)
        if not (1 <= n <= len(images)) or (item and item["placement"] == "drop"):
            return ""
        caption = item["caption"] if item else Path(images[n - 1]["filename"]).stem
        return figure(save(n), caption)

    body = re.sub(r"\{\{IMAGE:(\d+)\}\}", replace_marker, body)
    body = re.sub(r"\[\[IMAGE (\d+)\]\]", "", body)
    body = re.sub(r"\n{3,}", "\n\n", body)

    gallery = [n for n, item in sorted(plan.items()) if item["placement"] != "drop" and n not in saved]
    if gallery:
        # keep footnote definitions at the very end, after the gallery
        notes = re.findall(r"^\[\^[^\]]+\]:.*$", body, flags=re.M)
        body = re.sub(r"^\[\^[^\]]+\]:.*\n?", "", body, flags=re.M).rstrip()
        body += "\n\n## 新聞圖片\n\n" + "\n\n".join(figure(save(n), plan[n]["caption"]) for n in gallery)
        if notes:
            body += "\n\n" + "\n".join(notes)

    cover_n = result.get("cover_image", -1)
    cover = saved.get(cover_n) or (save(cover_n) if 1 <= cover_n <= len(images) and plan.get(cover_n, {}).get("placement") != "drop" else None)
    if not cover and saved:
        cover = saved[min(saved)]

    front = {
        "title": result["title"],
        "date": date.strftime("%Y-%m-%d %H:%M:%S %z"),
        "description": result["description"],
        "brand": result["brand"],
        "source": result["source_name"] or result["brand"],
        "tags": result["tags"],
    }
    if cover:
        front["cover"] = cover
    # JSON strings are valid YAML scalars, which keeps titles with colons or quotes safe
    header = "\n".join(["---"] + [f"{k}: {json.dumps(v, ensure_ascii=False)}" for k, v in front.items()] + ["---"]) + "\n\n"
    lead = (result.get("lead") or "").strip()
    if lead:
        header += f"**{lead}**\n\n"
    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    path.write_text(header + body + "\n", encoding="utf-8")

    if date > datetime.now(TAIPEI):
        warnings.append(f"禁播時間：{date:%Y-%m-%d %H:%M}，Merge 後會在這個時間之後自動出現")
    return path, slug, date, warnings, len(saved)


def redact(text):
    """The PR is public: strip email addresses and phone numbers that may come from the email."""
    text = re.sub(r"[\w.+-]+@[\w-]+(\.[\w-]+)+", "[email]", text)
    phone = (
        r"\+?886[\s-]?\(?\d{1,2}\)?[\s-]?\d{3,4}[\s-]?\d{3,4}(#\d+)?"  # +886 2 2894 3447
        r"|\(0\d{1,2}\)\s?\d{3,4}-?\d{4}(#\d+)?"  # (02) 2894-3447#27156
        r"|(?<!\d)09\d{2}-?\d{3}-?\d{3}(?!\d)"  # 0965-517-156
        r"|(?<!\d)0\d{1,2}-\d{7,8}(?!\d)"  # 02-28943447
    )
    return re.sub(phone, "[phone]", text)


def write_pr_body(inbox, mail, meta, result, path, date, warnings, image_count):
    # no sender address here: the repository and its pull requests are public
    lines = [f"自動轉換自 Email 新聞稿。", "", "| 項目 | 內容 |", "|---|---|"]
    lines += [
        f"| 主旨 | {redact(mail['subject'])} |",
        f"| 來源 | {meta.get('source_type_label', meta.get('source_type', ''))} |",
        f"| 文章 | `{path.relative_to(ROOT)}` |",
        f"| 發佈時間 | {date:%Y-%m-%d %H:%M} |",
        f"| 圖片 | {image_count} 張 |",
    ]
    if meta.get("source_type") == "detected":
        warnings.insert(0, "**未知寄件者**：這封信不在白名單標籤裡，是自動偵測到的，請確認寄件者可信")
    if warnings:
        lines += ["", "### 需要確認", ""] + [f"- {redact(w)}" for w in warnings]
    lines += ["", "預覽網址會在建置完成後留言在下方。確認沒問題後按 **Merge** 即可發佈。"]
    (inbox / "pr_body.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def process(inbox, llm_output=None):
    meta = json.loads((inbox / "meta.json").read_text(encoding="utf-8")) if (inbox / "meta.json").exists() else {}
    message_id = meta.get("message_id") or inbox.name
    mail = parse_email(inbox / "email.eml")

    # drop logos and icons first, so [[IMAGE n]] markers and the image list share one numbering
    images = [img for img in mail["images"] if max(img["image"].size) >= MIN_IMAGE_EDGE]
    body = html_to_text(mail["html"], images) if mail["html"] else (mail["text"] or "")
    if len(body.strip()) < 200 and mail["docx"]:
        body = docx_text(mail["docx"][0]) or body
    body, cloud_links = resolve_links(body)

    if llm_output:
        result = json.loads(Path(llm_output).read_text(encoding="utf-8"))
    else:
        result = call_claude(build_request(mail, body, images))

    if not result["is_press_release"]:
        return {"status": "skipped", "reason": result.get("skip_reason", ""), "subject": mail["subject"]}

    path, slug, date, warnings, image_count = render(result, mail, images, message_id)
    if cloud_links:
        warnings.append("信中有雲端下載連結，可能還有圖片沒附在信裡，請手動確認：" + "、".join(cloud_links[:5]))
    if len(images) > MAX_THUMBS:
        warnings.append(f"圖片超過 {MAX_THUMBS} 張，後面的圖片沒有附縮圖給 AI 判斷位置")
    write_pr_body(inbox, mail, meta, result, path, date, warnings, image_count)
    return {
        "status": "created",
        "title": result["title"],
        "slug": slug,
        "post": str(path.relative_to(ROOT)),
        "brand": result["brand"],
        "warnings": warnings,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("inbox_root", type=Path, help="newsroom-inbox 資料夾")
    parser.add_argument("--llm-output", help="測試用：直接使用這個 JSON 檔當作 Claude 的輸出")
    parser.add_argument("--github-output", help="把結果寫入 GitHub Actions 的 output 檔")
    args = parser.parse_args()

    inboxes = [p for p in sorted(args.inbox_root.iterdir()) if (p / "email.eml").exists() and not (p / "result.json").exists()]
    if len(inboxes) != 1:
        print(f"預期剛好一封待處理的信，實際找到 {len(inboxes)} 封", file=sys.stderr)
        sys.exit(1)
    inbox = inboxes[0]

    try:
        result = process(inbox, args.llm_output)
    except Exception as exc:  # report every failure back to Gmail as an error label
        result = {"status": "error", "error": f"{type(exc).__name__}: {exc}"}

    (inbox / "result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))

    if args.github_output:
        with open(args.github_output, "a", encoding="utf-8") as out:
            out.write(f"status={result['status']}\n")
            out.write(f"inbox={inbox.relative_to(ROOT) if inbox.is_absolute() else inbox}\n")
            if result["status"] == "created":
                out.write(f"title={result['title']}\n")
                out.write(f"slug={result['slug']}\n")


if __name__ == "__main__":
    main()
