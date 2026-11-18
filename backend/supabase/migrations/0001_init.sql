-- =====================================================================
--  Giỏi Toán (gioitoan.com.vn) – Tài khoản học sinh, gói trả phí, thanh toán VietQR (PayOS)
--  Chạy toàn bộ file này một lần trong Supabase: SQL Editor > New query > Run
-- =====================================================================

-- ---------- 1. Hồ sơ học sinh (1 tài khoản = 1 học sinh) ----------
create table if not exists public.profiles (
  id            uuid primary key references auth.users(id) on delete cascade,
  username      text unique not null check (username ~ '^[a-z0-9_.]{4,30}$'),
  full_name     text not null default '',
  grade         int  not null default 1 check (grade between 1 and 12),
  premium_until timestamptz,                     -- hết hạn gói trả phí (null = chưa mua)
  created_at    timestamptz not null default now()
);

-- Tự tạo hồ sơ khi có tài khoản mới (thông tin lấy từ metadata lúc đăng ký)
create or replace function public.handle_new_user()
returns trigger language plpgsql security definer set search_path = public as $$
begin
  insert into public.profiles (id, username, full_name, grade)
  values (
    new.id,
    lower(coalesce(new.raw_user_meta_data->>'username', split_part(new.email, '@', 1))),
    coalesce(new.raw_user_meta_data->>'full_name', ''),
    coalesce((new.raw_user_meta_data->>'grade')::int, 1)
  );
  return new;
end $$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function public.handle_new_user();

-- ---------- 2. Các gói trả phí (sửa giá tại đây hoặc trong Table Editor) ----------
create table if not exists public.plans (
  id        text primary key,
  name      text not null,
  price_vnd int  not null check (price_vnd >= 2000),
  days      int  not null check (days > 0),
  active    boolean not null default true,
  sort      int  not null default 0
);

insert into public.plans (id, name, price_vnd, days, sort) values
  ('thang', 'Gói 1 tháng',  59000,  30, 1),
  ('quy',   'Gói 3 tháng', 99000,  90, 2),
  ('nam',   'Gói 1 năm',   299000, 365, 3)
on conflict (id) do nothing;

-- ---------- 3. Đơn hàng thanh toán ----------
create table if not exists public.orders (
  id              bigserial primary key,
  order_code      bigint unique not null,         -- mã đơn gửi sang PayOS
  user_id         uuid not null references public.profiles(id) on delete cascade,
  plan_id         text not null references public.plans(id),
  amount          int  not null,
  status          text not null default 'pending' check (status in ('pending','paid','cancelled')),
  payos_link_id   text,
  checkout_url    text,
  qr_code         text,
  created_at      timestamptz not null default now(),
  paid_at         timestamptz,
  raw_webhook     jsonb
);
create index if not exists orders_user_idx on public.orders(user_id, created_at desc);

-- ---------- 4. Lượt dùng miễn phí theo ngày ----------
create table if not exists public.daily_usage (
  user_id   uuid not null references public.profiles(id) on delete cascade,
  day       date not null default (now() at time zone 'Asia/Ho_Chi_Minh')::date,
  questions int  not null default 0,
  exams     int  not null default 0,
  primary key (user_id, day)
);

-- Giới hạn gói miễn phí (sửa số ở đây)
create or replace function public.free_limits()
returns table (questions int, exams int) language sql immutable as $$
  select 10, 1   -- 10 câu luyện tập + 1 đề thi mỗi ngày
$$;

-- ---------- 5. Bảo mật theo dòng (RLS) ----------
alter table public.profiles    enable row level security;
alter table public.plans       enable row level security;
alter table public.orders      enable row level security;
alter table public.daily_usage enable row level security;

drop policy if exists "profile_select_own" on public.profiles;
create policy "profile_select_own" on public.profiles for select using (auth.uid() = id);

drop policy if exists "profile_update_own" on public.profiles;
create policy "profile_update_own" on public.profiles for update using (auth.uid() = id) with check (auth.uid() = id);

-- Học sinh chỉ được sửa họ tên và lớp, KHÔNG được sửa username hay hạn gói
revoke update on public.profiles from authenticated, anon;
grant  update (full_name, grade) on public.profiles to authenticated;

drop policy if exists "plans_read_all" on public.plans;
create policy "plans_read_all" on public.plans for select using (active);

drop policy if exists "orders_select_own" on public.orders;
create policy "orders_select_own" on public.orders for select using (auth.uid() = user_id);
-- Không có policy insert/update cho orders: chỉ Edge Function (service role) được ghi.

drop policy if exists "usage_select_own" on public.daily_usage;
create policy "usage_select_own" on public.daily_usage for select using (auth.uid() = user_id);

-- ---------- 6. Hàm dùng chung ----------
-- Trạng thái tài khoản để hiển thị trên trang
create or replace function public.my_status()
returns json language plpgsql security definer set search_path = public as $$
declare
  p public.profiles;
  u public.daily_usage;
  lim record;
  today date := (now() at time zone 'Asia/Ho_Chi_Minh')::date;
begin
  select * into p from public.profiles where id = auth.uid();
  if p.id is null then return json_build_object('logged_in', false); end if;
  select * into u from public.daily_usage where user_id = p.id and day = today;
  select * into lim from public.free_limits();
  return json_build_object(
    'logged_in', true,
    'username', p.username, 'full_name', p.full_name, 'grade', p.grade,
    'premium', coalesce(p.premium_until > now(), false),
    'premium_until', p.premium_until,
    'used_questions', coalesce(u.questions, 0), 'used_exams', coalesce(u.exams, 0),
    'limit_questions', lim.questions, 'limit_exams', lim.exams
  );
end $$;

-- Trừ 1 lượt miễn phí. kind = 'question' hoặc 'exam'. Gói trả phí thì luôn cho phép.
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
  if p.premium_until is not null and p.premium_until > now() then
    return json_build_object('allowed', true, 'premium', true);
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

-- Kích hoạt đơn đã thanh toán (chỉ Edge Function gọi bằng service role).
-- Chạy nhiều lần vẫn an toàn: đơn đã 'paid' sẽ không cộng thêm ngày.
create or replace function public.activate_order(p_order_code bigint, p_amount int, p_raw jsonb)
returns text language plpgsql security definer set search_path = public as $$
declare
  o public.orders;
  pl public.plans;
begin
  select * into o from public.orders where order_code = p_order_code for update;
  if o.id is null then return 'not_found'; end if;
  if o.status = 'paid' then return 'already_paid'; end if;
  if p_amount < o.amount then return 'amount_mismatch'; end if;

  select * into pl from public.plans where id = o.plan_id;
  update public.orders set status = 'paid', paid_at = now(), raw_webhook = p_raw where id = o.id;
  update public.profiles
     set premium_until = greatest(coalesce(premium_until, now()), now()) + make_interval(days => pl.days)
   where id = o.user_id;
  return 'activated';
end $$;

revoke all on function public.activate_order(bigint, int, jsonb) from public, anon, authenticated;
grant execute on function public.my_status() to authenticated;
grant execute on function public.consume(text) to authenticated;

-- ---------- 7. Tiện ích cho quản trị (chạy tay trong SQL Editor khi cần) ----------
-- Tặng/gia hạn gói thủ công cho một học sinh:
--   update public.profiles set premium_until = greatest(coalesce(premium_until, now()), now()) + interval '30 days'
--   where username = 'ten_dang_nhap';
-- Xem doanh thu theo tháng:
--   select date_trunc('month', paid_at) thang, count(*) so_don, sum(amount) doanh_thu
--   from public.orders where status = 'paid' group by 1 order by 1 desc;
