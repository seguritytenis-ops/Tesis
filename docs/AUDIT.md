# QA checklist — links, precios, flujos
## Links
- Todos los enlaces internos usan rutas relativas. Las fotos cargan desde CDN.
- Rutas: /, /collections/*, /pages/*, /policies/*, /products/*, /cart/, /checkout/, /search/
- Los formularios de compra usan el flujo local de pedido sin recarga.
## Precios (COP, coherentes home=ficha por slug)
- Promo 55-59k base, medio 64-79k, alto 79-89k, premium 89-99k
- Descuento = 1-now/was: 45/55/65%
## QA por click
- Home → ficha (galería+tallas+formulario) → confirmar pedido → notificación
- Colecciones → ficha → checkout. Tarjeta/PSE muestra aviso temporal → COD.
