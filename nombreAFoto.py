from PIL import Image, ImageDraw, ImageFont
import os
from glob import glob

# --- CONFIGURACIÓN DE CARPETAS ---
CARPETA_ENTRADA = "imagenes_originales"   # Coloque sus imágenes aquí
CARPETA_SALIDA = "imagenes_webp"    # Las imágenes procesadas se guardarán aquí
# Ahora incluye .webp en las extensiones compatibles
EXTENSIONES_COMPATIBLES = ('*.jpg', '*.jpeg', '*.png', '*.webp') 

# --- CONFIGURACIÓN DEL TEXTO ---
TEXTO_A_AÑADIR = "PADRE"

# Opciones de fuente:
RUTA_FUENTE = None      # Ruta a un archivo .ttf. Deje None para usar la fuente por defecto.
TAMANIO_FUENTE = 50     # Tamaño en puntos
COLOR_TEXTO = (255, 255, 255) # Blanco (RGB)
POSICION_TEXTO = 'centrado' # Posicionamiento: 'izquierda' o 'centrado'

# Ajustes de Espaciado:
PADDING_INFERIOR = 30   # Espacio en píxeles entre el texto y el borde inferior.
MARGEN_HORIZONTAL = 30  # Margen lateral (si POSICION_TEXTO es 'izquierda').
# --------------------

def obtener_fuente(font_path, font_size):
    """Carga una fuente TrueType o retorna la fuente por defecto."""
    try:
        if font_path:
            return ImageFont.truetype(font_path, font_size)
        else:
            return ImageFont.load_default(font_size) 
    except Exception as e:
        print(f"Advertencia: No se pudo cargar la fuente '{font_path}'. Usando fuente por defecto. Error: {e}")
        return ImageFont.load_default(font_size)

def añadir_texto_a_imagen(ruta_entrada, ruta_salida):
    """Procesa una sola imagen, añade texto y la guarda."""
    try:
        img = Image.open(ruta_entrada)
        draw = ImageDraw.Draw(img)
        ancho_imagen, alto_imagen = img.size

        font = obtener_fuente(RUTA_FUENTE, TAMANIO_FUENTE)

        # Calcular el tamaño del texto
        bbox_text = draw.textbbox((0,0), TEXTO_A_AÑADIR, font=font)
        ancho_texto = bbox_text[2] - bbox_text[0]
        alto_texto = bbox_text[3] - bbox_text[1]

        # Calcular la posición Y (vertical)
        y_pos = alto_imagen - alto_texto - PADDING_INFERIOR

        # Calcular la posición X (horizontal)
        if POSICION_TEXTO == 'centrado':
            x_pos = (ancho_imagen - ancho_texto) // 2
        elif POSICION_TEXTO == 'izquierda':
            x_pos = MARGEN_HORIZONTAL
        else:
            x_pos = (ancho_imagen - ancho_texto) // 2 

        # Dibujar el texto
        draw.text((x_pos, y_pos), TEXTO_A_AÑADIR, font=font, fill=COLOR_TEXTO)
        
        # --- CLAVE PARA WEB P ---
        # Se usa img.format (ej: 'WEBP', 'JPEG', 'PNG') para guardar en el formato original.
        # Si el formato es WEBP, Pillow lo guardará como WEBP.
        formato_salida = img.format if img.format else 'JPEG' # Fallback a JPEG
        
        # Ajustes de calidad específicos para WebP/JPEG si se desea:
        if formato_salida == 'WEBP':
             # Aquí puede añadir parámetros específicos de WebP como 'quality=85'
             img.save(ruta_salida, formato_salida, quality=90) 
        elif formato_salida == 'JPEG':
             img.save(ruta_salida, formato_salida, quality=90)
        else:
             img.save(ruta_salida, formato_salida)


        print(f"✔️ Procesada: {os.path.basename(ruta_entrada)} [{formato_salida}]")

    except Exception as e:
        print(f"❌ ERROR al procesar {os.path.basename(ruta_entrada)}: {e}")

def procesar_carpeta():
    """Ejecuta el procesamiento de texto en todas las imágenes de la carpeta."""
    
    # Crear carpeta de salida si no existe
    if not os.path.exists(CARPETA_SALIDA):
        os.makedirs(CARPETA_SALIDA)
        print(f"Creada carpeta de salida: '{CARPETA_SALIDA}'")
        
    if not os.path.exists(CARPETA_ENTRADA):
        print(f"❌ ERROR: La carpeta de entrada '{CARPETA_ENTRADA}' no existe.")
        print("Cree la carpeta y coloque sus imágenes originales dentro.")
        return

    print(f"\nIniciando procesamiento de texto en '{CARPETA_ENTRADA}'...")
    
    contador = 0
    
    for ext in EXTENSIONES_COMPATIBLES:
        for ruta_entrada in glob(os.path.join(CARPETA_ENTRADA, ext)):
            
            # Generar la ruta de salida, manteniendo el nombre original
            nombre_archivo = os.path.basename(ruta_entrada)
            ruta_salida = os.path.join(CARPETA_SALIDA, nombre_archivo)
                
            añadir_texto_a_imagen(ruta_entrada, ruta_salida)
            contador += 1
            
    if contador == 0:
        print("⚠️ No se encontraron imágenes compatibles para procesar.")
        
    print(f"\n✅ Proceso completado. {contador} imágenes procesadas.")

if __name__ == "__main__":
    procesar_carpeta()