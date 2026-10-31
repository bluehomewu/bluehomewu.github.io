# NewsRoom Gmail 自動化（Google Apps Script）

把廠商新聞稿 Email 送到 GitHub，由 `.github/workflows/newsroom.yml` 轉成 `_newsroom/` 的文章並開 PR。

**原始信件只會存放在私人 repo `bluehomewu/newsroom-inbox`。** 部落格 repo 是公開的，只會收到轉換後的文章與圖片；`newsroom/*` 分支也已用 repository ruleset 封鎖，舊版程式無法再把信件推到公開 repo。

## 流程

1. Apps Script 每 15 分鐘找出要處理的信件，把原始信件存到私人 repo 的 `inbox/<message_id>/`，再發送 `repository_dispatch` 通知部落格 repo。
2. GitHub Actions 從私人 repo 讀取信件，用 Claude 判斷是不是新聞稿、轉成 Markdown、壓縮圖片，把文章推到 `press/<message_id>` 分支、開 PR，並上傳 Cloudflare 預覽。處理結果寫回私人 repo 的 `inbox/<message_id>/result.json`。
3. Apps Script 下次執行時讀取結果，把信件標成「已處理」「略過」或「錯誤」。
4. 確認預覽後在 GitHub 按 Merge，網站就會發佈。

要重新處理某封信：到部落格 repo 的 Actions →「NewsRoom」→「Run workflow」，輸入信件的 message id。

## 處理哪些信件

| 來源 | 條件 |
|---|---|
| 白名單 | `Code.gs` 裡 `sourceLabels` 列出的標籤（目前是「華碩新聞」「asustor華芸」） |
| 手動 | 你自己加上「NewsRoom」標籤的信件 |
| 自動偵測 | 收件匣裡含「新聞稿」「台北訊」等關鍵字、有附件的信件；PR 會標註「未知寄件者」 |

只處理 `setup()` 執行當天之後收到的信件。

## Gmail 標籤

| 標籤 | 意思 |
|---|---|
| `NewsRoom` | 手動要求處理 |
| `NewsRoom/處理中` | 已送到 GitHub，等待轉換 |
| `NewsRoom/已處理` | 已開 PR |
| `NewsRoom/略過` | AI 判斷不是新聞稿 |
| `NewsRoom/錯誤` | 轉換失敗，或超過 24 小時沒有結果 |

標籤會在第一次執行 `setup()` 時自動建立。

## 安裝

1. 打開 https://script.google.com ，按「新專案」，專案名稱改成 `NewsRoom`。
2. 把 `Code.gs` 的內容整份貼上，取代原本的程式碼，按儲存。
3. 左側「專案設定」（齒輪圖示）→ 最下方「指令碼屬性」→「新增指令碼屬性」：
   - 屬性：`GITHUB_TOKEN`
   - 值：GitHub fine-grained token（授權 `bluehomewu.github.io` 與 `newsroom-inbox` 兩個 repo，Contents 為 Read and write，Pull requests 為 Read-only）
4. 回到「編輯器」，上方函式選單選 `setup`，按「執行」。
5. 第一次執行會要求授權：選你的 Google 帳號 →「進階」→「前往 NewsRoom（不安全）」→「允許」。這是因為程式是你自己寫的、沒有經過 Google 審核，屬於正常情況。
6. 執行記錄出現「設定完成」就完成了。

## GitHub 端需要的 Secret

部落格 repo 的 Settings → Secrets and variables → Actions：

| Secret | 用途 |
|---|---|
| `ANTHROPIC_API_KEY` | Claude API 金鑰 |
| `CLOUDFLARE_API_TOKEN` | 上傳預覽網站 |
| `NEWSROOM_INBOX_TOKEN` | 讓 Actions 讀取私人收件匣、寫回處理結果；可以和 Apps Script 用同一個 token |

## 新增白名單廠商

在 `Code.gs` 的 `sourceLabels` 加上 Gmail 標籤名稱，例如：

```js
sourceLabels: ['華碩新聞', 'asustor華芸', 'Nothing 新聞'],
```

## 調整轉換格式

修改 `.github/newsroom/prompt.md`，下一封信就會套用新規則。
