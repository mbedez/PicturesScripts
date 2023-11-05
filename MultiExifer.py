from exif import Image
from datetime import datetime
from tkinter import filedialog

# Fonction pour convertir de DD (degrés décimaux) en DMS (degrés, minutes, secondes)
def dd_to_dms(dd):
    is_positive = dd >= 0
    dd = abs(dd)  # Utilisez la valeur absolue pour effectuer la conversion

    degrees = int(dd)
    minutes = int((dd - degrees) * 60)
    seconds = ((dd - degrees - minutes / 60) * 3600)

    # Si la valeur d'origine était négative, appliquez la négativité aux degrés
    if not is_positive:
        degrees = -degrees

    return degrees, minutes, seconds

# Utilisez filedialog pour obtenir la liste des chemins d'images sélectionnés
image_paths = filedialog.askopenfilenames(filetypes=[("Image files", ".png .jpg .jpeg")])

# Demander la latitude GPS en degrés décimaux
gps_latitude_dd = float(input("Entrez la latitude GPS en degrés décimaux : "))
gps_longitude_dd = float(input("Entrez la longitude GPS en degrés décimaux : "))

# Convertir de DD en DMS
gps_latitude_dms = dd_to_dms(gps_latitude_dd)
gps_longitude_dms = dd_to_dms(gps_longitude_dd)

# Déterminer la référence de la latitude en fonction du signe
gps_latitude_ref = "N" if gps_latitude_dd >= 0 else "S"
if gps_latitude_dms[0] < 0  : gps_latitude_dms = (-gps_latitude_dms[0],gps_latitude_dms[1],gps_latitude_dms[2])

# Déterminer la référence de la longitude en fonction du signe
gps_longitude_ref = "E" if gps_longitude_dd >= 0 else "W"
if gps_longitude_dms[0] < 0  : gps_longitude_dms = (-gps_longitude_dms[0],gps_longitude_dms[1],gps_longitude_dms[2])

day = int(input("Entrez le jour de la prise de photo : "))
month = int(input("Entrez le mois de la prise de photo : "))
year = int(input("Entrez l'année de la prise de photo : "))

s = 0
m = 0
for image_path in image_paths:
    # Récupérez le nom du fichier à partir du chemin
    image_filename = image_path.split('/')[-1]

    with open(image_path, 'rb') as image_file:  # Utilisez 'rb' pour le mode lecture
        my_image = Image(image_file)

        print(f"\n{image_filename}")

        # Modifier les informations de l'image
        my_image.gps_latitude = gps_latitude_dms
        my_image.gps_longitude = gps_longitude_dms
        my_image.gps_latitude_ref = gps_latitude_ref
        my_image.gps_longitude_ref = gps_longitude_ref

        new_date = datetime(year=year, month=month, day=day, hour=0, minute=m, second=s)
        my_image.datetime_original = new_date.strftime("%Y:%m:%d %H:%M:%S")

        with open(image_path, 'wb') as new_image_file:
            new_image_file.write(image_file.read())  # Copiez les données de l'image d'origine
            new_image_file.write(my_image.get_file())  # Ajoutez les informations EXIF
            print(f"Les informations ont été modifiées et l'image a été sauvegardée sous le nom {image_filename}.")
            if s < 59:
                s += 1
            else :
                s = 0
                m += 1

print("\nScript achevé avec succès !\n")
