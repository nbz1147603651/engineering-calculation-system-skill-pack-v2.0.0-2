#!/usr/bin/env bash
# Re-download vendored KaTeX 0.16.11 assets into webapp/static/vendor/katex/.
#
# Run from the project template root (engineering_calc_project/) or pass the
# target directory as $1. The vendored copy is committed to the repo so the
# app works offline / air-gapped; this script exists to make the vendoring
# reproducible and to refresh assets when KaTeX is upgraded.
#
# Usage:  bash scripts/vendor_katex.sh [vendor_dir]
set -euo pipefail

KATEX_VERSION="0.16.11"
BASE_URL="https://cdn.jsdelivr.net/npm/katex@${KATEX_VERSION}/dist"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEFAULT_TARGET="${SCRIPT_DIR}/../webapp/static/vendor/katex"
TARGET_DIR="${1:-${DEFAULT_TARGET}}"

mkdir -p "${TARGET_DIR}/fonts" "${TARGET_DIR}/contrib"

echo "Downloading KaTeX ${KATEX_VERSION} into ${TARGET_DIR}"

curl -fsSL "${BASE_URL}/katex.min.css"        -o "${TARGET_DIR}/katex.min.css"
curl -fsSL "${BASE_URL}/katex.min.js"         -o "${TARGET_DIR}/katex.min.js"
curl -fsSL "${BASE_URL}/contrib/auto-render.min.js" -o "${TARGET_DIR}/contrib/auto-render.min.js"

FONT_FAMILIES=(
  KaTeX_AMS-Regular
  KaTeX_Caligraphic-Bold
  KaTeX_Caligraphic-Regular
  KaTeX_Fraktur-Bold
  KaTeX_Fraktur-Regular
  KaTeX_Main-Bold
  KaTeX_Main-BoldItalic
  KaTeX_Main-Italic
  KaTeX_Main-Regular
  KaTeX_Math-BoldItalic
  KaTeX_Math-Italic
  KaTeX_SansSerif-Bold
  KaTeX_SansSerif-Italic
  KaTeX_SansSerif-Regular
  KaTeX_Script-Regular
  KaTeX_Size1-Regular
  KaTeX_Size2-Regular
  KaTeX_Size3-Regular
  KaTeX_Size4-Regular
  KaTeX_Typewriter-Regular
)

for family in "${FONT_FAMILIES[@]}"; do
  for ext in woff2 woff ttf; do
    curl -fsSL "${BASE_URL}/fonts/${family}.${ext}" -o "${TARGET_DIR}/fonts/${family}.${ext}"
  done
done

echo
echo "KaTeX ${KATEX_VERSION} vendored. Verify with:"
echo "  sha256sum ${TARGET_DIR}/katex.min.css ${TARGET_DIR}/katex.min.js"
echo
echo "Files: $(find "${TARGET_DIR}" -type f | wc -l)  Size: $(du -sh "${TARGET_DIR}" | cut -f1)"
