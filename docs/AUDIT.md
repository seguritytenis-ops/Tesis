# Auditoría — links, precios, QA
## Links
- Todo `tenisi.co` no-CDN debe ser relativo. CDNs de fotos se mantienen.
- Rutas: /, /collections/*, /pages/*, /policies/*, /products/*, /cart/, /checkout/, /search/
- Formularios /cart/add → interceptados, van al checkout local sin recarga.
## Precios (COP, coherentes home=ficha por slug)
- Promo 55-59k: baletas, puma base, samba base, nike osito
- Medio 64-79k: puma/samba/adidas/force/nike/dunk
- Medio-alto 79-89k: onitsuka/salomon
- Premium 89-99k: jordan/golden
- Descuento = 1 - now/was: base 45%, medio 52-58%, premium 65%
## QA por click
- Home → pídelo ya → ficha (orderForm+tallas+galería) → PAGA CONTRA ENTREGA → Telegram
- Liquidación → grid local (JS sin absolutos) → ficha → checkout
- Tarjeta/PSE → modal mantenimiento → COD
