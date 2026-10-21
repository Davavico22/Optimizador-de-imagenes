
import os
import subprocess
import tempfile
from pathlib import Path
from PIL import Image, ImageOps

# ============== CONFIGURACIÓN ==============

CARPETA_ENTRADA = Path("imagenes_originales")
CARPETA_SALIDA = Path("imagenes_webp")

RUTINA_CWEBP = "libwebp-1.6.0-windows-x64/bin/cwebp.exe"

# Límite de tamaño: 1 MB decimal
PESO_MAXIMO = 1_000_000

# Resolución máxima inicial
ANCHO_MAXIMO = 1920
ALTO_MAXIMO = 1920

# Calidades a probar, de mayor a menor
CALIDADES = [85, 80, 75, 70, 65, 60, 55]

# Reducciones de resolución si sigue pesando demasiado
FACTORES_ESCALA = [1.0, 0.85, 0.70, 0.55, 0.40, 0.25]

EXTENSIONES = {".jpg", ".jpeg", ".png"}

# ===========================================


def peso_mb(ruta):
    return os.path.getsize(ruta) / 1_000_000


def convertir_webp(entrada, salida, calidad):
    comando = [
        RUTINA_CWEBP,
        "-q", str(calidad),
        "-m", "6",
        "-af",
        "-mt",
        "-alpha_filter", "best",
        "-quiet",
        str(entrada),
        "-o", str(salida)
    ]

    resultado = subprocess.run(
        comando,
        capture_output=True,
        text=True
    )

    if resultado.returncode != 0:
        raise RuntimeError(resultado.stderr.strip())


def optimizar_imagen(ruta_entrada, ruta_salida):
    peso_original = peso_mb(ruta_entrada)

    try:
        with Image.open(ruta_entrada) as original:
            imagen = ImageOps.exif_transpose(original)

            # Preservar transparencia cuando exista
            if imagen.mode in ("RGBA", "LA") or (
                imagen.mode == "P" and "transparency" in imagen.info
            ):
                imagen = imagen.convert("RGBA")
            else:
                imagen = imagen.convert("RGB")

            # Limitar la resolución inicial
            imagen.thumbnail(
                (ANCHO_MAXIMO, ALTO_MAXIMO),
                Image.Resampling.LANCZOS
            )

            base = imagen.copy()

        with tempfile.TemporaryDirectory() as temporal:
            temporal = Path(temporal)
            ruta_temporal = temporal / "temporal.png"

            for factor in FACTORES_ESCALA:
                ancho = max(1, int(base.width * factor))
                alto = max(1, int(base.height * factor))

                reducida = base.resize(
                    (ancho, alto),
                    Image.Resampling.LANCZOS
                )

                reducida.save(ruta_temporal, format="PNG")

                for calidad in CALIDADES:
                    convertir_webp(
                        ruta_temporal,
                        ruta_salida,
                        calidad
                    )

                    peso_final = os.path.getsize(ruta_salida)

                    if peso_final < PESO_MAXIMO:
                        reduccion = (
                            1 - peso_final /
                            os.path.getsize(ruta_entrada)
                        ) * 100

                        print(
                            f"✅ {ruta_entrada.name}\n"
                            f"   Original: {peso_original:.2f} MB\n"
                            f"   WebP: {peso_mb(ruta_salida):.2f} MB\n"
                            f"   Resolución: {ancho}x{alto}\n"
                            f"   Calidad: {calidad}\n"
                            f"   Reducción: {reduccion:.1f}%\n"
                        )
                        return True

        # No se ha conseguido el peso objetivo
        if ruta_salida.exists():
            ruta_salida.unlink()

        print(
            f"⚠️ No se consiguió bajar de 1 MB: "
            f"{ruta_entrada.name}"
        )
        return False

    except Exception as e:
        if ruta_salida.exists():
            ruta_salida.unlink()

        print(f"❌ Error en {ruta_entrada.name}: {e}")
        return False


def procesar_carpeta():
    if not CARPETA_ENTRADA.exists():
        print("❌ No existe la carpeta de entrada.")
        return

    CARPETA_SALIDA.mkdir(parents=True, exist_ok=True)

    imagenes = sorted(
        ruta for ruta in CARPETA_ENTRADA.iterdir()
        if ruta.is_file()
        and ruta.suffix.lower() in EXTENSIONES
    )

    correctas = 0

    for ruta in imagenes:
        salida = CARPETA_SALIDA / (ruta.stem + ".webp")

        if optimizar_imagen(ruta, salida):
            correctas += 1

    print("\n====== RESUMEN ======")
    print(f"Imágenes encontradas: {len(imagenes)}")
    print(f"Optimizadas: {correctas}")
    print(f"Fallidas: {len(imagenes) - correctas}")


if __name__ == "__main__":
    procesar_carpeta()
