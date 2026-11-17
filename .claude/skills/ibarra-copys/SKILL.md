---
name: ibarra-copys
description: Escribe los copys de publicación (un solo texto para Facebook e Instagram, con emojis y 5 hashtags) para las imágenes ya creadas de Jabones Ibarra y Caricia en contenido-creado/AAAA-MM/, viendo cada imagen final, y los guarda en copys/AAAA-MM.md. Usar siempre que pidan copys, textos de publicación, captions o descripciones para las imágenes ya generadas de Ibarra o Caricia.
---

# Copys para las imágenes de Jabones Ibarra y Caricia

Lee las imágenes finales de un mes y escribe **un copy por publicación**, el mismo para Facebook e Instagram, con emojis y exactamente 5 hashtags. Todo se guarda en **un solo archivo por mes**: `copys/AAAA-MM.md`.

Las rutas son relativas a la raíz del proyecto (la carpeta que contiene `contenido-creado/`, `copys/` y `references/`).

Esta skill NO modifica `contenido-creado/`. Los `copy.md` existentes solo sirven de contexto; el texto nace de lo que se ve en la imagen.

## Antes de empezar

Lee completos:

- `contenido-creado/AAAA-MM/calendario.md`: grupo, gancho, nivel de marca, producto, tienda y fecha cruzada de cada día, más las validaciones del mes.
- `.claude/skills/ibarra-contenido/references/voz-y-territorios.md`: voz y palabras prohibidas.
- `.claude/skills/ibarra-contenido/references/catalogo.md`: claims permitidos.
- `.claude/skills/ibarra-contenido/references/tiendas-promos.md`: tiendas, vigencias y mecánicas.
- `.claude/skills/ibarra-contenido/references/ejemplos.md`: piezas planas vs. con gancho.

## Flujo

### 1. Determinar el mes

- Si piden un mes, úsalo.
- Si no, toma el más reciente de `contenido-creado/` que no tenga `copys/AAAA-MM.md`.
- Si el archivo ya existe, pregunta antes de sobrescribir; ofrece regenerar solo días concretos.
- Si piden solo algunos días, escribe esos y actualiza su sección sin tocar las demás.

### 2. Ver cada imagen

Recorre las carpetas `AAAA-MM-DD_slug/` en orden cronológico. Por cada una:

- Abre la imagen con Read. Prefiere `imagen-logo.png`. En carruseles abre todas las `lamina-NN-logo.png`.
- Si no existe la versión `-logo`, usa la que haya (`imagen.png` / `lamina-NN.png`) y anótalo en el resumen final.
- Si la carpeta no tiene imagen, sáltala y repórtala.
- Lee el texto impreso en la imagen y observa escena, producto y tienda. El copy **complementa** la imagen: no copia su texto, lo continúa, lo amplía o lo remata.
- Toma del calendario: grupo, gancho, nivel de marca, producto/tienda y fecha cruzada.

### 3. Escribir el copy

- **Primera línea = gancho.** Nada de nombre de producto, tienda o precio al inicio, salvo en promociones.
- Tuteo mexicano, cálido, concreto, frases cortas, que se pueda leer en voz alta. Humor que se ríe con la gente, nunca de ella.
- **Emojis:** de 1 a 4, bien puestos y distintos a los de los días vecinos; sin cadenas de emojis.
- **CTA:** una invitación a comentar, guardar o compartir. "Compra" solo en piezas Comerciales.
- **Hashtags: exactamente 5**, al final en una línea. El primero es `#JabonesIbarra` (o `#Caricia` si la pieza es de Caricia); los otros 4 son temáticos y de la situación, no genéricos.
- Carrusel: un solo copy para toda la publicación. Puede invitar a deslizar si encaja.
- Largo: de 2 a 6 líneas cortas. Más breve en Personas, algo más informativo en Útil y Comercial.

### 4. Reglas que no se rompen

