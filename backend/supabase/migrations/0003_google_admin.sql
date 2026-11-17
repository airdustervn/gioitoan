-- Giỏi Toán – đăng nhập Google + trang quản trị (chạy sau 0001, 0002)

-- 1) Danh sách email quản trị. Không có policy => chỉ máy chủ đọc được.
create table if not exists public.admins (email text primary key);
alter table public.admins enable row level security;
revoke all on public.admins from anon, authenticated;
insert into public.admins (email) values ('airdustervn@gmail.com') on conflict do nothing;

create or replace function public.is_admin()
returns boolean language sql stable security definer set search_path = public as $$
  select exists (
    select 1 from public.admins a join auth.users u on lower(u.email) = lower(a.email)
    where u.id = auth.uid()
  );
$$;

-- 2) Tạo hồ sơ cho mọi kiểu đăng ký (tên đăng nhập hoặc Google).
--    Tài khoản Google: lấy phần trước @ của Gmail, lọc ký tự lạ, thêm số nếu trùng.
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
  insert into public.profiles (id, username, full_name, grade)
  values (
    new.id,
    uname,
    left(coalesce(new.raw_user_meta_data->>'full_name', new.raw_user_meta_data->>'name', ''), 80),
    least(12, greatest(1, coalesce((new.raw_user_meta_data->>'grade')::int, 1)))
  );
  return new;
end $$;

-- 3) Trạng thái tài khoản: thêm is_admin, email Google, cách đăng nhập.
create or replace function public.my_status()
returns json language plpgsql security definer set search_path = public as $$
declare
  p public.profiles;
  u public.daily_usage;
  au auth.users;
  lim record;
  today date := (now() at time zone 'Asia/Ho_Chi_Minh')::date;
begin
  select * into p from public.profiles where id = auth.uid();
  if p.id is null then return json_build_object('logged_in', false); end if;
  select * into au from auth.users where id = p.id;
  select * into u from public.daily_usage where user_id = p.id and day = today;
  select * into lim from public.free_limits();
  return json_build_object(
    'logged_in', true,
    'username', p.username, 'full_name', p.full_name, 'grade', p.grade,
    'provider', coalesce(au.raw_app_meta_data->>'provider', 'email'),
    'email', case when au.email like '%@hs.gioitoan.com.vn' then null else au.email end,
    'is_admin', public.is_admin(),
    'premium', coalesce(p.premium_until > now(), false),
    'premium_until', p.premium_until,
    'used_questions', coalesce(u.questions, 0), 'used_exams', coalesce(u.exams, 0),
    'limit_questions', lim.questions, 'limit_exams', lim.exams
  );
end $$;

-- 4) Danh sách tài khoản cho quản trị (tìm theo tên đăng nhập / họ tên / email), có phân trang.
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
    'google',   (select count(*) from auth.users where raw_app_meta_data->>'provider' = 'google'),
    'active',   (select count(distinct user_id) from public.daily_usage where day = today),
    'matched',  (select count(*) from public.profiles p join auth.users u on u.id = p.id
                  where lower(p.username) like pat or lower(p.full_name) like pat or lower(u.email) like pat),
    'rows', coalesce((
      select json_agg(r) from (
        select p.username, p.full_name, p.grade, p.created_at, p.premium_until,
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

-- 5) Quản trị cấp/thu hồi gói trả phí bằng tay (p_days = 0 để thu hồi).
create or replace function public.admin_set_premium(p_username text, p_days int)
returns timestamptz language plpgsql security definer set search_path = public as $$
declare r timestamptz;
begin
  if not public.is_admin() then raise exception 'not_admin' using errcode = '42501'; end if;
  if p_days is null or p_days < 0 or p_days > 3660 then raise exception 'bad_days'; end if;
  update public.profiles
     set premium_until = case when p_days = 0 then null
                              else greatest(coalesce(premium_until, now()), now()) + make_interval(days => p_days) end
   where username = lower(p_username)
   returning premium_until into r;
  if not found then raise exception 'not_found'; end if;
  return r;
end $$;

revoke all on function public.admin_users(text, int, int) from public, anon;
revoke all on function public.admin_set_premium(text, int) from public, anon;
revoke all on function public.is_admin() from public, anon;
grant execute on function public.admin_users(text, int, int) to authenticated;
grant execute on function public.admin_set_premium(text, int) to authenticated;
grant execute on function public.is_admin() to authenticated;
grant execute on function public.my_status() to authenticated;
