-- Theo dõi hoạt động học của từng tài khoản + dashboard quản trị
alter table public.profiles add column if not exists last_seen_at timestamptz;

create table if not exists public.user_activity (
  user_id   uuid not null references auth.users(id) on delete cascade,
  day       date not null,
  questions int  not null default 0,
  correct   int  not null default 0,
  exams     int  not null default 0,
  seconds   int  not null default 0,
  sessions  int  not null default 0,
  first_at  timestamptz not null default now(),
  last_at   timestamptz not null default now(),
  primary key (user_id, day)
);
create index if not exists user_activity_day_idx on public.user_activity (day);
alter table public.user_activity enable row level security;

create table if not exists public.exam_log (
  id      bigserial primary key,
  user_id uuid not null references auth.users(id) on delete cascade,
  at      timestamptz not null default now(),
  title   text,
  right_n int,
  total_n int,
  pct     numeric
);
create index if not exists exam_log_at_idx on public.exam_log (at desc);
create index if not exists exam_log_user_idx on public.exam_log (user_id, at desc);
alter table public.exam_log enable row level security;

-- Ghi hoạt động: q = trả lời 1 câu, exam = nộp 1 đề, ping = 60 giây đang học, session = mở trang
create or replace function public.act(p_kind text, p_ok boolean default null, p_secs int default 0,
  p_title text default null, p_r int default null, p_n int default null, p_pct numeric default null)
returns void language plpgsql security definer set search_path = public as $$
declare uid uuid := auth.uid(); d date := (now() at time zone 'Asia/Ho_Chi_Minh')::date; cur public.user_activity;
begin
  if uid is null or p_kind not in ('q','exam','ping','session') then return; end if;
  insert into public.user_activity (user_id, day) values (uid, d) on conflict do nothing;
  select * into cur from public.user_activity where user_id = uid and day = d;
  if p_kind = 'q' then
    if cur.questions >= 3000 then return; end if;
    update public.user_activity set questions = questions + 1, correct = correct + (case when p_ok then 1 else 0 end), last_at = now()
      where user_id = uid and day = d;
  elsif p_kind = 'exam' then
    if cur.exams >= 200 then return; end if;
    update public.user_activity set exams = exams + 1, last_at = now() where user_id = uid and day = d;
    insert into public.exam_log (user_id, title, right_n, total_n, pct)
    values (uid, left(coalesce(p_title, ''), 80),
            greatest(0, least(coalesce(p_r, 0), 500)), greatest(0, least(coalesce(p_n, 0), 500)),
            case when p_pct is null then null else greatest(0, least(p_pct, 100)) end);
  elsif p_kind = 'ping' then
    -- tối đa 1 ping / 50 giây được tính, tối đa 16 giờ / ngày
    if now() - cur.last_at < interval '50 seconds' and cur.seconds > 0 then return; end if;
    update public.user_activity set seconds = least(seconds + greatest(0, least(coalesce(p_secs, 60), 60)), 57600), last_at = now()
      where user_id = uid and day = d;
  else
    if cur.sessions >= 200 then return; end if;
    update public.user_activity set sessions = sessions + 1, last_at = now() where user_id = uid and day = d;
  end if;
  update public.profiles set last_seen_at = now() where id = uid;
end $$;
revoke all on function public.act(text, boolean, int, text, int, int, numeric) from public, anon;
grant execute on function public.act(text, boolean, int, text, int, int, numeric) to authenticated;

-- Dashboard quản trị
create or replace function public.admin_activity(p_days int default 30)
returns json language plpgsql security definer set search_path = public as $$
declare n int := greatest(7, least(coalesce(p_days, 30), 90));
        today date := (now() at time zone 'Asia/Ho_Chi_Minh')::date;
        since date := today - (n - 1);
        res json;
begin
  if not public.is_admin() then raise exception 'not admin'; end if;
  with a as (select * from public.user_activity where day >= since),
  days as (select generate_series(since, today, interval '1 day')::date as day),
  series as (
    select d.day,
      (select count(*) from a where a.day = d.day) as active,
      (select coalesce(sum(questions),0) from a where a.day = d.day) as questions,
      (select coalesce(sum(exams),0) from a where a.day = d.day) as exams,
      (select coalesce(sum(seconds),0)/60 from a where a.day = d.day) as minutes,
      (select count(*) from public.profiles p where (p.created_at at time zone 'Asia/Ho_Chi_Minh')::date = d.day) as signups
    from days d order by d.day),
  per_user as (
    select user_id, sum(questions) q, sum(correct) c, sum(exams) e, sum(seconds)/60 m, count(*) days_active, max(last_at) last_at
    from a group by user_id),
  top as (
    select pu.*, p.username, p.full_name, p.grade,
      case when p.premium_until > now() then 'PRO' when p.trial_until > now() then 'Dùng thử' else 'Miễn phí' end as plan
    from per_user pu join public.profiles p on p.id = pu.user_id
    order by pu.m desc, pu.q desc limit 50),
  recent as (
    select e.at, e.title, e.right_n, e.total_n, e.pct, p.username
    from public.exam_log e join public.profiles p on p.id = e.user_id
    order by e.at desc limit 25),
  grades as (
    select coalesce(p.grade, 0) grade, count(*) users, sum(pu.q) q
    from per_user pu join public.profiles p on p.id = pu.user_id group by 1 order by 1),
  hours as (
    select extract(hour from (e.at at time zone 'Asia/Ho_Chi_Minh'))::int h, count(*) c
    from public.exam_log e where e.at >= since group by 1),
  cohort as (
    select count(*) filter (where true) as signed,
           count(*) filter (where exists (select 1 from public.user_activity x where x.user_id = p.id and x.questions + x.exams > 0)) as activated,
           count(*) filter (where exists (select 1 from public.user_activity x where x.user_id = p.id and x.day >= today - 6)) as active7
    from public.profiles p where p.created_at >= now() - make_interval(days => n))
  select json_build_object(
    'days', n,
    'kpi', json_build_object(
      'users', (select count(*) from public.profiles),
      'dau', (select count(*) from public.user_activity where day = today),
      'wau', (select count(distinct user_id) from public.user_activity where day >= today - 6),
      'mau', (select count(distinct user_id) from public.user_activity where day >= today - 29),
      'q_period', (select coalesce(sum(questions),0) from a),
      'acc_period', (select case when sum(questions) > 0 then round(100.0 * sum(correct) / sum(questions)) end from a),
      'exams_period', (select coalesce(sum(exams),0) from a),
      'min_per_user', (select case when count(*) > 0 then round(sum(seconds)::numeric / 60 / count(*), 1) end from a),
      'avg_pct', (select round(avg(pct)) from public.exam_log where at >= since and pct is not null),
      'paid', (select count(*) from public.profiles where premium_until > now()),
      'trial', (select count(*) from public.profiles where trial_until > now() and (premium_until is null or premium_until <= now())),
      'returning', (select count(*) from per_user where days_active >= 2)),
    'cohort', (select row_to_json(cohort) from cohort),
    'series', (select json_agg(series) from series),
    'top', (select coalesce(json_agg(top), '[]'::json) from top),
    'recent', (select coalesce(json_agg(recent), '[]'::json) from recent),
    'grades', (select coalesce(json_agg(grades), '[]'::json) from grades),
    'hours', (select coalesce(json_agg(hours), '[]'::json) from hours)
  ) into res;
  return res;
end $$;
revoke all on function public.admin_activity(int) from public, anon;
grant execute on function public.admin_activity(int) to authenticated;
