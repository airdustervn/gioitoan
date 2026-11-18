-- Giỏi Toán – siết quyền theo cảnh báo bảo mật của Supabase (đã chạy 18/11/2026)
revoke execute on function public.handle_new_user() from public, anon, authenticated;
alter function public.free_limits() set search_path = public;
alter function public.clean_tag(text, int) set search_path = public;
alter function public.trial_days() set search_path = public;
revoke execute on function public.my_status() from public, anon;
revoke execute on function public.consume(text) from public, anon;
grant execute on function public.my_status() to authenticated;
grant execute on function public.consume(text) to authenticated;
