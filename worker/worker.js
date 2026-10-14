// Storefront worker: static assets + order notifications API.
// Secretos TG_TOKEN y TG_CHAT via wrangler secret (nunca en cliente).
const WA = "573169486100";
export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    if (req.method === "POST" && url.pathname === "/api/order") {
      try {
        const d = await req.json();
        const msg = `PEDIDO — $${(d.total||0).toLocaleString()}\n${d.product||"-"}\n${d.name||"-"} | ${d.phone||"-"}\n${d.addr||"-"} (${d.city||"-"}) Talla:${d.talla||"-"}\nModo: ${d.mode}`;
        await fetch(`https://api.telegram.org/bot${env.TG_TOKEN}/sendMessage`, {
          method: "POST", headers: {"Content-Type":"application/json"},
          body: JSON.stringify({chat_id: env.TG_CHAT, text: msg})
        });
      } catch(e){}
      return new Response(JSON.stringify({ok:true, wa:WA}), {headers:{"Content-Type":"application/json"}});
    }
    if (env.ASSETS) return env.ASSETS.fetch(req);
    return new Response("not found", {status:404});
  }
};
