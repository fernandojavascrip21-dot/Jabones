#!/usr/bin/env python3
"""
reparar_orillas.py — Quita la línea oscura del borde en PNG transparentes YA generados.

No vuelve a calcular la máscara ni necesita rembg: solo repinta la orilla del producto
con el color del interior. Sirve para arreglar las fotos que ya sacaste.

Instalación:
    pip3 install pillow numpy

Uso:
    python3 reparar_orillas.py "carpeta/sin_fondo"
    python3 reparar_orillas.py "carpeta/sin_fondo" --banda 10 --encoger 2
    python3 reparar_orillas.py foto_sinfondo.png --revisar     # guarda un zoom antes/después
"""

import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter


def _erosionar(binaria, pasos):
    im = Image.fromarray((binaria * 255).astype(np.uint8), "L")
    for _ in range(pasos):
        im = im.filter(ImageFilter.MinFilter(3))
    return np.asarray(im) > 127


def reparar(imagen_rgba, banda, encoger, suavizar):
    rgb = imagen_rgba.convert("RGB")
    mascara = imagen_rgba.getchannel("A")

    alfa = np.asarray(mascara, dtype=np.uint8)
    solido = alfa >= 250
    if not solido.any():
        return imagen_rgba

    ys, xs = np.where(alfa > 0)
    m = banda + 4
    y0, y1 = max(0, ys.min() - m), min(alfa.shape[0], ys.max() + m + 1)
    x0, x1 = max(0, xs.min() - m), min(alfa.shape[1], xs.max() + m + 1)

    trozo = np.asarray(rgb, dtype=np.float32)[y0:y1, x0:x1].copy()
    nucleo = _erosionar(solido[y0:y1, x0:x1], banda)
    if not nucleo.any():
        return imagen_rgba

    conocido = nucleo.copy()
    trozo[~conocido] = 0.0

    for _ in range(banda + 2):
        suma = np.zeros_like(trozo)
        cuenta = np.zeros(trozo.shape[:2], np.float32)
        for eje, giro in ((0, 1), (0, -1), (1, 1), (1, -1)):
            suma += np.roll(trozo, giro, eje)
            cuenta += np.roll(conocido, giro, eje).astype(np.float32)
        nuevos = (~conocido) & (cuenta > 0)
        if not nuevos.any():
            break
        trozo[nuevos] = suma[nuevos] / cuenta[nuevos][:, None]
        conocido |= nuevos

    plano = np.asarray(rgb).copy()
    plano[y0:y1, x0:x1] = np.clip(trozo, 0, 255).astype(np.uint8)

    nueva = mascara
    for _ in range(max(0, encoger)):
        nueva = nueva.filter(ImageFilter.MinFilter(3))
    if suavizar > 0:
        nueva = nueva.filter(ImageFilter.GaussianBlur(suavizar))

    salida = Image.fromarray(plano, "RGB").convert("RGBA")
    salida.putalpha(nueva)
    return salida


def zoom_comparacion(antes, despues, destino):
    """Pega el mismo trozo del borde superior antes y después, sobre blanco, x3."""
    alfa = np.asarray(antes.getchannel("A"))
    ys, xs = np.where(alfa > 10)
    cx, cy = (xs.min() + xs.max()) // 2, ys.min()
    caja = (max(0, cx - 200), max(0, cy - 30), min(antes.width, cx + 200), min(antes.height, cy + 100))

    tiras = []
    for im in (antes, despues):
        fondo = Image.new("RGBA", im.size, (255, 255, 255, 255))
        plano = Image.alpha_composite(fondo, im).convert("RGB").crop(caja)
        tiras.append(plano.resize((plano.width * 3, plano.height * 3), Image.NEAREST))

    lienzo = Image.new("RGB", (tiras[0].width, tiras[0].height * 2 + 10), (200, 200, 200))
    lienzo.paste(tiras[0], (0, 0))
    lienzo.paste(tiras[1], (0, tiras[0].height + 10))
    lienzo.save(destino, "PNG")


def main():
    p = argparse.ArgumentParser(description="Quita la línea oscura del borde en PNG transparentes.")
    p.add_argument("entrada", help="Archivo PNG o carpeta con PNG transparentes")
    p.add_argument("-o", "--salida", default=None, help="Carpeta de salida (def: limpias)")
    p.add_argument("--banda", type=int, default=6,
                   help="Píxeles de orilla que se repintan con el color del interior (def: 6)")
    p.add_argument("--encoger", type=int, default=2,
                   help="Píxeles a recortar de la silueta (def: 2)")
    p.add_argument("--suavizar", type=float, default=0.8, help="Difuminado del borde (def: 0.8)")
    p.add_argument("--sufijo", default="_limpio", help="Sufijo del archivo de salida")
    p.add_argument("--revisar", action="store_true", help="Guarda un zoom antes/después")
    args = p.parse_args()

    entrada = Path(args.entrada).expanduser()
    if not entrada.exists():
        print(f"No existe: {entrada}")
        return 1

    if entrada.is_dir():
        archivos = sorted(f for f in entrada.glob("*.png")
                          if args.sufijo not in f.stem and "_zoom" not in f.stem)
        base = entrada
    else:
        archivos, base = [entrada], entrada.parent

    if not archivos:
        print("No se encontraron PNG.")
        return 1

    carpeta = Path(args.salida).expanduser() if args.salida else base / "limpias"
    carpeta.mkdir(parents=True, exist_ok=True)
    print(f"banda={args.banda} encoger={args.encoger} | {len(archivos)} archivo(s)\n")

    errores = 0
    for i, archivo in enumerate(archivos, 1):
        try:
            antes = Image.open(archivo).convert("RGBA")
            despues = reparar(antes, args.banda, args.encoger, args.suavizar)
            destino = carpeta / f"{archivo.stem}{args.sufijo}.png"
            despues.save(destino, "PNG", optimize=True)
            if args.revisar:
                zoom_comparacion(antes, despues, carpeta / f"{archivo.stem}_zoom.png")
            print(f"[{i}/{len(archivos)}] OK  {archivo.name} -> {destino.name}")
        except Exception as e:
            errores += 1
            print(f"[{i}/{len(archivos)}] ERROR en {archivo.name}: {e}")

    print(f"\nListo en: {carpeta.resolve()}")
    return 0 if errores == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
