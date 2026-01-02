import os
import subprocess

# --- CONFIGURACIÓN ---
# Carpeta donde quieres procesar todo (ej: "public_html")
DIRECTORIO_TRABAJO = "C:\\xampp\\htdocs\\opoprix\\Contenido\\WEB_OPORPIX_DEFINITIVO\\WEB_OPORPIX_DEFINITIVO"

RUTINA_CWEBP = "libwebp-1.6.0-windows-x64/bin/cwebp.exe"

# Parámetros de optimización
PARAMETROS_CWEBP = [
    "-q", "80", 
    "-m", "6", 
    "-f", "60",
    "-alpha_filter", "best"
]

def procesar_y_reemplazar():
    """Recorre carpetas, convierte a WebP y elimina el original."""
    
    extensiones_a_convertir = ('.jpg', '.jpeg', '.png')
    conteo_exito = 0
    
    print(f"🚀 Iniciando optimización y REEMPLAZO en: {DIRECTORIO_TRABAJO}")

    for root, dirs, files in os.walk(DIRECTORIO_TRABAJO):
        for nombre_archivo in files:
            if nombre_archivo.lower().endswith(extensiones_a_convertir):
                
                # 1. Rutas de archivos
                ruta_original = os.path.join(root, nombre_archivo)
                nombre_sin_ext = os.path.splitext(nombre_archivo)[0]
                ruta_webp = os.path.join(root, f"{nombre_sin_ext}.webp")

                # 2. Comando cwebp
                comando = [RUTINA_CWEBP] + PARAMETROS_CWEBP + [ruta_original, "-o", ruta_webp, "-quiet"]
                
                try:
                    # Ejecutar conversión
                    subprocess.run(comando, check=True)
                    
                    # 3. ELIMINAR ORIGINAL (Solo si el WebP se creó con éxito)
                    if os.path.exists(ruta_webp):
                        os.remove(ruta_original)
                        print(f"🔄 Reemplazado: {nombre_archivo} -> {nombre_sin_ext}.webp")
                        conteo_exito += 1
                        
                except Exception as e:
                    print(f"❌ Error procesando {nombre_archivo}: {e}")

    print(f"\n✅ Proceso finalizado. Se han reemplazado {conteo_exito} imágenes.")

if __name__ == "__main__":
    # PRECAUCIÓN: Este script borra archivos. Asegúrate de tener backup.
    confirmacion = input("⚠️ Esto eliminará los archivos JPG/PNG originales. ¿Continuar? (s/n): ")
    if confirmacion.lower() == 's':
        procesar_y_reemplazar()
    else:
        print("Operación cancelada.")