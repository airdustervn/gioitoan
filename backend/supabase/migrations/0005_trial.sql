-- Giỏi Toán – tài khoản mới được dùng thử đầy đủ 7 ngày (chạy sau 0004)

alter table public.profiles add column if not exists trial_until timestamptz;

-- Số ngày dùng thử (đổi ở đây nếu muốn 3, 14 ngày…)
create or replace function public.trial_days()
returns int language sql immutable as $$ select 7 $$;

-- Tài khoản đã tạo: được dùng thử tính từ ngày đăng ký (ai quá 7 ngày thì coi như đã hết hạn)
update public.profiles set trial_until = created_at + make_interval(days => public.trial_days())
 where trial_until is null;

-- Tạo hồ sơ + bật dùng thử cho tài khoản mới (giữ nguyên cách đặt tên của bản 0003)
create or replace function public.handle_new_user()
returns trigger language plpgsql security definer set search_path = public as $$
declare
  base text;
  uname text;
  n int := 0;
begin
  base := lower(coalesce(new.raw_user_meta_data->>'username', split_part(new.email, '@', 1)));
  base := regexp_replace(base, '[^a-z0-9_.]', '', 'g');
  if length(base) < 4 then base := rpad(coalesce(nullif(base, ''), 'hs'), 4, '0'); end if;
  base := left(base, 24);
  uname := base;
  while exists (select 1 from public.profiles where username = uname) loop
    n := n + 1;
    uname := base || n;
  end loop;
  insert into public.profiles (id, username, full_name, grade, trial_until)
  values (
    new.id,
    uname,
    left(coalesce(new.raw_user_meta_data->>'full_name', new.raw_user_meta_data->>'name', ''), 80),
    least(12, greatest(1, coalesce((new.raw_user_meta_data->>'grade')::int, 1))),
    now() + make_interval(days => public.trial_days())
  );
  return new;
end $$;

-- Không cho học sinh tự sửa ngày dùng thử
revoke update on public.profiles from authenticated, anon;
grant  update (full_name, grade) on public.profiles to authenticated;

-- Trừ lượt: gói trả phí HOẶC còn dùng thử thì không giới hạn
create or replace function public.consume(kind text)
returns json language plpgsql security definer set search_path = public as $$
declare
  p public.profiles;
  lim record;
  today date := (now() at time zone 'Asia/Ho_Chi_Minh')::date;
  used int;
begin
  if kind not in ('question','exam') then raise exception 'kind không hợp lệ'; end if;
  select * into p from public.profiles where id = auth.uid();
  if p.id is null then return json_build_object('allowed', false, 'reason', 'login'); end if;
  if (p.premium_until is not null and p.premium_until > now()) then
    return json_build_object('allowed', true, 'premium', true);
  end if;
  if (p.trial_until is not null and p.trial_until > now()) then
    return json_build_object('allowed', true, 'premium', true, 'trial', true);
  end if;
  select * into lim from public.free_limits();
  insert into public.daily_usage (user_id, day) values (p.id, today) on conflict do nothing;
  if kind = 'question' then
    update public.daily_usage set questions = questions + 1
      where user_id = p.id and day = today and questions < lim.questions
      returning questions into used;
    if used is null then return json_build_object('allowed', false, 'reason', 'quota', 'limit', lim.questions); end if;
    return json_build_object('allowed', true, 'premium', false, 'remaining', lim.questions - used);
  else
    update public.daily_usage set exams = exams + 1
      where user_id = p.id and day = today and exams < lim.exams
      returning exams into used;
    if used is null then return json_build_object('allowed', false, 'reason', 'quota', 'limit', lim.exams); end if;
    return json_build_object('allowed', true, 'premium', false, 'remaining', lim.exams - used);
  end if;
end $$;

