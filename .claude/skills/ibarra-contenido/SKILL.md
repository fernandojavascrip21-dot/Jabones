---
name: ibarra-contenido
description: Genera el contenido de redes sociales de un mes completo para Jabones Ibarra y Caricia, con copy y prompt de imagen para ChatGPT por cada día, en formato 4:5 y sin video. Evita el contenido plano o repetitivo, conecta con personas y familias (muchas piezas solo con logo), aprovecha fechas importantes y promociones de Soriana, y guarda todo en contenido-creado/. Usar siempre que pidan contenido, publicaciones, copys, prompts, calendario o parrilla para Jabones Ibarra o Caricia.
---

# Contenido mensual de Jabones Ibarra y Caricia

Cada uso genera **un mes completo**: una pieza 4:5 por cada día, cada una con `copy.md` y `prompt.md`. No se generan videos, reels, guiones ni historias 9:16.

El problema a resolver es que el contenido se volvió plano: producto + tienda + "visita tu sucursal". La marca debe sentirse como alguien que conoce la vida en casa, no como un folleto.

Todas las rutas son relativas a la raíz del proyecto (la carpeta que contiene `references/`, `logo-marca/` y `contenido-creado/`).

## Antes de empezar

Lee estos archivos completos:

- `references/catalogo.md` de la skill: productos, claims, fotos y tiendas.
- `references/tiendas-promos.md`: tiendas y vigencias de Soriana.
- `references/voz-y-territorios.md`: voz, territorios, ganchos y palabras prohibidas.
- `references/fechas.md`: fechas importantes.
- `references/formatos-visuales.md`: recetas visuales y estructura del prompt.
- `references/ejemplos.md`: piezas planas vs. piezas con gancho.
- `contenido-creado/historial.md` del proyecto (si no existe, créalo con el encabezado de la sección "Historial").

## Flujo

### 1. Determinar el mes

- Si piden un mes, úsalo.
- Si no, toma el siguiente mes calendario sin carpeta en `contenido-creado/`.
- Si la carpeta de ese mes ya existe, pregunta antes de sobrescribirla.

### 2. Marcar lo que no se mueve

En orden, fija en el calendario:

1. Vigencias de Soriana que caen en el mes, con las piezas de promoción dentro de ellas (una al inicio y otra en las últimas 48 horas).
2. Fechas importantes del mes, el mismo día o de 1 a 3 días antes.
3. Si una fecha móvil no está confirmada para ese año, búscala en la web; si no se puede confirmar, márcala como validación pendiente.

### 3. Asignar cada día

A cada día asígnale grupo, territorio, tipo de gancho, nivel de marca, formato, receta visual y, si aplica, producto y tienda. Cumple todo esto en el mes:

- **Mezcla 50/30/20:** Personas / Útil / Comercial sobre el total del mes (30 días = 15/9/6; 31 días = 16/9/6). Las fechas ocupan lugares dentro de la mezcla.
- **Territorio y gancho:** nunca el mismo en días consecutivos.
- **Receta visual:** no se repite en 3 días seguidos.
- **Producto:** no se repite en 3 días seguidos, salvo promoción activa.
- **Mes anterior:** no reutilizar primeras líneas ni ideas centrales que aparezcan en el historial.
- **Tiendas:** tocar todas las tiendas activas en el mes, también desde piezas Útil.
- **Variedad:** repartir entre tocador y lavandería, Ibarra y Caricia; no concentrarse en pocos productos.
- **Solo logo:** es el nivel por defecto de las piezas de Personas. Sin producto, sin tienda y sin llamado a comprar.

### 4. Escribir

Escribe `copy.md` y `prompt.md` de cada pieza con las plantillas de abajo. Cada idea debe salir de una situación concreta de la vida en casa, no de una característica del producto.

### 5. Revisar

Pieza por pieza, reescribe si falla alguna pregunta:

- ¿Alguien la compartiría o la guardaría?
- ¿Se entiende sin ver el logo?
- ¿Podría publicarla cualquier otra marca? Si sí, le falta identidad.
- ¿Suena a anuncio en la primera línea?

Después lee el mes completo en orden. Si dos piezas se sienten iguales, cambia una, aunque técnicamente cumpla las reglas.

### 6. Guardar

