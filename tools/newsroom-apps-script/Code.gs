/**
 * NewsRoom — 把廠商新聞稿 Email 送到 GitHub，由 GitHub Actions 轉成部落格文章並開 PR。
 *
 * 安裝步驟見同資料夾的 README.md。需要在「專案設定 → 指令碼屬性」新增：
 *   GITHUB_TOKEN  只授權 bluehomewu.github.io、Contents 可讀寫的 fine-grained token
 *
 * 處理的信件：
 *   1. 來源標籤（SOURCE_LABELS）裡的新信件
 *   2. 你手動加上「NewsRoom」標籤的信件（新廠商、公關公司等例外）
 *   3. 收件匣裡含新聞稿關鍵字、有附件的信件（PR 會標註「未知寄件者」）
 */

const CONFIG = {
  owner: 'bluehomewu',
  repo: 'bluehomewu.github.io',
  baseBranch: 'main',
  sourceLabels: ['華碩新聞', 'asustor華芸'],
  labels: {
    manual: 'NewsRoom',
    processing: 'NewsRoom/處理中',
    done: 'NewsRoom/已處理',
    skipped: 'NewsRoom/略過',
    error: 'NewsRoom/錯誤',
  },
  detectKeywords: ['新聞稿', '"press release"', '新聞資料', '台北訊', '臺北訊', '媒體朋友', '解禁', '禁播'],
  maxPerRun: 5,
  pendingTimeoutHours: 24,
};

const PROPS = PropertiesService.getScriptProperties();

/** 第一次安裝時執行一次：建立標籤、記錄開始日期、設定每 15 分鐘執行。 */
function setup() {
  Object.values(CONFIG.labels).forEach(getOrCreateLabel_);
  if (!PROPS.getProperty('START_DATE')) {
    PROPS.setProperty('START_DATE', Utilities.formatDate(new Date(), 'Asia/Taipei', 'yyyy/MM/dd'));
  }
  ScriptApp.getProjectTriggers()
    .filter((t) => t.getHandlerFunction() === 'run')
    .forEach((t) => ScriptApp.deleteTrigger(t));
  ScriptApp.newTrigger('run').timeBased().everyMinutes(15).create();
  github_('GET', `/repos/${CONFIG.owner}/${CONFIG.repo}`); // fails early if the token is missing or wrong
  Logger.log(`設定完成，只會處理 ${PROPS.getProperty('START_DATE')} 之後收到的信件。`);
}

/** 定時執行：先更新之前送出的信件狀態，再送出新的信件。 */
function run() {
  const lock = LockService.getScriptLock();
  if (!lock.tryLock(1000)) return;
  try {
    checkPending_();
    sendNew_();
  } finally {
    lock.releaseLock();
  }
}

// ------------------------------------------------------------------ 送出新信件

function sendNew_() {
  const start = PROPS.getProperty('START_DATE');
  const exclude = Object.values(CONFIG.labels)
    .filter((name) => name !== CONFIG.labels.manual)
    .map((name) => `-${labelQuery_(name)}`)
    .join(' ');
  const sources = CONFIG.sourceLabels.map(labelQuery_);

  const queries = [
    { type: 'whitelist', label: '白名單標籤', query: `(${sources.join(' OR ')}) after:${start} ${exclude}` },
    { type: 'manual', label: '手動標記 NewsRoom', query: `${labelQuery_(CONFIG.labels.manual)} ${exclude}` },
    {
      type: 'detected',
      label: '自動偵測（未知寄件者）',
      query: `in:inbox has:attachment after:${start} (${CONFIG.detectKeywords.join(' OR ')}) ` +
        `${sources.map((q) => `-${q}`).join(' ')} -${labelQuery_(CONFIG.labels.manual)} -from:me ${exclude}`,
    },
  ];

  let sent = 0;
  const seen = {};
  for (const q of queries) {
    for (const thread of GmailApp.search(q.query, 0, CONFIG.maxPerRun)) {
      if (sent >= CONFIG.maxPerRun || seen[thread.getId()]) continue;
      seen[thread.getId()] = true;
      const message = pickMessage_(thread);
      if (!message) continue;
      try {
        sendToGitHub_(message, q);
        thread.addLabel(getOrCreateLabel_(CONFIG.labels.processing));
        PROPS.setProperty(`pending:${thread.getId()}`, JSON.stringify({ id: message.getId(), at: Date.now() }));
        sent++;
      } catch (e) {
        Logger.log(`送出失敗：${message.getSubject()} — ${e}`);
        thread.addLabel(getOrCreateLabel_(CONFIG.labels.error));
      }
    }
  }
  if (sent) Logger.log(`送出 ${sent} 封信件。`);
}

/** 使用討論串中最後一封不是自己寄出的信。 */
function pickMessage_(thread) {
  const me = Session.getActiveUser().getEmail().toLowerCase();
  const messages = thread.getMessages().filter((m) => !m.getFrom().toLowerCase().includes(me));
  return messages.length ? messages[messages.length - 1] : null;
}