-- Trạng thái: thêm trial / trial_until; "premium" = được dùng không giới hạn (trả phí hoặc dùng thử)
create or replace function public.my_status()
returns json language plpgsql security definer set search_path = public as $$
declare
  p public.profiles;
  u public.daily_usage;
  au auth.users;
  lim record;
  today date := (now() at time zone 'Asia/Ho_Chi_Minh')::date;
  paid boolean;
  trial boolean;
begin
  select * into p from public.profiles where id = auth.uid();
  if p.id is null then return json_build_object('logged_in', false); end if;
  select * into au from auth.users where id = p.id;
  select * into u from public.daily_usage where user_id = p.id and day = today;
  select * into lim from public.free_limits();
  paid  := coalesce(p.premium_until > now(), false);
  trial := not paid and coalesce(p.trial_until > now(), false);
  return json_build_object(
    'logged_in', true,
    'username', p.username, 'full_name', p.full_name, 'grade', p.grade,
    'provider', coalesce(au.raw_app_meta_data->>'provider', 'email'),
    'email', case when au.email like '%@hs.gioitoan.com.vn' then null else au.email end,
    'is_admin', public.is_admin(),
    'premium', paid or trial,
    'paid', paid,
    'trial', trial,
    'trial_until', p.trial_until,
    'trial_days', public.trial_days(),
    'premium_until', p.premium_until,
    'used_questions', coalesce(u.questions, 0), 'used_exams', coalesce(u.exams, 0),
    'limit_questions', lim.questions, 'limit_exams', lim.exams
  );
end $$;

-- Quản trị: thêm cột hạn dùng thử và số đang dùng thử
create or replace function public.admin_users(q text default '', lim int default 50, off int default 0)
returns json language plpgsql security definer set search_path = public as $$
declare
  today date := (now() at time zone 'Asia/Ho_Chi_Minh')::date;
  pat text := '%' || lower(coalesce(q, '')) || '%';
  res json;
begin
  if not public.is_admin() then raise exception 'not_admin' using errcode = '42501'; end if;
  lim := least(greatest(coalesce(lim, 50), 1), 200);
  select json_build_object(
    'total',    (select count(*) from public.profiles),
    'today',    (select count(*) from public.profiles where (created_at at time zone 'Asia/Ho_Chi_Minh')::date = today),
    'week',     (select count(*) from public.profiles where created_at > now() - interval '7 days'),
    'premium',  (select count(*) from public.profiles where premium_until > now()),
    'trial',    (select count(*) from public.profiles where trial_until > now() and (premium_until is null or premium_until <= now())),
    'google',   (select count(*) from auth.users where raw_app_meta_data->>'provider' = 'google'),
    'active',   (select count(distinct user_id) from public.daily_usage where day = today),
    'matched',  (select count(*) from public.profiles p join auth.users u on u.id = p.id
                  where lower(p.username) like pat or lower(p.full_name) like pat or lower(u.email) like pat),
    'rows', coalesce((
      select json_agg(r) from (
        select p.username, p.full_name, p.grade, p.created_at, p.premium_until, p.trial_until,
               u.last_sign_in_at,
               coalesce(u.raw_app_meta_data->>'provider', 'email') as provider,
               case when u.email like '%@hs.gioitoan.com.vn' then null else u.email end as email,
               coalesce(d.questions, 0) as q_today, coalesce(d.exams, 0) as e_today
        from public.profiles p
        join auth.users u on u.id = p.id
        left join public.daily_usage d on d.user_id = p.id and d.day = today
        where lower(p.username) like pat or lower(p.full_name) like pat or lower(u.email) like pat
        order by p.created_at desc
        limit lim offset greatest(coalesce(off, 0), 0)
      ) r), '[]'::json)
  ) into res;
  return res;
end $$;

grant execute on function public.my_status() to authenticated;
grant execute on function public.consume(text) to authenticated;
revoke all on function public.admin_users(text, int, int) from public, anon;
grant execute on function public.admin_users(text, int, int) to authenticated;
