import os
from fpdf import FPDF
from PIL import Image, ImageDraw, ImageFont

class PDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 12)
        self.cell(0, 10, 'Portfolio', new_x="LMARGIN", new_y="NEXT", align='C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', new_x="RIGHT", new_y="TOP", align='C')

# def agregar_id_a_imagen(file_path, product_id):
#     img = Image.open(file_path)
#     draw = ImageDraw.Draw(img)
    
#     # Fuente para el ID (puedes cambiar el tamaño y la fuente)
#     font_size = 30
#     try:
#         font = ImageFont.truetype("arial.ttf", font_size)
#     except IOError:
#         font = ImageFont.load_default()
    
#     # Posición del texto
#     text = f"ID: {product_id}"
#     bbox = draw.textbbox((0, 0), text, font=font)
#     text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
#     position = (img.width - text_width - 10, img.height - text_height - 10)  # En la esquina inferior derecha

#     # Añadir texto (ID) a la imagen
#     draw.text(position, text, font=font, fill=(255, 255, 255))  # Color blanco

#     # Guardar la imagen con el ID superpuesto
#     img.save(file_path)

def crear_portafolio(username, output_file="portafolio.pdf", fotos_por_pagina=6):
    # Crear el PDF en formato cuadrado
    pdf = PDF(orientation='P', unit='mm', format=(210, 210))  # 210x210 mm, tamaño cuadrado
    pdf.set_auto_page_break(auto=True, margin=15)

    folder_path = f"{username}"
    image_files = [f for f in os.listdir(folder_path) if f.endswith(".jpg")]

    # Ajuste del tamaño de las miniaturas (más cuadradas)
    thumbnail_size = 70

    # Mapear las páginas de destino
    link_map = []

    # Añadir las imágenes en miniatura (n fotos por página)
    for i, file_name in enumerate(image_files):
        product_id = i + 1  # Generar ID para cada producto
        
        # Superponer el ID en la imagen
        file_path = os.path.join(folder_path, file_name)
        # agregar_id_a_imagen(file_path, product_id)
        
        if i % fotos_por_pagina == 0:
            pdf.add_page()
        
        img = Image.open(file_path)
        
        # Mantener el aspecto ratio de la imagen
        img.thumbnail((thumbnail_size, thumbnail_size), Image.LANCZOS)
        x = 10 + (i % 3) * 65
        y = 20 + (i % fotos_por_pagina // 3) * 75
        pdf.image(file_path, x, y, img.size[0], img.size[1])

        # Crear enlace a WhatsApp con el ID del producto
        whatsapp_url = f"https://api.whatsapp.com/send?phone=573054365551&text=I'm%20interested%20in%20product%20ID%20{product_id}"
        link = pdf.add_link()
        pdf.set_link(link, y=0, page=None)
        pdf.link(x, y, img.size[0], img.size[1], whatsapp_url)

        # Mapear el enlace a la imagen grande en una página
        link_map.append((x, y, img.size[0], img.size[1], link))

    # Añadir páginas con imágenes grandes (una por página)
    for i, file_name in enumerate(image_files):
        pdf.add_page()
        file_path = os.path.join(folder_path, file_name)
        pdf.set_xy(0, 0)

        # Cargar imagen para determinar el aspecto ratio
        img = Image.open(file_path)
        img_width, img_height = img.size

        # Ajustar el tamaño de la imagen manteniendo el aspecto ratio
        max_size = 190  # Tamaño máximo tanto para ancho como para alto (cuadrado)
        if img_width > img_height:
            width = max_size
            height = int(max_size * img_height / img_width)
        else:
            height = max_size
            width = int(max_size * img_width / img_height)

        pdf.image(file_path, 10, 10, width, height)
        pdf.set_link(link_map[i][4], y=0)  # Mapeo del enlace a la página

        # Añadir el nombre de usuario en la parte superior izquierda en negrilla
        pdf.set_xy(10, 10)
        pdf.set_font('Helvetica', 'B', 12)
        pdf.set_text_color(0, 0, 0)  # Negro
        pdf.cell(0, 10, f"@{username}", new_x="LMARGIN", new_y="NEXT", align='L')

    pdf.output(output_file)

# Ejecución del Paso 2
username = "vinylreart_co"  # Reemplaza con el nombre de usuario de Instagram
output_file = "portafolio.pdf"

# Crear el portafolio usando las imágenes restantes en la carpeta
crear_portafolio(username, output_file=output_file)

print(f"Portafolio creado: {output_file}")
