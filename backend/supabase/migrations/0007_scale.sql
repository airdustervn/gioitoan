-- Chịu tải: index theo thời gian cho visits; nâng trần chống spam log_visit lên 5000 lượt/phút
create index if not exists visits_at_idx on public.visits (at desc);
create or replace function public.log_visit(p_vid text, p_source text, p_medium text, p_campaign text, p_path text, p_ref text)
 returns void language plpgsql security definer set search_path to 'public' as $function$
declare v text := left(coalesce(p_vid, ''), 40); s text := coalesce(nullif(public.clean_tag(p_source), ''), 'direct');
        c text := public.clean_tag(p_campaign);
begin
  if v !~ '^[A-Za-z0-9_-]{8,40}$' then return; end if;
  if (select count(*) from (select 1 from public.visits where at > now() - interval '1 minute' limit 5001) t) > 5000 then return; end if;
  if exists (select 1 from public.visits where vid = v and source = s and campaign = c and at > now() - interval '30 minutes') then return; end if;
  insert into public.visits (vid, source, medium, campaign, path, ref_host, user_id)
  values (v, s, public.clean_tag(p_medium), c, left(coalesce(p_path, ''), 80), public.clean_tag(p_ref, 80), auth.uid());
end $function$;
