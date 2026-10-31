// Pageview counter for edwardwu23.com posts and press releases: every page load counts once.
//   POST /hit?path=/posts/<slug>    increment, returns {"count": n}
//   GET  /count?path=/posts/<slug>  read only, returns {"count": n}
// /newsroom/<slug> paths are accepted the same way.

const ALLOWED_ORIGINS = ['https://edwardwu23.com'];
const PATH_RE = /^\/(posts|newsroom)\/[a-z0-9._-]{1,150}$/;
const BOT_RE = /bot|crawl|spider|slurp|headless|lighthouse|preview|facebookexternalhit|embedly|curl|wget|python/i;

const normalize = (raw) => {
  const path = (raw || '').toLowerCase().replace(/\/+$/, '');
  return PATH_RE.test(path) ? path : null;
};

const corsHeaders = (origin) => ({
  'Access-Control-Allow-Origin': ALLOWED_ORIGINS.includes(origin) ? origin : ALLOWED_ORIGINS[0],
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Max-Age': '86400',
  Vary: 'Origin',
});

const json = (body, status, origin) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store', ...corsHeaders(origin) },
  });

const readCount = async (db, path) => {
  const row = await db.prepare('SELECT count FROM pageviews WHERE path = ?').bind(path).first();
  return row ? row.count : 0;
};

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const origin = request.headers.get('Origin') || '';

    if (request.method === 'OPTIONS') return new Response(null, { status: 204, headers: corsHeaders(origin) });

    const path = normalize(url.searchParams.get('path'));
    if (!path) return json({ error: 'invalid path' }, 400, origin);

    if (url.pathname === '/count' && request.method === 'GET') {
      return json({ count: await readCount(env.DB, path) }, 200, origin);
    }

    if (url.pathname === '/hit' && request.method === 'POST') {
      // Only count real visits from the blog itself; anything else just reads the current value
      const ua = request.headers.get('User-Agent') || '';
      if (!ALLOWED_ORIGINS.includes(origin) || BOT_RE.test(ua)) {
        return json({ count: await readCount(env.DB, path) }, 200, origin);
      }
      const row = await env.DB.prepare(
        'INSERT INTO pageviews (path, count) VALUES (?, 1) ON CONFLICT(path) DO UPDATE SET count = count + 1 RETURNING count'
      )
        .bind(path)
        .first();
      return json({ count: row.count }, 200, origin);
    }

    return json({ error: 'not found' }, 404, origin);
  },
};
