import os
import instaloader

def descargar_fotos(username, max_fotos=10):
    L = instaloader.Instaloader()
    profile = instaloader.Profile.from_username(L.context, username)
    
    count = 0
    os.makedirs(username, exist_ok=True)
    for post in profile.get_posts():
        if count < max_fotos:
            L.download_post(post, target=f"{username}")
            count += 1
        else:
            break

# Ejecución del Paso 1
username = "vinylreart_co"  # Reemplaza con el nombre de usuario de Instagram
max_fotos = 40  # Número máximo de fotos a descargar

# Descargar las fotos de la cuenta de Instagram
descargar_fotos(username, max_fotos)

print(f"Imágenes descargadas en la carpeta: {username}")
print("Puedes revisar la carpeta y eliminar las imágenes que no deseas incluir en el portafolio.")
