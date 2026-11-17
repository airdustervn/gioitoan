#!/usr/bin/env python3
"""Đẩy papers.jsonl lên bảng public.papers (upsert theo id).

Dùng:  SUPABASE_URL=https://<ma>.supabase.co SUPABASE_SERVICE_ROLE_KEY=... python3 tools/upload_papers.py out/papers.jsonl
Khóa service role chỉ dùng trên máy của bạn, tuyệt đối không đưa vào index.html hay lên hosting.
"""
import json, os, sys, urllib.request
url = os.environ["SUPABASE_URL"].rstrip("/") + "/rest/v1/papers?on_conflict=id"
key = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
rows = [json.loads(l) for l in open(sys.argv[1], encoding="utf-8") if l.strip()]
for i in range(0, len(rows), 50):
    body = json.dumps(rows[i:i + 50], ensure_ascii=False).encode()
    req = urllib.request.Request(url, body, method="POST", headers={
        "apikey": key, "Authorization": "Bearer " + key, "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates,return=minimal"})
    urllib.request.urlopen(req).read()
    print(f"{min(i + 50, len(rows))}/{len(rows)}")
