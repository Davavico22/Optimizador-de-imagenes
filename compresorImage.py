import os
import subprocess
from glob import glob

# --- CONFIGURACIÓN AVANZADA (Basada en la interfaz de Squoosh/cwebp) ---
CARPETA_ENTRADA = "imagenes_originales"
CARPETA_SALIDA = "imagenes_webp"
RUTINA_CWEBP = "libwebp-1.6.0-windows-x64/bin/cwebp.exe" # Asegúrese de que 'cwebp' esté en su PATH o ponga la ruta completa

# Parámetros avanzados de cwebp:
# Nota: La sintaxis de cwebp es "-[parametro] [valor]"

# 1. Compresión (Calidad/Lossless)
#    -q 85: Calidad (0-100, para compresión Lossy). Omita esto si usa lossless=True.
#    -lossless: Activa la compresión sin pérdida. Usar solo UNO de estos dos.
PARAM_COMPRESION = "-q" 
VALUE_COMPRESION = "85" 

# 2. Esfuerzo / Preset / Método de compresión (Effort)
#    -m 6: Nivel de método de compresión (0=rápido, 6=lento, máxima compresión).
PARAM_ESFUERZO = "-m" 
VALUE_ESFUERZO = "6"

# 3. Parametros de Filtrado
#    -f 60: Fuerza del filtro (Filter strength 0-100).
#    -sharpness 0: Nitidez del filtro (Filter sharpness 0-7).
PARAM_FILTRO = "-f" 
VALUE_FILTRO = "60"
VALUE_SHARPNESS = "0"

# 4. Multiprocesamiento (Passes)
#    -pass 1: Número de pasadas/repeticiones para optimizar.
PARAM_PASADAS = "-pass" 
VALUE_PASADAS = "1"

# 5. Conversion Alpha (Para PNGs con transparencia)
#    -alpha_filter 'best': Similar a 'Alpha to quality' en Squoosh.
PARAM_ALPHA = "-alpha_filter" 
VALUE_ALPHA = "best"

# -------------------------------------------------------------------------

def ejecutar_cwebp(ruta_entrada, ruta_salida_webp):
    """Ejecuta el comando cwebp con los parámetros definidos."""
    
    # 1. Crear la cadena de comandos
    # Se añade '-quiet' para que cwebp no imprima información por cada archivo
    comando = [
        RUTINA_CWEBP,
        PARAM_COMPRESION,
        VALUE_COMPRESION,
        PARAM_ESFUERZO,
        VALUE_ESFUERZO,
        PARAM_FILTRO,
        VALUE_FILTRO,
        VALUE_SHARPNESS,
        PARAM_PASADAS,
        VALUE_PASADAS,
        PARAM_ALPHA,
        VALUE_ALPHA,
        ruta_entrada, 
        "-o", ruta_salida_webp,
        # "-quiet"
    ]
    
    # 2. Ejecutar
    try:
        # La función subprocess.run ejecuta el comando
        resultado = subprocess.run(
            comando, 
            check=True,  # Lanza un error si cwebp falla
            capture_output=True, 
            text=True
        )
        print(f"✔️ Procesada: {os.path.basename(ruta_entrada)}")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ ERROR en cwebp para {os.path.basename(ruta_entrada)}:")
        print(f"   Salida de error: {e.stderr.strip()}")
    except FileNotFoundError:
        print(f"❌ ERROR: El comando '{RUTINA_CWEBP}' no fue encontrado.")
        print("Asegúrese de instalar 'cwebp' y de que esté en su PATH.")


def procesar_carpeta():
    """Recorre la carpeta de entrada y convierte cada imagen compatible."""
    
    if not os.path.exists(CARPETA_SALIDA):
        os.makedirs(CARPETA_SALIDA)
        print(f"Creada carpeta de salida: '{CARPETA_SALIDA}'")
        
    if not os.path.exists(CARPETA_ENTRADA):
        print(f"❌ ERROR: La carpeta de entrada '{CARPETA_ENTRADA}' no existe.")
        return

    print(f"Iniciando conversión avanzada a WebP en '{CARPETA_ENTRADA}'...")
    
    # Busca todos los archivos compatibles
    extensiones_compatibles = ['*.jpg', '*.jpeg', '*.png']
    
    for ext in extensiones_compatibles:
        for ruta_entrada in glob(os.path.join(CARPETA_ENTRADA, ext)):
            
            # Generar el nombre de salida .webp
            nombre_base = os.path.splitext(os.path.basename(ruta_entrada))[0]
            ruta_salida_webp = os.path.join(CARPETA_SALIDA, f"{nombre_base}.webp")
            
            ejecutar_cwebp(ruta_entrada, ruta_salida_webp)
            
    print("\n✅ Proceso de conversión avanzada a WebP completado.")

if __name__ == "__main__":
    procesar_carpeta()