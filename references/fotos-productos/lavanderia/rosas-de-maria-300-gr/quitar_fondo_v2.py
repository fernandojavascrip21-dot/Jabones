#!/usr/bin/env python3
"""
quitar_fondo.py  (v2) — Quita el fondo y guarda PNG transparente sin comerse el producto.

Instalación:
    pip3 install rembg pillow onnxruntime numpy
    pip3 install pillow-heif        # opcional, para .HEIC de iPhone

Uso básico:
    python3 quitar_fondo.py "ruta/de/las/fotos"

Si TODAVÍA te corta partes del producto:
    python3 quitar_fondo.py "ruta" --crecer 3            # amplía el recorte
    python3 quitar_fondo.py "ruta" --umbral 60           # acepta bordes más dudosos
    python3 quitar_fondo.py "ruta" -m birefnet-general   # modelo más preciso (más lento)
    python3 quitar_fondo.py "ruta" --mascara             # guarda la máscara para revisar

Si deja fondo o halo de sobra:
    python3 quitar_fondo.py "ruta" --crecer -2 --umbral 160
"""

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageOps
from rembg import new_session, remove

try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
except ImportError:
    pass

Image.MAX_IMAGE_PIXELS = None

EXTENSIONES = {
    ".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff",
    ".gif", ".heic", ".heif", ".jfif", ".ppm", ".avif",
}

COLORES = {
    "blanco": (255, 255, 255), "negro": (0, 0, 0), "gris": (240, 240, 240),
    "beige": (245, 240, 232), "crema": (250, 246, 238),
}


# ---------------------------------------------------------------- máscara ---

def obtener_mascara(imagen, session, matting, lado_modelo):
    """Devuelve la máscara (modo L) del objeto, al tamaño original de la imagen."""
    chica = imagen.copy()
    chica.thumbnail((lado_modelo, lado_modelo), Image.LANCZOS)

    if matting:
        recorte = remove(
            chica, session=session, alpha_matting=True,
            alpha_matting_foreground_threshold=230,
            alpha_matting_background_threshold=20,
            alpha_matting_erode_size=3,
        ).convert("RGBA")
        mascara = recorte.getchannel("A")
    else:
        mascara = remove(chica, session=session, only_mask=True,
                         post_process_mask=True).convert("L")

    return mascara.resize(imagen.size, Image.LANCZOS)


def rellenar_huecos(mascara, umbral):
    """Vuelve opaco todo agujero interno (letras, brillos, centros oscuros)."""
    binaria = mascara.point(lambda p: 255 if p >= umbral else 0).convert("L")
    ancho, alto = binaria.size
    marcada = binaria.copy()
    pixeles = marcada.load()

    bordes = (
        [(x, 0) for x in range(ancho)] + [(x, alto - 1) for x in range(ancho)] +
        [(0, y) for y in range(alto)] + [(ancho - 1, y) for y in range(alto)]
    )
    for punto in bordes:
        if pixeles[punto] == 0:
            ImageDraw.floodfill(marcada, punto, 128)

    # Lo que sigue en 0 quedó encerrado -> era un hueco, se rellena
    huecos = marcada.point(lambda p: 255 if p == 0 else 0)
    return ImageChops.lighter(mascara, huecos)


def limpiar_islas(mascara, umbral, pct):
    """Borra manchas sueltas (fondo residual) que no alcancen pct% del objeto mayor."""
    from collections import deque

    chica = mascara.copy()
    chica.thumbnail((700, 700), Image.NEAREST)
    binaria = chica.point(lambda p: 255 if p >= umbral else 0).convert("L")
    ancho, alto = binaria.size
    px = list(binaria.getdata())
    visto = bytearray(ancho * alto)
    grupos = []

    for inicio in range(ancho * alto):
        if px[inicio] and not visto[inicio]:
            cola = deque([inicio])
            visto[inicio] = 1
            celdas = [inicio]
            while cola:
                c = cola.popleft()
                x, y = c % ancho, c // ancho
                for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                    if 0 <= nx < ancho and 0 <= ny < alto:
                        n = ny * ancho + nx
                        if px[n] and not visto[n]:
                            visto[n] = 1
                            cola.append(n)
                            celdas.append(n)
            grupos.append(celdas)

    if not grupos:
        return mascara

    minimo = max(len(g) for g in grupos) * pct / 100.0
    conservar = bytearray(ancho * alto)
    for grupo in grupos:
        if len(grupo) >= minimo:
            for i in grupo:
                conservar[i] = 255

    guia = Image.frombytes("L", (ancho, alto), bytes(conservar))
    guia = guia.filter(ImageFilter.MaxFilter(5))          # margen por la reducción
    guia = guia.resize(mascara.size, Image.LANCZOS).point(lambda p: 255 if p >= 100 else 0)
    return ImageChops.multiply(mascara, guia)


