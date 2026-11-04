#!/usr/bin/env bash
#
# Merge a new jekyll-theme-chirpy release into this blog with a real `git merge`.
#
# The blog keeps its own copies of many theme files (_includes, _layouts, _sass, ...)
# and customizes them. To let git do proper three-way merges, the theme files of each
# upstream release are snapshotted onto the `chirpy-upstream` branch, which `main`
# merges. Git then uses the previous snapshot as the merge base, so local
# customizations are kept and only upstream changes are applied (conflicts are marked
# as usual).
#
# Usage:
#   tools/sync-chirpy.sh <tag>          e.g. tools/sync-chirpy.sh v7.7.0
#   tools/sync-chirpy.sh --init <tag>   one-time setup: record <tag> as already merged
#
# After a sync:
#   1. resolve conflicts (git status), review `git diff --cached`
#   2. check the PWA overrides in assets/js/dist if the script warns about them
#   3. bundle update jekyll-theme-chirpy && JEKYLL_ENV=production bundle exec jekyll build
#   4. git commit
#
# 中文說明：每次上游發布新版時執行 `tools/sync-chirpy.sh vX.Y.Z`，腳本會把該版本的主題檔案
# 快照到 chirpy-upstream 分支，再用 git merge 合併進目前分支；客製化會保留，衝突照一般方式處理。

set -euo pipefail

BRANCH="chirpy-upstream"
UPSTREAM_URL="https://github.com/cotes2020/jekyll-theme-chirpy.git"

# Theme files this blog keeps a copy of. Paths missing upstream are skipped.
PATHS=(
  _includes
  _layouts
  _sass
  _javascript
  _data/locales
  _data/contact.yml
  _data/share.yml
  _plugins
  _tabs/archives.md
  _tabs/categories.md
  _tabs/tags.md
  assets/img/favicons/site.webmanifest
  assets/js/data/search.json
  assets/lib
  tools/run.sh
  tools/test.sh
  .devcontainer
  .vscode
  _config.yml
  index.html
  .editorconfig
  .gitattributes
  .gitignore
  .gitmodules
  .nojekyll
  LICENSE
)

# Upstream path -> path in this repo
declare -A RENAMES=(
  [.github/workflows/starter/pages-deploy.yml]=.github/workflows/pages-deploy.yml
)

# Upstream files that this blog overrides elsewhere and must be reviewed by hand
WATCH=(_javascript/pwa _includes/notification.html assets/js/data/swconf.js)

die() {
  echo "error: $*" >&2
  exit 1
}

init=false
if [[ ${1:-} == "--init" ]]; then
  init=true
  shift
fi
tag=${1:-}
[[ -n $tag ]] || die "usage: $0 [--init] <tag>"

cd "$(git rev-parse --show-toplevel)"
[[ -z $(git status --porcelain --untracked-files=no) ]] || die "working tree has uncommitted changes"

remote=$(git remote -v | awk '/cotes2020\/jekyll-theme-chirpy(\.git)? \(fetch\)/ {print $1; exit}')
if [[ -z $remote ]]; then
  remote="chirpy"
  git remote add "$remote" "$UPSTREAM_URL"
fi
echo "Fetching $tag from $remote ..."
git fetch --quiet --no-tags "$remote" "refs/tags/$tag:refs/tags/$tag"
upstream=$(git rev-parse "$tag^{commit}")

# Build the snapshot tree in a temporary index, without touching the working tree
index=$(mktemp)
trap 'rm -f "$index"' EXIT
export GIT_INDEX_FILE=$index
git read-tree --empty
for path in "${PATHS[@]}"; do
  git ls-tree -r --full-tree "$upstream" -- "$path" | git update-index --index-info
done
for src in "${!RENAMES[@]}"; do
  git ls-tree -r --full-tree "$upstream" -- "$src" |
    sed "s|	$src\$|	${RENAMES[$src]}|" | git update-index --index-info
done
tree=$(git write-tree)
unset GIT_INDEX_FILE

parent=()
previous=""
if git rev-parse --verify --quiet "refs/heads/$BRANCH" >/dev/null; then
  previous=$(git log -1 --format=%s "$BRANCH" | sed -n 's/^Chirpy upstream \([^ ]*\).*/\1/p')
  if [[ $(git rev-parse "$BRANCH^{tree}") == "$tree" ]]; then
    echo "$BRANCH already matches $tag"
  else
    parent=(-p "$BRANCH")
  fi
elif ! $init; then
  die "branch $BRANCH does not exist yet; run '$0 --init <tag of the last synced release>' first"
fi

if [[ $(git rev-parse "$BRANCH^{tree}" 2>/dev/null) != "$tree" ]]; then
  commit=$(git commit-tree "$tree" "${parent[@]}" \
    -m "Chirpy upstream $tag" -m "Snapshot of the theme files from cotes2020/jekyll-theme-chirpy@$upstream.")
  git update-ref "refs/heads/$BRANCH" "$commit"
  echo "Updated $BRANCH to $tag"
fi

if $init; then
  git merge --quiet -s ours --allow-unrelated-histories --no-edit \
    -m "Theme: Record chirpy $tag as the theme sync base" "$BRANCH"
  echo "Recorded $tag as already merged. Future syncs: $0 <new tag>"
  exit 0
fi

if [[ -n $previous ]]; then
  changed=$(git diff --name-only "$previous" "$tag" -- "${WATCH[@]}" 2>/dev/null || true)
  if [[ -n $changed ]]; then
    echo
    echo "NOTE: upstream changed files that assets/js/dist/{app,sw}.min.js override; review them:"
    echo "$changed" | sed 's/^/  /'
  fi
fi

version=${tag#v}
echo
if git merge --no-ff --no-commit "$BRANCH" -m "Theme: Merge chirpy $tag"; then
  echo "Merged without conflicts."
else
  echo "Merge has conflicts; resolve them, then commit."
fi
sed -i -E "s/^(gem \"jekyll-theme-chirpy\", )\"[^\"]+\"/\1\"$version\"/" Gemfile
git add Gemfile
echo "Gemfile now pins jekyll-theme-chirpy $version. Next: bundle update jekyll-theme-chirpy, build, test, commit."
