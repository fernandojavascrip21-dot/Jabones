# Formatos y prompts de imagen

## Formato

Solo 4:5 (1080×1350 px), en imagen o carrusel. Carruseles de 3 a 6 láminas, con el mismo estilo en todas y la primera funcionando como gancho por sí sola. Las encuestas y preguntas también son 4:5. Máximo 4 carruseles por cada 10 piezas.

## Recetas visuales

| Clave | Receta | Cuándo |
|---|---|---|
| `escena` | Fotografía documental de un momento real en casa, luz natural, encuadre imperfecto | Rituales, generaciones |
| `tipografia` | Frase gigante sobre color plano; la tipografía es la imagen | Humor, preguntas |
| `objeto` | Un solo objeto cotidiano como protagonista, con mucho aire | Humor, confesiones |
| `macro` | Primer plano de textura: espuma, tela, agua, ropa al sol | Rituales, trucos |
| `recado` | Nota o recado escrito a mano, sobre el refri o la mesa | Frases de casa, tienda |
| `ilustracion` | Ilustración mexicana: papel picado, grabado, lotería | Raíz, fechas |
| `dos-opciones` | Imagen partida a la mitad con dos opciones | Encuestas, dilemas |
| `lista` | Lista del súper o ticket de compra, fotografiado de cerca | Promociones, humor |
| `pasos` | Carrusel con fotos sencillas y un paso por lámina | Trucos, guías |
| `producto-escena` | El empaque real dentro de una escena de uso | Producto en la vida |
| `mapa` | Mapa, recorrido o señalización como idea central | Dónde encontrarnos |

## Paleta

- **Ibarra:** rojo y azul marino, con blanco. En piezas emotivas, permite tonos de la escena (sol, madera, tela), usando el rojo y el azul solo como acento.
- **Caricia:** azul marino, azul cielo y blanco; verde en Antibacterial y Dermatológico.
- No todas las piezas deben parecer un anuncio de jabón: nada de burbujas y agua azul por defecto.

## Reglas para la imagen

- **Logo:** nunca se adjunta ni se pide colocarlo, porque ChatGPT lo redibuja. Cada prompt reserva una esquina limpia, con fondo liso o de poco detalle, sin texto ni objetos importantes y sin recuadro visible. El logo real se coloca después con otra skill. En carruseles, la zona se reserva en cada lámina.
- **Empaque:** siempre se adjunta la foto real de `catalogo.md`, y se pide conservar diseño, colores y texto idénticos. Los empaques de fondo blanco deben verse blanco neutro, como Ibarra Neutro: algunas fotos, como la de Granada, tienen un tono crema que no debe reproducirse. Si no hay foto, la pieza no muestra el empaque.
- **Barra sin empaque:** si la escena la muestra, se adjunta la foto de `catalogo.md` y se pide conservar su forma y grabado, mostrándola de color blanco aunque en la foto se vea marfil.
- **Tiendas:** el prompt reserva otra zona limpia, igual que la del logo y sin recuadro, en el lado contrario para que no se encimen. Sus logos se colocan en diseño y requieren permiso de uso.
- **Zonas reservadas:** son parte natural de la escena, con su mismo fondo. Nunca son recuadros, manchas blancas ni parches de color.
- **Texto:** máximo unas 15 palabras en la imagen, salvo en carruseles. Se pide escribir el texto exacto, con acentos, y sin agregar nada más.
- **Personas:** ver las reglas de la skill. Sin niñas o niños sin ropa o en el baño.

## Estructura de `prompt.md`

```markdown
# AAAA-MM-DD · Título interno

## Adjuntar en ChatGPT
- (foto del producto; si no aplica, escribe "Ninguno")

## Prompt
Crea una imagen vertical en formato 4:5 (1080×1350 px) para redes sociales de una marca mexicana de jabones.

Concepto: (la idea en una frase)
Escena: (qué se ve, con detalles concretos de un hogar mexicano)
Estilo: (receta visual, luz, cámara o técnica)
Paleta: (colores)
Composición: (dónde va cada cosa, dejando espacio para el texto)

Texto exacto en la imagen, con estos acentos y sin agregar otras palabras:
"(texto)"

Zona reservada: deja la esquina (…) limpia, con el mismo fondo de la escena y poco detalle, sin texto ni objetos importantes, porque ahí se colocará el logo después. La escena debe continuar de forma natural en esa zona: no dibujes recuadros, manchas ni parches, y no escribas nada ahí. No agregues logos ni nombres de marca a la imagen (si hay producto: "salvo los del empaque o la barra adjuntos").
(Si hay producto) Empaque: usa la foto adjunta y conserva idénticos su diseño, colores y texto. Si el fondo del empaque es blanco o crema, muéstralo blanco neutro, sin tono crema ni amarillento, aunque la luz de la escena sea cálida; todos los empaques blancos deben verse igual de blancos.
(Si hay tienda) Zona reservada de la tienda: deja (lado contrario a la zona del logo) limpio, con el mismo fondo de la escena y poco detalle, porque ahí se colocará después el logo de la tienda. Tampoco dibujes un recuadro ahí; no escribas ni dibujes logos de tiendas.

Evita: burbujas decorativas, apariencia de banco de imágenes, texto adicional, marcas de agua, recuadros en blanco, logos o nombres de marca fuera del empaque adjunto.

## Carrusel (solo si aplica)
Lámina por lámina: escena y texto exacto. Pide generar una imagen a la vez, manteniendo el estilo de la primera.

## Revisar al recibir la imagen
- Formato 4:5, texto exacto, y zonas reservadas limpias, sin recuadros, logos ni marcas agregados.
- (Si hay producto) Empaque idéntico al original y, si es blanco, sin tono crema ni amarillento.
```
