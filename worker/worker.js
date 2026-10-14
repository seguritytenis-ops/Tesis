// Storefront worker: static assets + order notifications API.
const WA = "573169486100";
function esc(s){return String(s==null?"":s).slice(0,200);}
export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    let path = url.pathname;
    if (req.method === "POST" && path === "/api/order") {
      try {
        const d = await req.json();
        for (const k of ["name","phone","addr","city","product","mode","depto","talla"])
          if(typeof d[k]==="string") d[k]=d[k].slice(0,200);
        const total = Number(d.total)||0;
        if(!d.name || !d.phone) return new Response(JSON.stringify({ok:false,error:"datos"}),{status:422,headers:{"Content-Type":"application/json"}});
        const msg = `PEDIDO — $${total.toLocaleString()}\n${esc(d.product||"-")}\n${esc(d.name)} | ${esc(d.phone)}\n${esc(d.addr||"-")} (${esc(d.city||"-")}, ${esc(d.depto||"-")}) Talla:${esc(d.talla||"-")}\nModo: ${esc(d.mode)}`;
        const r = await fetch(`https://api.telegram.org/bot${env.TG_TOKEN}/sendMessage`, {
          method: "POST", headers: {"Content-Type":"application/json"},
          body: JSON.stringify({chat_id: env.TG_CHAT, text: msg})
        });
        if(!r.ok) return new Response(JSON.stringify({ok:false}),{status:502,headers:{"Content-Type":"application/json"}});
      } catch(e){ return new Response(JSON.stringify({ok:false}),{status:400,headers:{"Content-Type":"application/json"}}); }
      return new Response(JSON.stringify({ok:true, wa:WA}), {headers:{"Content-Type":"application/json"}});
    }
    if (req.method === "GET" && env.ASSETS) {
      const tryPaths = [path];
      if (path !== "/" && path.endsWith("/")) tryPaths.push(path + "index.html", path.slice(0,-1) + ".html");
      if (!path.includes(".") && !path.endsWith("/")) tryPaths.push(path + "/index.html", path + ".html");
      if (path.startsWith("/products/")) {
        const slug = path.split("/")[2];
        tryPaths.push(`/tabs_products/${slug}.html`, `/tabs_products/${slug}/index.html`);
      }
      if (path.startsWith("/collections/") || path.startsWith("/pages/") || path.startsWith("/policies/")) {
        const flat = path.replace(/^\//,"").replace(/\//g,"_");
        tryPaths.push(`/${flat}.html`, `/tabs/${flat}.html`);
      }
      if (path === "/checkout" || path === "/checkout/") tryPaths.push("/checkout.html", "/checkout/index.html");
      if (path === "/cart" || path === "/cart/") tryPaths.push("/tabs/cart.html", "/cart/index.html");
      if (path === "/search" || path === "/search/") tryPaths.push("/tabs/search.html", "/search/index.html");
      for (const p of tryPaths) {
        try {
          const r = await env.ASSETS.fetch(new Request(new URL(p, url.origin), req));
          if (r.status !== 404) return r;
        } catch(e){}
      }
      try {
        const home = await env.ASSETS.fetch(new Request(new URL("/index.html", url.origin), req));
        if (home.status !== 404) return home;
      } catch(e){}
    }
    if (env.ASSETS) return env.ASSETS.fetch(req);
    return new Response("not found", {status:404});
  }
};
