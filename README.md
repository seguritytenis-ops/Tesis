# TENISI — Tienda colombiana de sneakers premium con pago contra entrega
Proyecto propio de e-commerce: catálogo de sneakers, liquidación, carrito,
checkout con pago contra entrega, FAQ, políticas y contacto. Despliegue en
Cloudflare Pages + Worker para notificaciones de pedidos por Telegram.
## Estructura
- `site/` HTML estático del storefront (home, colecciones, productos, cart, checkout, policies, search)
- `worker/` Cloudflare Worker `/api/order` → Telegram (token por secreto, nunca en cliente)
- `docs/` auditoría de links, precios y QA
## Deploy
- Pages: `wrangler pages deploy site --project-name=tenisi-total`
- Worker API: `wrangler deploy --config worker/wrangler.jsonc`
- Secretos: `TG_TOKEN`, `TG_CHAT` (wrangler secret put)
