-- Giỏi Toán – bảo vệ đề trên máy chủ (chạy sau 0001_init.sql)
-- Đề và đáp án nằm trong bảng papers, KHÔNG có policy nào => anon/authenticated không đọc được.
-- Chỉ hàm get-paper (service role) đọc và trả đề sau khi kiểm tra lượt/gói.

create table if not exists public.papers (
  id         text primary key,
  cat        text not null default '',
  free       boolean not null default false,   -- true: đề mẫu cho xem không cần lượt
  data       jsonb not null,
  updated_at timestamptz not null default now()
);
alter table public.papers enable row level security;
revoke all on public.papers from anon, authenticated;

-- Ai đã mở đề nào: mở lại cùng đề trong 24 giờ không bị trừ thêm lượt; đồng thời chặn tải hàng loạt.
create table if not exists public.paper_access (
  user_id   uuid not null references auth.users(id) on delete cascade,
  paper_id  text not null references public.papers(id) on delete cascade,
  opened_at timestamptz not null default now(),
  primary key (user_id, paper_id)
);
create index if not exists paper_access_user_time on public.paper_access (user_id, opened_at desc);
alter table public.paper_access enable row level security;
revoke all on public.paper_access from anon, authenticated;
