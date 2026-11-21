-- Giỏi Toán – Lịch sử đề giáo viên đã tạo (Góc giáo viên › Bảng điều khiển)

create table if not exists public.teacher_papers (
  id          bigserial primary key,
  user_id     uuid not null default auth.uid() references public.profiles(id) on delete cascade,
  local_id    text not null,                     -- mã đề phía trình duyệt (tránh trùng khi đồng bộ)
  created_at  timestamptz not null default now(),
  grade       int  not null check (grade between 1 and 12),
  kind        text not null default 'c',         -- 15 | 45 | gk1 | hk1 | gk2 | hk2 | c
  title       text not null default '',
  minutes     int  not null default 15,
  n           int  not null default 0,
  n_mc        int  not null default 0,
  n_f         int  not null default 0,
  ver         int  not null default 1,
  codes       text not null default '',
  own         int  not null default 0,           -- số câu tự soạn
  chapters    text[] not null default '{}',
  downloads   int  not null default 0,           -- lượt tải Word
  prints      int  not null default 0,           -- lượt in / PDF
  data        jsonb,                             -- nội dung đề để mở lại
  unique (user_id, local_id),
  constraint teacher_papers_size check (data is null or octet_length(data::text) < 600000)
);
create index if not exists teacher_papers_user_idx on public.teacher_papers(user_id, created_at desc);

alter table public.teacher_papers enable row level security;
drop policy if exists tp_sel on public.teacher_papers;
drop policy if exists tp_ins on public.teacher_papers;
drop policy if exists tp_upd on public.teacher_papers;
drop policy if exists tp_del on public.teacher_papers;
create policy tp_sel on public.teacher_papers for select using (user_id = auth.uid());
create policy tp_ins on public.teacher_papers for insert with check (user_id = auth.uid());
create policy tp_upd on public.teacher_papers for update using (user_id = auth.uid()) with check (user_id = auth.uid());
create policy tp_del on public.teacher_papers for delete using (user_id = auth.uid());

revoke all on public.teacher_papers from anon;
grant select, insert, update, delete on public.teacher_papers to authenticated;
grant usage, select on sequence public.teacher_papers_id_seq to authenticated;

-- Tăng lượt tải / in (an toàn, chỉ đề của chính mình)
create or replace function public.teacher_paper_hit(p_local_id text, p_kind text)
returns void language plpgsql security definer set search_path = public as $$
begin
  update public.teacher_papers
     set downloads = downloads + case when p_kind = 'docx' then 1 else 0 end,
         prints    = prints    + case when p_kind = 'print' then 1 else 0 end
   where user_id = auth.uid() and local_id = p_local_id;
end $$;
revoke all on function public.teacher_paper_hit(text, text) from public, anon;
grant execute on function public.teacher_paper_hit(text, text) to authenticated;
