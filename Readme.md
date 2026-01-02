# 📂 Manual de Gestión Web y Kit de Optimización de Imágenes

Este documento centraliza las instrucciones para la clonación de sitios web, configuración de Git y el uso de herramientas de automatización para imágenes.

---

## 1. 🌐 Duplicación de Sitio Web (Manual)

Basado en la estructura de archivos de tu servidor (DirectAdmin/cPanel):

1.  **Copia de Archivos:** Descarga o copia la carpeta `public_html`. Es el núcleo que contiene WordPress.
2.  **Base de Datos:** Accede a **phpMyAdmin**, selecciona la base de datos de la web original y usa la función **Exportar**.
3.  **Despliegue:**
    * Sube los archivos al nuevo dominio/directorio.
    * Crea una nueva base de datos e **Importa** el archivo `.sql`.
    * Edita el archivo `wp-config.php` con los nuevos datos de conexión (`DB_NAME`, `DB_USER`, `DB_PASSWORD`).
4.  **Actualización de URLs:** Si el dominio ha cambiado, usa un script de "Search and Replace" para actualizar las rutas en la base de datos.

---

## 2. 🛠️ Configuración de Git (`.gitignore`)

Para evitar subir archivos innecesarios o sensibles al repositorio, crea un archivo `.gitignore` en la raíz:

```text
# Archivos sensibles y temporales
wp-config.php
.htaccess
*.log
.trash/

# Contenido multimedia pesado
wp-content/uploads/