def ajustar_mascara(mascara, umbral, crecer, suavizar, rellenar, limpiar=5):
    """Limpia y ajusta la máscara: islas, relleno, curva de umbral, crecer/encoger, difuminado."""
    if limpiar > 0:
        mascara = limpiar_islas(mascara, umbral, limpiar)

    if rellenar:
        mascara = rellenar_huecos(mascara, umbral)

    # Curva: lo claramente objeto a 255, lo claramente fondo a 0, el resto en rampa
    bajo, alto = max(0, umbral - 40), min(255, umbral + 40)
    rango = max(1, alto - bajo)
    mascara = mascara.point(
        lambda p: 0 if p <= bajo else (255 if p >= alto else int((p - bajo) * 255 / rango))
    )

    if crecer:
        pasos = min(abs(crecer), 25)
        filtro = ImageFilter.MaxFilter(3) if crecer > 0 else ImageFilter.MinFilter(3)
        for _ in range(pasos):
            mascara = mascara.filter(filtro)

    if suavizar > 0:
        mascara = mascara.filter(ImageFilter.GaussianBlur(suavizar))

    return mascara


# ---------------------------------------------------------------- proceso ---

def procesar(ruta, carpeta_salida, session, args):
    imagen = Image.open(ruta)
    imagen = ImageOps.exif_transpose(imagen)      # respeta la rotación del iPhone
    imagen = imagen.convert("RGB")

    if args.max_lado:
        imagen.thumbnail((args.max_lado, args.max_lado), Image.LANCZOS)

    mascara = obtener_mascara(imagen, session, args.matting, args.lado_modelo)
    mascara = ajustar_mascara(mascara, args.umbral, args.crecer,
                              args.suavizar, not args.sin_relleno, args.limpiar)

    resultado = imagen.convert("RGBA")
    resultado.putalpha(mascara)

    if args.recortar:
        caja = resultado.getbbox()
        if caja:
            if args.margen:
                x0, y0, x1, y1 = caja
                m = args.margen
                caja = (max(0, x0 - m), max(0, y0 - m),
                        min(resultado.width, x1 + m), min(resultado.height, y1 + m))
            resultado = resultado.crop(caja)

    if args.fondo:
        color = COLORES.get(args.fondo.lower())
        if color is None:
            hexa = args.fondo.lstrip("#")
            color = tuple(int(hexa[i:i + 2], 16) for i in (0, 2, 4))
        lienzo = Image.new("RGBA", resultado.size, color + (255,))
        resultado = Image.alpha_composite(lienzo, resultado)

    carpeta_salida.mkdir(parents=True, exist_ok=True)
    salida = carpeta_salida / f"{ruta.stem}{args.sufijo}.png"
    resultado.save(salida, "PNG", optimize=True)

    if args.mascara:
        mascara.save(carpeta_salida / f"{ruta.stem}_mascara.png", "PNG")

    return salida


