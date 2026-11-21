-- Giỏi Toán – Gói giáo viên (Góc giáo viên: ra đề kiểm tra)
-- Dùng thử 7 ngày, sau đó phải đăng nhập và mua gói giáo viên (giá/kỳ hạn giống gói học sinh).

alter table public.profiles add column if not exists teacher_until timestamptz;        -- hết hạn gói giáo viên
alter table public.profiles add column if not exists teacher_trial_until timestamptz;  -- hết hạn dùng thử giáo viên

alter table public.plans add column if not exists audience text not null default 'hs';
do $$ begin
  alter table public.plans add constraint plans_audience_chk check (audience in ('hs','gv'));
exception when duplicate_object then null; end $$;

insert into public.plans (id, name, price_vnd, days, sort, audience) values
  ('gv_thang', 'Giáo viên 1 tháng',  59000,  30, 11, 'gv'),
  ('gv_quy',   'Giáo viên 3 tháng', 149000,  90, 12, 'gv'),
  ('gv_nua',   'Giáo viên 6 tháng', 199000, 180, 13, 'gv'),
  ('gv_nam',   'Giáo viên 1 năm',   299000, 365, 14, 'gv')
on conflict (id) do nothing;

-- Kích hoạt đơn: gói giáo viên cộng vào teacher_until, gói học sinh cộng vào premium_until
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
  if pl.audience = 'gv' then
    update public.profiles
       set teacher_until = greatest(coalesce(teacher_until, now()), now()) + make_interval(days => pl.days)
     where id = o.user_id;
  else
    update public.profiles
       set premium_until = greatest(coalesce(premium_until, now()), now()) + make_interval(days => pl.days)
     where id = o.user_id;
  end if;
  return 'activated';
end $$;
revoke all on function public.activate_order(bigint, int, jsonb) from public, anon, authenticated;

-- Trạng thái gói giáo viên của tài khoản đang đăng nhập.
-- p_first: thời điểm trình duyệt bắt đầu dùng thử khi chưa đăng nhập – không cộng dồn thêm 7 ngày.
-- p_start = true (gọi từ Góc giáo viên): lần đầu sẽ bắt đầu dùng thử; false (trang tài khoản): chỉ xem.
drop function if exists public.teacher_status(timestamptz);
create or replace function public.teacher_status(p_first timestamptz default null, p_start boolean default true)
returns json language plpgsql security definer set search_path = public as $$
declare
  p public.profiles;
  st timestamptz;
begin
  select * into p from public.profiles where id = auth.uid();
  if p.id is null then return json_build_object('logged_in', false); end if;
  if p.teacher_trial_until is null and p_start then
    st := greatest(least(coalesce(p_first, now()), now()), now() - interval '7 days');
    update public.profiles set teacher_trial_until = st + interval '7 days'
     where id = p.id returning * into p;
  end if;
  return json_build_object(
    'logged_in', true,
    'paid', coalesce(p.teacher_until > now(), false),
    'teacher_until', p.teacher_until,
    'trial', coalesce(p.teacher_trial_until > now(), false) and not coalesce(p.teacher_until > now(), false),
    'trial_until', p.teacher_trial_until,
    'started', p.teacher_trial_until is not null or p.teacher_until is not null,
    'active', coalesce(p.teacher_until > now(), false) or coalesce(p.teacher_trial_until > now(), false),
    'is_admin', public.is_admin()
  );
end $$;
revoke all on function public.teacher_status(timestamptz, boolean) from public, anon;
grant execute on function public.teacher_status(timestamptz, boolean) to authenticated;

-- Quản trị: tặng / gia hạn / hủy gói giáo viên (p_days = 0 để hủy)
create or replace function public.admin_set_teacher(p_username text, p_days int)
returns timestamptz language plpgsql security definer set search_path = public as $$
declare r timestamptz;
begin
  if not public.is_admin() then raise exception 'not_admin' using errcode = '42501'; end if;
  if p_days is null or p_days < 0 or p_days > 3660 then raise exception 'bad_days'; end if;
  update public.profiles
     set teacher_until = case when p_days = 0 then null
                              else greatest(coalesce(teacher_until, now()), now()) + make_interval(days => p_days) end
   where username = lower(p_username)
   returning teacher_until into r;
  if not found then raise exception 'not_found'; end if;
  return r;
end $$;
revoke all on function public.admin_set_teacher(text, int) from public, anon;
grant execute on function public.admin_set_teacher(text, int) to authenticated;
