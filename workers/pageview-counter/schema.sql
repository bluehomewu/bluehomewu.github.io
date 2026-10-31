-- One row per post path (lowercase, no trailing slash)
CREATE TABLE IF NOT EXISTS pageviews (
  path TEXT PRIMARY KEY,
  count INTEGER NOT NULL DEFAULT 0
);
