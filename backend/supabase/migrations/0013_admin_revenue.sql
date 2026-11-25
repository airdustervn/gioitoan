-- Giỏi Toán – Báo cáo doanh thu cho quản trị viên (trang Quản trị › Báo cáo doanh thu)
-- Ngày tính theo giờ Việt Nam. Doanh thu = các đơn đã thanh toán (status = 'paid'), tính theo paid_at.

create or replace function public.admin_revenue(p_from date, p_to date)
returns json language plpgsql stable security definer set search_path = public as $$
declare
  tz constant text := 'Asia/Ho_Chi_Minh';
  t0 timestamptz;
  t1 timestamptz;
  res json;
begin
  if not public.is_admin() then raise exception 'not_admin' using errcode = '42501'; end if;
  if p_from is null or p_to is null or p_to < p_from or p_to - p_from > 3660 then raise exception 'bad_range'; end if;
  t0 := (p_from::timestamp) at time zone tz;
  t1 := ((p_to + 1)::timestamp) at time zone tz;

  with paid as (
    select o.*, coalesce(pl.audience, 'hs') as audience, coalesce(pl.name, o.plan_id) as plan_name,
           (o.paid_at at time zone tz)::date as d
      from orders o left join plans pl on pl.id = o.plan_id
     where o.status = 'paid' and o.paid_at >= t0 and o.paid_at < t1
  ),
  created as (
    select o.* from orders o where o.created_at >= t0 and o.created_at < t1
  ),
  firsts as (   -- lần thanh toán đầu tiên của mỗi tài khoản (để biết khách mới / gia hạn)
    select user_id, min(paid_at) as first_paid from orders where status = 'paid' group by user_id
  ),
  span as (
    select case when p_to - p_from > 92 then 'month' else 'day' end as unit
  ),
  buckets as (
    select g::date as b
      from span, generate_series(
        case when (select unit from span) = 'month' then date_trunc('month', p_from::timestamp) else p_from::timestamp end,
        p_to::timestamp,
        case when (select unit from span) = 'month' then interval '1 month' else interval '1 day' end) g
  )
  select json_build_object(
    'from', p_from, 'to', p_to, 'unit', (select unit from span),
    'paid_count',  (select count(*) from paid),
    'revenue',     (select coalesce(sum(amount), 0) from paid),
    'revenue_hs',  (select coalesce(sum(amount), 0) from paid where audience = 'hs'),
    'revenue_gv',  (select coalesce(sum(amount), 0) from paid where audience = 'gv'),
    'payers',      (select count(distinct user_id) from paid),
    'new_payers',  (select count(distinct p.user_id) from paid p join firsts f on f.user_id = p.user_id and f.first_paid >= t0 and f.first_paid < t1),
    'created_count',   (select count(*) from created),
    'created_paid',    (select count(*) from created where status = 'paid'),
    'pending_count',   (select count(*) from created where status = 'pending'),
    'pending_amount',  (select coalesce(sum(amount), 0) from created where status = 'pending'),
    'cancelled_count', (select count(*) from created where status = 'cancelled'),
    'all_time',    (select coalesce(sum(amount), 0) from orders where status = 'paid'),
    'all_time_count', (select count(*) from orders where status = 'paid'),
    'active_premium', (select count(*) from profiles where premium_until > now()),
    'active_teacher', (select count(*) from profiles where teacher_until > now()),
    'series', (select coalesce(json_agg(json_build_object('d', b.b, 'v', coalesce(x.v, 0), 'n', coalesce(x.n, 0)) order by b.b), '[]')
                 from buckets b left join (
                   select case when (select unit from span) = 'month' then date_trunc('month', d)::date else d end as k,
                          sum(amount) v, count(*) n
                     from paid group by 1) x on x.k = b.b),
    'by_plan', (select coalesce(json_agg(r order by r.v desc), '[]') from (
                  select plan_id as id, max(plan_name) as name, max(audience) as audience, count(*) n, sum(amount) v
                    from paid group by plan_id) r),
    'orders', (select coalesce(json_agg(r order by r.paid_at desc), '[]') from (
                  select p.order_code, p.plan_name, p.audience, p.amount, p.paid_at, pr.username, pr.full_name,
                         (f.first_paid = p.paid_at) as is_new
                    from paid p left join profiles pr on pr.id = p.user_id left join firsts f on f.user_id = p.user_id
                   order by p.paid_at desc limit 500) r)
  ) into res;
  return res;
end $$;
revoke all on function public.admin_revenue(date, date) from public, anon;
grant execute on function public.admin_revenue(date, date) to authenticated;