**Claims**
- Solo los de `catalogo.md`. No inventes beneficios, datos, estadísticas, testimonios ni anécdotas de la empresa. De la empresa solo se sabe: más de 90 años y origen en Cocula, Jalisco.
- Si el copy menciona: dermatológico, antibacterial, desinfectante, hipoalergénico, antioxidante, astringente, exfoliante o eliminación/reducción de microorganismos, agrega la nota `⚠ Validar con Calidad`.
- Nunca "ayuda a la cicatrización de heridas" ni "antimicrobiano".
- Personas: sin claims, sin producto, sin tienda, sin llamado a comprar.

**Precios y disponibilidad**
- Precios solo en promociones y solo dentro de una vigencia de `tiendas-promos.md`.
- Toda pieza que mencione tienda lleva debajo: *Disponibilidad, presentación y empaque sujetos a existencia, región y sucursal.*
- Las promociones agregan además vigencia y *Aplica en tiendas participantes.*
- Los productos por tienda salen solo de `tiendas-promos.md`.

**Fechas**
- Fechas religiosas, cívicas o de duelo: sin precio, sin producto y sin llamado a comprar.
- Buen Fin: no mencionar ofertas ni descuentos sin confirmación de Ventas.

**Personas**
- Niñas y niños nunca sin ropa ni en el baño o la tina. Las tareas de casa no son solo de mamá.
- Sin culpa ni comentarios sobre cómo se ve o huele alguien.

**Palabras prohibidas:** "la mejor opción", "calidad que se nota", "lleva tu", "no te quedes sin", "aprovecha", "descubre", "ideal para toda la familia", "más que un jabón", "cuida a los que más quieres". Sin comparaciones con otras marcas, jabón líquido o detergentes.

**Coherencia:** si lo que dice la imagen contradice el calendario o los claims (producto distinto, texto con error, tienda equivocada), escribe el copy más seguro y marca `⚠ Validar: …` con el detalle.

### 5. Revisar

Pieza por pieza, reescribe si falla alguna pregunta:

- ¿Alguien lo compartiría o lo guardaría?
- ¿Se entiende sin ver el logo?
- ¿Lo podría publicar cualquier otra marca? Si sí, le falta identidad.
- ¿Suena a anuncio en la primera línea?
- ¿Tiene exactamente 5 hashtags y al menos un emoji?

Luego lee el mes en orden: no repitas primeras líneas, estructura ni combinación de emojis en días consecutivos. Si dos copys se sienten iguales, cambia uno.

### 6. Guardar

Escribe `copys/AAAA-MM.md` (crea la carpeta `copys/` si no existe) con este formato:

```markdown
# Copys AAAA-MM · Jabones Ibarra y Caricia

## Día 01 · Título del calendario · AAAA-MM-DD
**Imagen:** imagen-logo.png
**Tipo:** Personas · Solo logo

```
Texto del copy, listo para copiar y pegar,
con emojis 🧺 y frases cortas.

#JabonesIbarra #Tag2 #Tag3 #Tag4 #Tag5

Leyenda de tienda/vigencia (solo si menciona tienda o es promoción)
```

> ⚠ Validar: …          (solo si hay algo pendiente, FUERA del bloque)

---
```

**Bloque de código obligatorio:** el copy, los 5 hashtags y la leyenda (disponibilidad, y vigencia/"Aplica en tiendas participantes." en promos) van juntos dentro de un bloque de código con triple acento grave, para que el visor muestre el botón de copiar y se conserven saltos de línea y emojis. Dentro del bloque va solo lo que se publica. Las notas `⚠ Validar`, la imagen y el tipo van fuera, nunca dentro. La leyenda va como texto plano dentro del bloque, sin `>`.

Para carruseles, en **Imagen** lista las láminas (`lamina-01-logo.png … lamina-04-logo.png`).

Al final del archivo agrega la sección `## Validaciones pendientes` con la lista consolidada por día.

Termina en el chat con un resumen corto: días escritos, días sin imagen o sin versión con logo, y validaciones pendientes. No pegues los 30 copys en el chat.
