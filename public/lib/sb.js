/* Giỏi Toán – bộ kết nối Supabase tối giản (thay supabase-js, không tải script ngoài).
   Hỗ trợ đúng phần trang dùng: auth (signUp, signInWithPassword, signOut, getSession, onAuthStateChange),
   rpc, from(t).select().order().limit(), from(t).update().eq(), functions.invoke. */
(function () {
  function createClient(url, key) {
    url = url.replace(/\/$/, "");
    const SKEY = "sb-" + new URL(url).hostname.split(".")[0] + "-auth";
    const subs = [];
    let session = null;
    try { session = JSON.parse(localStorage.getItem(SKEY) || "null"); } catch (_) { session = null; }

    function save(s, ev) {
      session = s;
      try { s ? localStorage.setItem(SKEY, JSON.stringify(s)) : localStorage.removeItem(SKEY); } catch (_) {}
      subs.forEach(f => { try { f(ev, s); } catch (_) {} });
    }
    function norm(d) {
      if (!d || !d.access_token) return null;
      return { access_token: d.access_token, refresh_token: d.refresh_token,
        expires_at: d.expires_at || Math.floor(Date.now() / 1000) + (d.expires_in || 3600), user: d.user };
    }
    async function req(path, opt = {}, auth = true) {
      const h = Object.assign({ apikey: key, "Content-Type": "application/json" }, opt.headers || {});
      if (auth) { const s = await getValid(); h.Authorization = "Bearer " + (s ? s.access_token : key); }
      return fetch(url + path, Object.assign({}, opt, { headers: h }));
    }
    async function asJson(res) {
      const t = await res.text(); let b = null; try { b = t ? JSON.parse(t) : null; } catch (_) { b = t; }
      if (!res.ok) return { data: null, error: { status: res.status, message: (b && (b.msg || b.message || b.error_description || b.error)) || ("HTTP " + res.status), body: b } };
      return { data: b, error: null };
    }
    let refreshing = null;
    async function getValid() {
      if (!session) return null;
      if (session.expires_at - 60 > Date.now() / 1000) return session;
      if (!refreshing) refreshing = (async () => {
        const r = await asJson(await req("/auth/v1/token?grant_type=refresh_token",
          { method: "POST", body: JSON.stringify({ refresh_token: session.refresh_token }) }, false));
        save(r.error ? null : norm(r.data), r.error ? "SIGNED_OUT" : "TOKEN_REFRESHED");
      })().finally(() => { refreshing = null; });
      await refreshing;
      return session;
    }

    const auth = {
      async getSession() { return { data: { session: await getValid() }, error: null }; },
      onAuthStateChange(f) { subs.push(f); return { data: { subscription: { unsubscribe() { const i = subs.indexOf(f); if (i >= 0) subs.splice(i, 1); } } } }; },
      async signUp({ email, password, options }) {
        const r = await asJson(await req("/auth/v1/signup", { method: "POST",
          body: JSON.stringify({ email, password, data: (options && options.data) || {} }) }, false));
        if (r.error) return r;
        const s = norm(r.data); if (s) save(s, "SIGNED_IN");
        return { data: { session: s, user: (r.data && r.data.user) || r.data }, error: null };
      },
      async signInWithPassword({ email, password }) {
        const r = await asJson(await req("/auth/v1/token?grant_type=password", { method: "POST",
          body: JSON.stringify({ email, password }) }, false));
        if (r.error) return r;
        const s = norm(r.data); save(s, "SIGNED_IN");
        return { data: { session: s, user: s && s.user }, error: null };
      },
      async signOut() {
        if (session) { try { await req("/auth/v1/logout", { method: "POST" }); } catch (_) {} }
        save(null, "SIGNED_OUT"); return { error: null };
      }
    };

    async function rpc(fn, args) {
      return asJson(await req("/rest/v1/rpc/" + encodeURIComponent(fn), { method: "POST", body: JSON.stringify(args || {}) }));
    }

    function from(table) {
      const q = { table, params: [], method: "GET", body: null };
      const api = {
        select(cols) { q.params.push("select=" + encodeURIComponent(cols || "*")); return api; },
        order(col, o) { q.params.push("order=" + encodeURIComponent(col) + "." + (o && o.ascending === false ? "desc" : "asc")); return api; },
        limit(n) { q.params.push("limit=" + (n | 0)); return api; },
        eq(col, v) { q.params.push(encodeURIComponent(col) + "=eq." + encodeURIComponent(v)); return api; },
        update(obj) { q.method = "PATCH"; q.body = JSON.stringify(obj); return api; },
        then(ok, no) {
          const headers = q.method === "PATCH" ? { Prefer: "return=minimal" } : {};
          return req("/rest/v1/" + encodeURIComponent(q.table) + (q.params.length ? "?" + q.params.join("&") : ""),
            { method: q.method, body: q.body, headers }).then(asJson).then(ok, no);
        }
      };
      return api;
    }

    const functions = {
      async invoke(name, { body } = {}) {
        const res = await req("/functions/v1/" + encodeURIComponent(name), { method: "POST", body: JSON.stringify(body || {}) });
        if (!res.ok) return { data: null, error: { status: res.status, message: "HTTP " + res.status, context: res } };
        const t = await res.text(); let d = null; try { d = t ? JSON.parse(t) : null; } catch (_) { d = t; }
        return { data: d, error: null };
      }
    };

    return { auth, rpc, from, functions };
  }
  window.supabase = { createClient };
})();
