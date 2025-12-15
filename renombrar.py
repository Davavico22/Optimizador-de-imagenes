import os
from typing import List

def renombrar_imagenes(directorio: str, prefijo: str = "imagen_", inicio_con: int = 1) -> None:
    """
    Renombra todos los archivos de imagen en un directorio dado.

    Las imágenes se renombran usando el formato:
    <prefijo><número>.<extension_original>

    Ejemplo: foto.jpg -> imagen_1.jpg, selfie.png -> imagen_2.png

    :param directorio: Ruta al directorio que contiene las imágenes.
    :param prefijo: El prefijo a usar para el nuevo nombre del archivo (ej. "vacaciones_").
    :param inicio_con: El número con el que se empezará a enumerar las imágenes (ej. 1).
    :return: None
    """
    # Extensiones de imagen comunes que se buscarán
    EXTENSIONES_IMAGEN = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')
    
    # 1. Obtener la lista de archivos en el directorio
    try:
        archivos: List[str] = os.listdir(directorio)
    except FileNotFoundError:
        print(f"❌ Error: El directorio '{directorio}' no existe.")
        return
    except Exception as e:
        print(f"❌ Error al acceder al directorio: {e}")
        return

    # 2. Filtrar solo los archivos que son imágenes
    imagenes_a_renombrar: List[str] = []
    for archivo in archivos:
        # Extraer el nombre base y la extensión
        nombre_base, extension = os.path.splitext(archivo)
        
        # Convertir la extensión a minúsculas para la verificación
        if extension.lower() in EXTENSIONES_IMAGEN:
            # Comprobar que realmente es un archivo (y no un subdirectorio)
            ruta_completa: str = os.path.join(directorio, archivo)
            if os.path.isfile(ruta_completa):
                imagenes_a_renombrar.append(archivo)

    # Ordenar las imágenes para asegurar un orden predecible (por ejemplo, alfabético)
    imagenes_a_renombrar.sort()
    
    if not imagenes_a_renombrar:
        print(f"ℹ️ No se encontraron imágenes con extensiones comunes en '{directorio}'.")
        return

    print(f"✅ Se encontraron {len(imagenes_a_renombrar)} imágenes para renombrar.")
    
    # 3. Renombrar las imágenes
    contador: int = inicio_con
    for nombre_antiguo in imagenes_a_renombrar:
        # Obtener la extensión original para conservarla
        extension: str = os.path.splitext(nombre_antiguo)[1]
        
        # Crear el nuevo nombre (ej: "vacaciones_1.jpg")
        nuevo_nombre: str = f"{prefijo}{contador}{extension.lower()}"
        
        # Rutas completas
        ruta_antigua: str = os.path.join(directorio, nombre_antiguo)
        ruta_nueva: str = os.path.join(directorio, nuevo_nombre)
        
        try:
            # Ejecutar el renombramiento
            os.rename(ruta_antigua, ruta_nueva)
            print(f"➡️ Renombrado: '{nombre_antiguo}' -> '{nuevo_nombre}'")
            contador += 1
        except Exception as e:
            print(f"❌ No se pudo renombrar '{nombre_antiguo}': {e}")
            
    print(f"\n✨ ¡Proceso completado! Se renombraron {contador - inicio_con} archivos.")


# --- CONFIGURACIÓN Y EJECUCIÓN ---

# ⚠️ MODIFICA ESTAS 3 LÍNEAS DE ACUERDO A TUS NECESIDADES ⚠️

# 1. Especifica la ruta al directorio donde están tus imágenes:
#    Ejemplo en Windows: r"C:\Users\TuUsuario\Desktop\MisFotos"
#    Ejemplo en Linux/macOS: "/home/tu_usuario/fotos_viaje"
RUTA_DEL_DIRECTORIO = "imagenes_originales" 

# 2. El prefijo que quieres usar para los nuevos nombres:
PREFIJO_NUEVO = "CACHORROS" 

# 3. El número con el que quieres empezar a enumerar:
INICIO_DE_ENUMERACION = 72 

# Llama a la función principal
renombrar_imagenes(RUTA_DEL_DIRECTORIO, PREFIJO_NUEVO, INICIO_DE_ENUMERACION)

# Si quieres probarlo, descomenta la línea de arriba y edita la RUTA_DEL_DIRECTORIO