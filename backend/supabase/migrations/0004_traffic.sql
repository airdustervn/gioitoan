-- Giỏi Toán – đo lượt truy cập và nguồn đăng ký (chạy sau 0003)

-- 1) Lượt vào web: mỗi trình duyệt có một mã ẩn danh (vid), không lưu IP.
create table if not exists public.visits (
  id        bigserial primary key,
  at        timestamptz not null default now(),
  day       date not null default (now() at time zone 'Asia/Ho_Chi_Minh')::date,
  vid       text not null,
  source    text not null default 'direct',
  medium    text not null default '',
  campaign  text not null default '',
  path      text not null default '',
  ref_host  text not null default '',
  user_id   uuid
);
create index if not exists visits_day_idx on public.visits (day);
create index if not exists visits_vid_idx on public.visits (vid, at desc);
alter table public.visits enable row level security;
revoke all on public.visits from anon, authenticated;

-- 2) Nguồn đăng ký của từng tài khoản
alter table public.profiles add column if not exists signup_source   text;
alter table public.profiles add column if not exists signup_campaign text;

create or replace function public.clean_tag(t text, n int default 60)
returns text language sql immutable as $$
  select left(regexp_replace(lower(coalesce(t, '')), '[^a-z0-9_.\-]', '', 'g'), n)
$$;

-- Ghi một lượt vào (mọi người gọi được). Chống ghi trùng: cùng trình duyệt + cùng nguồn trong 30 phút chỉ tính 1.
create or replace function public.log_visit(p_vid text, p_source text, p_medium text, p_campaign text, p_path text, p_ref text)
returns void language plpgsql security definer set search_path = public as $$
declare v text := left(coalesce(p_vid, ''), 40); s text := coalesce(nullif(public.clean_tag(p_source), ''), 'direct');
        c text := public.clean_tag(p_campaign);
begin
  if v !~ '^[A-Za-z0-9_-]{8,40}$' then return; end if;
  if (select count(*) from public.visits where at > now() - interval '1 minute') > 600 then return; end if;
  if exists (select 1 from public.visits where vid = v and source = s and campaign = c and at > now() - interval '30 minutes') then return; end if;
  insert into public.visits (vid, source, medium, campaign, path, ref_host, user_id)
  values (v, s, public.clean_tag(p_medium), c, left(coalesce(p_path, ''), 80), public.clean_tag(p_ref, 80), auth.uid());
end $$;

-- Gắn nguồn đăng ký cho tài khoản của chính mình (chỉ khi chưa có và tài khoản mới tạo trong 2 ngày)
create or replace function public.set_signup_source(p_source text, p_campaign text)
returns void language plpgsql security definer set search_path = public as $$
begin
  update public.profiles
     set signup_source = coalesce(nullif(public.clean_tag(p_source), ''), 'direct'),
         signup_campaign = public.clean_tag(p_campaign)
   where id = auth.uid() and signup_source is null and created_at > now() - interval '2 days';
end $$;

-- 3) Báo cáo cho quản trị
create or replace function public.admin_traffic(p_days int default 30)
returns json language plpgsql security definer set search_path = public as $$
declare
  d int := least(greatest(coalesce(p_days, 30), 1), 365);
  since date := (now() at time zone 'Asia/Ho_Chi_Minh')::date - (d - 1);
  res json;
begin
  if not public.is_admin() then raise exception 'not_admin' using errcode = '42501'; end if;
  select json_build_object(
    'days', d,
    'visits',  (select count(*) from public.visits where day >= since),
    'uniques', (select count(distinct vid) from public.visits where day >= since),
    'signups', (select count(*) from public.profiles where (created_at at time zone 'Asia/Ho_Chi_Minh')::date >= since),
    'daily', coalesce((select json_agg(x order by x.day) from (
        select g::date as day,
               (select count(*) from public.visits v where v.day = g::date) as visits,
               (select count(distinct vid) from public.visits v where v.day = g::date) as uniques,
               (select count(*) from public.profiles p where (p.created_at at time zone 'Asia/Ho_Chi_Minh')::date = g::date) as signups
        from generate_series(since, (now() at time zone 'Asia/Ho_Chi_Minh')::date, interval '1 day') g) x), '[]'::json),
    'sources', coalesce((select json_agg(y order by y.visits desc) from (
        select coalesce(v.source, p.source) as source, coalesce(v.campaign, p.campaign) as campaign,
               coalesce(v.visits, 0) as visits, coalesce(v.uniques, 0) as uniques, coalesce(p.signups, 0) as signups
        from (select source, campaign, count(*) visits, count(distinct vid) uniques
                from public.visits where day >= since group by 1, 2) v
        full join (select coalesce(signup_source, 'chưa rõ') source, coalesce(signup_campaign, '') campaign, count(*) signups
                from public.profiles where (created_at at time zone 'Asia/Ho_Chi_Minh')::date >= since group by 1, 2) p
          on p.source = v.source and p.campaign = v.campaign
        limit 50) y), '[]'::json),
    'referrers', coalesce((select json_agg(z) from (
        select ref_host, count(*) visits from public.visits
         where day >= since and ref_host <> '' group by 1 order by 2 desc limit 10) z), '[]'::json)
  ) into res;
  return res;
end $$;

revoke all on function public.log_visit(text, text, text, text, text, text) from public;
grant execute on function public.log_visit(text, text, text, text, text, text) to anon, authenticated;
revoke all on function public.set_signup_source(text, text) from public, anon;
grant execute on function public.set_signup_source(text, text) to authenticated;
revoke all on function public.admin_traffic(int) from public, anon;
grant execute on function public.admin_traffic(int) to authenticated;
