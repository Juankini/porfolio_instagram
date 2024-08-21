import instaloader
from PIL import Image
import os

# Función para descargar las fotos de Instagram
def descargar_fotos(username, max_fotos=10):
    L = instaloader.Instaloader()
    profile = instaloader.Profile.from_username(L.context, username)
    
    count = 0
    for post in profile.get_posts():
        if count < max_fotos:
            L.download_post(post, target=f"{username}")
            count += 1
        else:
            break

# Función para crear un portafolio en PDF
def crear_portafolio(username, output_file="portafolio.pdf"):
    images = []
    folder_path = f"{username}"

    for file_name in os.listdir(folder_path):
        if file_name.endswith(".jpg"):
            file_path = os.path.join(folder_path, file_name)
            img = Image.open(file_path)
            img = img.convert("RGB")  # Convertir a RGB
            images.append(img)

    if images:
        images[0].save(output_file, save_all=True, append_images=images[1:])

# Ejecución
username = "vinylreart_co"  # Nombre de usuario de Instagram
max_fotos = 10  # Número máximo de fotos a descargar

# Descarga las fotos de la cuenta de Instagram
descargar_fotos(username, max_fotos)

# Crea el portafolio en PDF
crear_portafolio(username, output_file="portafolio.pdf")

print(f"Portafolio creado: portafolio.pdf")
