# Prompt para IA de diseño (pegar tal cual)
Eres diseñador front-end senior. Repo: tienda colombiana de sneakers premium con
pago contra entrega (proyecto propio). Archivos en `site/` (HTML estático),
notificaciones de pedidos en `worker/worker.js` (`/api/order` -> Telegram).
Reglas: 1) Enlaces internos relativos; fotos desde CDN. 2) Formulario de pedido
con nombre/whatsapp/departamento/ciudad/barrio/dirección/talla + métodos:
contra entrega (principal), consignación Nequi/Daviplata, crédito por whatsapp,
tarjeta/PSE (mostrar aviso de no disponible y ofrecer contra entrega).
3) Precios COP coherentes home=ficha por slug + descuentos 45/55/65%.
4) Envío $15.000 (gratis desde $200.000), whatsapp de la tienda en config.
5) Credenciales: Telegram vía secretos TG_TOKEN/TG_CHAT (nunca en cliente).
Entrega: HTML completo por archivo + checklist QA click por click.
