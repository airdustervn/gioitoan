-- 0009: Danh sách tài khoản trong trang quản trị lọc được theo từng chỉ số
-- (bấm vào ô số liệu để xem đó là những tài khoản nào).
create or replace function public.admin_users_f(q text default '', lim int default 50, off int default 0,
                                                f text default 'all', p_days int default 30)
returns json language plpgsql security definer set search_path = public as $$
declare
  today date := (now() at time zone 'Asia/Ho_Chi_Minh')::date;
  n int := greatest(7, least(coalesce(p_days, 30), 90));
  since date := today - (n - 1);
  pat text := '%' || lower(coalesce(q, '')) || '%';
  ff text := coalesce(nullif(f, ''), 'all');
  res json;
begin
  if not public.is_admin() then raise exception 'not_admin' using errcode = '42501'; end if;
  lim := least(greatest(coalesce(lim, 50), 1), 500);
  with base as (
    select p.id, p.username, p.full_name, p.grade, p.created_at, p.premium_until, p.trial_until,
           u.last_sign_in_at,
           coalesce(u.raw_app_meta_data->>'provider', 'email') as provider,
           case when u.email like '%@hs.gioitoan.com.vn' then null else u.email end as email
    from public.profiles p join auth.users u on u.id = p.id
    where (lower(p.username) like pat or lower(coalesce(p.full_name,'')) like pat or lower(coalesce(u.email,'')) like pat)
      and case ff
        when 'all'      then true
        when 'today'    then (p.created_at at time zone 'Asia/Ho_Chi_Minh')::date = today
        when 'week'     then p.created_at > now() - interval '7 days'
        when 'premium'  then p.premium_until > now()
        when 'trial'    then p.trial_until > now() and (p.premium_until is null or p.premium_until <= now())
        when 'free'     then (p.premium_until is null or p.premium_until <= now()) and (p.trial_until is null or p.trial_until <= now())
        when 'google'   then u.raw_app_meta_data->>'provider' = 'google'
        when 'active'   then exists (select 1 from public.daily_usage d where d.user_id = p.id and d.day = today)
                          or exists (select 1 from public.user_activity x where x.user_id = p.id and x.day = today)
        when 'dau'      then exists (select 1 from public.user_activity x where x.user_id = p.id and x.day = today)
        when 'wau'      then exists (select 1 from public.user_activity x where x.user_id = p.id and x.day >= today - 6)
        when 'mau'      then exists (select 1 from public.user_activity x where x.user_id = p.id and x.day >= today - 29)
        when 'learned'  then exists (select 1 from public.user_activity x where x.user_id = p.id and x.day >= since and x.questions > 0)
        when 'examined' then exists (select 1 from public.user_activity x where x.user_id = p.id and x.day >= since and x.exams > 0)
        when 'returning' then (select count(*) from public.user_activity x where x.user_id = p.id and x.day >= since) >= 2
        when 'new'      then p.created_at >= now() - make_interval(days => n)
        when 'new_on'   then p.created_at >= now() - make_interval(days => n)
                          and exists (select 1 from public.user_activity x where x.user_id = p.id and x.questions + x.exams > 0)
        when 'new_off'  then p.created_at >= now() - make_interval(days => n)
                          and not exists (select 1 from public.user_activity x where x.user_id = p.id and x.questions + x.exams > 0)
        when 'new_7'    then p.created_at >= now() - make_interval(days => n)
                          and exists (select 1 from public.user_activity x where x.user_id = p.id and x.day >= today - 6)
        else false end
  )
  select json_build_object(
    'matched', (select count(*) from base),
    'rows', coalesce((
      select json_agg(r) from (
        select b.username, b.full_name, b.grade, b.created_at, b.premium_until, b.trial_until,
               b.last_sign_in_at, b.provider, b.email,
               coalesce(d.questions, 0) as q_today, coalesce(d.exams, 0) as e_today,
               (select max(x.last_at) from public.user_activity x where x.user_id = b.id) as last_act,
               (select coalesce(sum(x.questions),0) from public.user_activity x where x.user_id = b.id and x.day >= since) as q_period,
               (select count(*) from public.user_activity x where x.user_id = b.id and x.day >= since) as days_period
        from base b
        left join public.daily_usage d on d.user_id = b.id and d.day = today
        order by b.created_at desc
        limit lim offset greatest(coalesce(off, 0), 0)
      ) r), '[]'::json)
  ) into res;
  return res;
end $$;

revoke all on function public.admin_users_f(text, int, int, text, int) from public, anon;
grant execute on function public.admin_users_f(text, int, int, text, int) to authenticated;
