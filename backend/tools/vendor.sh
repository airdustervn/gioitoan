#!/usr/bin/env bash
# Tải supabase-js về site (tự phục vụ, không phụ thuộc CDN) và in mã toàn vẹn SRI.
# Dùng: bash tools/vendor.sh <thư-mục-site> [phiên-bản]
set -euo pipefail
SITE=${1:?thư mục site}; V=${2:-2.45.4}
URL="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@${V}/dist/umd/supabase.js"
mkdir -p "$SITE/lib"
curl -fsSL "$URL" -o "$SITE/lib/supabase.js"
SRI="sha384-$(openssl dgst -sha384 -binary "$SITE/lib/supabase.js" | openssl base64 -A)"
echo "Đã lưu $SITE/lib/supabase.js"
echo "SUPABASE_JS_SRI: $SRI"
echo "Nếu muốn dùng thẳng CDN thay vì tự lưu: --supabase-js $URL --sri $SRI"