/** 把原始信件與來源資訊提交到 newsroom/<message_id> 分支（一個 commit）。 */
function sendToGitHub_(message, source) {
  const id = message.getId();
  const branch = `newsroom/${id}`;
  const base = github_('GET', `/repos/${CONFIG.owner}/${CONFIG.repo}/git/ref/heads/${CONFIG.baseBranch}`).object.sha;
  const baseTree = github_('GET', `/repos/${CONFIG.owner}/${CONFIG.repo}/git/commits/${base}`).tree.sha;

  const meta = {
    message_id: id,
    thread_id: message.getThread().getId(),
    source_type: source.type,
    source_type_label: source.label,
    subject: message.getSubject(),
    from: message.getFrom(),
    date: message.getDate().toISOString(),
  };
  const files = {
    [`newsroom-inbox/${id}/email.eml`]: Utilities.newBlob(message.getRawContent()).getBytes(),
    [`newsroom-inbox/${id}/meta.json`]: Utilities.newBlob(JSON.stringify(meta, null, 2)).getBytes(),
  };

  const tree = Object.keys(files).map((path) => ({
    path,
    mode: '100644',
    type: 'blob',
    sha: github_('POST', `/repos/${CONFIG.owner}/${CONFIG.repo}/git/blobs`, {
      content: Utilities.base64Encode(files[path]),
      encoding: 'base64',
    }).sha,
  }));
  const treeSha = github_('POST', `/repos/${CONFIG.owner}/${CONFIG.repo}/git/trees`, { base_tree: baseTree, tree }).sha;
  const commit = github_('POST', `/repos/${CONFIG.owner}/${CONFIG.repo}/git/commits`, {
    message: `NewsRoom: Inbox ${message.getSubject()}`.slice(0, 200),
    tree: treeSha,
    parents: [base],
  }).sha;
  github_('POST', `/repos/${CONFIG.owner}/${CONFIG.repo}/git/refs`, { ref: `refs/heads/${branch}`, sha: commit });
}

// ------------------------------------------------------------------ 更新處理狀態

function checkPending_() {
  const all = PROPS.getProperties();
  for (const key of Object.keys(all).filter((k) => k.startsWith('pending:'))) {
    const threadId = key.slice('pending:'.length);
    const { id, at } = JSON.parse(all[key]);
    const status = lookupStatus_(id);
    if (!status && Date.now() - at < CONFIG.pendingTimeoutHours * 3600 * 1000) continue;

    const thread = GmailApp.getThreadById(threadId);
    const label = { created: 'done', skipped: 'skipped' }[status] || 'error';
    if (thread) {
      thread.removeLabel(getOrCreateLabel_(CONFIG.labels.processing));
      thread.addLabel(getOrCreateLabel_(CONFIG.labels[label]));
    }
    if (status === 'skipped') deleteBranch_(id);
    PROPS.deleteProperty(key);
  }
}

/** created：已開 PR；skipped / error：轉換程式寫回的結果；null：還在處理。 */
function lookupStatus_(id) {
  const branch = `newsroom/${id}`;
  const pulls = github_('GET', `/repos/${CONFIG.owner}/${CONFIG.repo}/pulls?state=all&head=${CONFIG.owner}:${encodeURIComponent(branch)}`);
  if (pulls.length) return 'created';
  const result = github_('GET', `/repos/${CONFIG.owner}/${CONFIG.repo}/contents/newsroom-inbox/${id}/result.json?ref=${encodeURIComponent(branch)}`, null, true);
  if (!result) return null;
  return JSON.parse(Utilities.newBlob(Utilities.base64Decode(result.content)).getDataAsString()).status;
}

function deleteBranch_(id) {
  github_('DELETE', `/repos/${CONFIG.owner}/${CONFIG.repo}/git/refs/heads/newsroom/${id}`, null, true);
}

// ------------------------------------------------------------------ 共用

function getOrCreateLabel_(name) {
  return GmailApp.getUserLabelByName(name) || GmailApp.createLabel(name);
}

/** Gmail 搜尋語法裡，標籤名稱的空白與斜線要換成連字號。 */
function labelQuery_(name) {
  return `label:${name.replace(/[\/\s]/g, '-')}`;
}

/** 呼叫 GitHub API；allowMissing 為 true 時，404 回傳 null。 */
function github_(method, path, body, allowMissing) {
  const token = PROPS.getProperty('GITHUB_TOKEN');
  if (!token) throw new Error('尚未在指令碼屬性設定 GITHUB_TOKEN');
  const res = UrlFetchApp.fetch(`https://api.github.com${path}`, {
    method,
    contentType: 'application/json',
    headers: {
      Authorization: `Bearer ${token}`,
      Accept: 'application/vnd.github+json',
      'X-GitHub-Api-Version': '2022-11-28',
    },
    payload: body ? JSON.stringify(body) : undefined,
    muteHttpExceptions: true,
  });
  const code = res.getResponseCode();
  if (allowMissing && code === 404) return null;
  if (code >= 300) throw new Error(`GitHub API ${method} ${path} 失敗（${code}）：${res.getContentText().slice(0, 300)}`);
  return code === 204 ? null : JSON.parse(res.getContentText());
}
