-- 0010: Học sinh xem lại lịch sử học của chính mình (bảng học tập trong trang Tài khoản)
create or replace function public.my_history(p_days int default 30)
returns json language sql stable security definer set search_path = public as $$
  select case when auth.uid() is null then null else json_build_object(
    'days', coalesce((select json_agg(json_build_object('day', a.day, 'q', a.questions, 'ok', a.correct, 'ex', a.exams, 'sec', a.seconds) order by a.day)
              from public.user_activity a
              where a.user_id = auth.uid()
                and a.day >= (now() at time zone 'Asia/Ho_Chi_Minh')::date - (greatest(7, least(coalesce(p_days, 30), 120)) - 1)), '[]'::json),
    'exams', coalesce((select json_agg(e) from (
              select l.at, l.title, l.right_n as r, l.total_n as n, l.pct
              from public.exam_log l where l.user_id = auth.uid()
              order by l.at desc limit 100) e), '[]'::json),
    'tot', (select json_build_object('q', coalesce(sum(questions),0), 'ok', coalesce(sum(correct),0), 'ex', coalesce(sum(exams),0), 'sec', coalesce(sum(seconds),0))
            from public.user_activity where user_id = auth.uid())
  ) end
$$;
revoke all on function public.my_history(int) from public, anon;
grant execute on function public.my_history(int) to authenticated;
