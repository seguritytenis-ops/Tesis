// Storefront worker: static assets + order notifications API.
const WA = "573169486100";
function esc(s){return String(s==null?"":s).slice(0,200);}
export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    const path = url.pathname;
    if (req.method === "POST" && path === "/api/order") {
      try {
        const d = await req.json();
        for (const k of ["name","phone","addr","city","product","mode"])
          if(typeof d[k]==="string") d[k]=d[k].slice(0,200);
        const total = Number(d.total)||0;
        const msg = `PEDIDO — $${total.toLocaleString()}\n${esc(d.product||"-")}\n${esc(d.name||"-")} | ${esc(d.phone||"-")}\n${esc(d.addr||"-")} (${esc(d.city||"-")}, ${esc(d.depto||d.departamento||"-"}) Talla:${esc(d.talla||"-")}\nModo: ${esc(d.mode)}`;
        const r = await fetch(`https://api.telegram.org/bot${env.TG_TOKEN}/sendMessage`, {
          method: "POST", headers: {"Content-Type":"application/json"},
          body: JSON.stringify({chat_id: env.TG_CHAT, text: msg})
        });
        if(!r.ok) return new Response(JSON.stringify({ok:false}),{status:502,headers:{"Content-Type":"application/json"}});
      } catch(e){ return new Response(JSON.stringify({ok:false}),{status:400,headers:{"Content-Type":"application/json"}}); }
      return new Response(JSON.stringify({ok:true, wa:WA}), {headers:{"Content-Type":"application/json"}});
    }
    if (env.ASSETS) return env.ASSETS.fetch(req);
    return new Response("not found", {status:404});
  }
};