def main():
    p = argparse.ArgumentParser(
        description="Quita el fondo de imágenes y las guarda como PNG transparente.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Consejo: si te corta el producto, sube --crecer y baja --umbral.",
    )
    p.add_argument("entrada", help="Archivo o carpeta con las imágenes")
    p.add_argument("-o", "--salida", default=None, help="Carpeta de salida (def: sin_fondo)")
    p.add_argument("-m", "--modelo", default=None,
                   help="isnet-general-use (def) | birefnet-general (mejor) | u2net | u2netp")

    p.add_argument("--seguro", action="store_true",
                   help="MODO SEGURO: no corta el producto. Mejor modelo, umbral bajo, "
                        "recorte expandido, sin limpieza de islas. Más lento")

    p.add_argument("--umbral", type=int, default=None,
                   help="0-255. Más bajo = conserva más producto (normal: 110, seguro: 40)")
    p.add_argument("--crecer", type=int, default=None,
                   help="Píxeles a expandir (+) o encoger (-) el recorte (normal: 1, seguro: 3)")
    p.add_argument("--suavizar", type=float, default=None,
                   help="Difuminado del borde en píxeles (normal: 0.8, seguro: 0.5)")
    p.add_argument("--limpiar", type=int, default=None,
                   help="Borra manchas sueltas menores a N%% del objeto mayor "
                        "(normal: 5, seguro: 0 = no limpia nada)")
    p.add_argument("--sin-relleno", action="store_true",
                   help="No rellenar huecos internos (si el producto tiene agujeros reales)")
    p.add_argument("--matting", action="store_true",
                   help="Modo pelo/transparencias. Preciso, pero puede comer bordes")

    p.add_argument("--recortar", action="store_true", help="Recorta el sobrante transparente")
    p.add_argument("--margen", type=int, default=0, help="Margen al recortar, en píxeles")
    p.add_argument("--fondo", default=None, help="Color de fondo: blanco, negro, gris o #RRGGBB")
    p.add_argument("--max-lado", type=int, default=0,
                   help="Reduce la salida a N px de lado mayor (0 = tamaño original)")
    p.add_argument("--lado-modelo", type=int, default=None,
                   help="Resolución de análisis (normal: 1600, seguro: 2048)")

    p.add_argument("--sufijo", default="_sinfondo", help="Sufijo del archivo de salida")
    p.add_argument("--mascara", action="store_true", help="Guarda también la máscara para revisar")
    p.add_argument("--recursivo", action="store_true", help="Incluye subcarpetas")
    args = p.parse_args()

    # Presets: lo que el usuario NO escribió a mano se llena según el modo
    NORMAL = {"modelo": "isnet-general-use", "umbral": 110, "crecer": 1,
              "suavizar": 0.8, "limpiar": 5, "lado_modelo": 1600}
    SEGURO = {"modelo": "birefnet-general", "umbral": 40, "crecer": 3,
              "suavizar": 0.5, "limpiar": 0, "lado_modelo": 2048}
    preset = SEGURO if args.seguro else NORMAL
    for clave, valor in preset.items():
        if getattr(args, clave) is None:
            setattr(args, clave, valor)

    entrada = Path(args.entrada).expanduser()
    if not entrada.exists():
        print(f"No existe: {entrada}")
        return 1

    if entrada.is_dir():
        patron = "**/*" if args.recursivo else "*"
        archivos = sorted(
            f for f in entrada.glob(patron)
            if f.is_file() and f.suffix.lower() in EXTENSIONES
            and args.sufijo not in f.stem and "_mascara" not in f.stem
        )
        base = entrada
    else:
        archivos, base = [entrada], entrada.parent

    if not archivos:
        print("No se encontraron imágenes compatibles.")
        return 1

    carpeta_salida = Path(args.salida).expanduser() if args.salida else base / "sin_fondo"

    print(f"Modo: {'SEGURO' if args.seguro else 'normal'} | Modelo: {args.modelo} | "
          f"umbral={args.umbral} crecer={args.crecer} limpiar={args.limpiar} "
          f"| {len(archivos)} imagen(es)\n")
    session = new_session(args.modelo)

    errores = 0
    for i, archivo in enumerate(archivos, 1):
        try:
            salida = procesar(archivo, carpeta_salida, session, args)
            print(f"[{i}/{len(archivos)}] OK  {archivo.name} -> {salida.name}")
        except Exception as e:
            errores += 1
            print(f"[{i}/{len(archivos)}] ERROR en {archivo.name}: {e}")

    print(f"\nListo. {len(archivos) - errores} de {len(archivos)} en: {carpeta_salida.resolve()}")
    return 0 if errores == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