```
contenido-creado/
├── historial.md
└── AAAA-MM/
    ├── calendario.md
    └── AAAA-MM-DD_slug/
        ├── copy.md
        └── prompt.md
```

Agrega una fila por pieza al historial. Al terminar, resume en el chat: mes, mezcla lograda, fechas aprovechadas y validaciones pendientes, y recuerda que las imágenes aún necesitan el logo.

## Reglas que no se rompen

**Claims**
- Solo se usan claims de `catalogo.md`. No inventes beneficios, datos, estadísticas, testimonios ni anécdotas de la empresa.
- Agrega a validaciones "Validar con Calidad" si aparece: dermatológico, antibacterial, desinfectante, hipoalergénico, antioxidante, astringente, exfoliante o eliminación/reducción de microorganismos.
- Nunca repitas "ayuda a la cicatrización de heridas" ni "antimicrobiano", aunque aparezcan en el empaque de Caricia.
- Las piezas de Personas no llevan claims.

**Precios y disponibilidad**
- Los precios solo aparecen en piezas de promoción publicadas dentro de una vigencia de `tiendas-promos.md`.
- Toda pieza que mencione tienda lleva: "Disponibilidad, presentación y empaque sujetos a existencia, región y sucursal."
- Las piezas de promoción agregan vigencia y "Aplica en tiendas participantes."
- Los productos por tienda salen solo de `tiendas-promos.md`.

**Fechas**
- Las fechas religiosas, cívicas o de duelo nunca llevan precio, producto ni llamado a comprar.
- Una fecha solo se usa si tiene relación natural con el jabón, la casa o la familia.

**Personas**
- Nunca muestres a niñas o niños sin ropa, ni en el baño o la tina. Para hablar de bañarlos, usa manos, espuma, toalla o la escena ya vestida.
- Las tareas de casa no son solo de mamá: alterna papás, abuelos, jóvenes y distintos tipos de familia.
- Personas siempre genéricas, nunca parecidas a alguien real.

**Marca**
- Logo de Ibarra: `logo-marca/logotipo_jabones_ibarra.png`. El prompt no lo adjunta ni lo coloca: solo reserva una esquina limpia, y el logo se agrega después con otra skill.
- Caricia todavía no tiene logo separado: las piezas "solo logo" reservan el espacio para el de Ibarra, y las de Caricia usan la foto real del empaque.
- Logos de tiendas: nunca los genera la IA. El prompt deja un espacio libre y se colocan en diseño.
- Concepto rector, para usarlo con moderación: "Ibarra y Caricia, más cerca de ti."

## Plantilla de `copy.md`

```markdown
# AAAA-MM-DD · Título interno

| Campo | Valor |
|---|---|
| Grupo / territorio | |
| Gancho | |
| Nivel de marca | Solo logo / Producto integrado / Comercial |
| Formato | Imagen 4:5 / Carrusel 4:5 (n láminas) |
| Receta visual | |
| Producto / tienda | — si no aplica |
| Fecha cruzada | — si no aplica |

## Ganchos (elige uno)
1. El principal, que es el que usa la imagen
2.
3.

## Texto en la imagen
(Texto exacto. En carrusel, lámina por lámina.)

## Caption
(Con el gancho en la primera línea.)

**Facebook:** (ajuste: más conversación y contexto)
**Instagram:** (ajuste: más breve)

## CTA
(Una invitación a comentar, guardar o compartir. "Compra" solo en piezas Comerciales.)

## Hashtags
(3 a 5)

## Leyenda
(Solo si aplica.)

## Validaciones pendientes
(Qué confirmar y con quién. "Ninguna" si no hay.)
```

## Plantilla de `prompt.md`

Sigue la estructura de `references/formatos-visuales.md`.

## Plantilla de `calendario.md`

Tabla con: día, fecha cruzada, título, grupo, territorio, gancho, nivel de marca, formato, receta visual, producto/tienda. Debajo: conteo de la mezcla, fechas aprovechadas y lista consolidada de validaciones.

## Historial

Encabezado de `contenido-creado/historial.md`:

```markdown
# Historial de contenido

| Fecha | Slug | Grupo | Territorio | Gancho | Formato | Receta visual | Producto/tienda | Primera línea |
|---|---|---|---|---|---|---|---|---|
```
