import os
from PIL import Image
from PIL.ExifTags import TAGS

def get_photo_date(image_path):
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()
        if exif_data is not None:
            for tag_id, value in exif_data.items():
                tag_name = TAGS.get(tag_id, tag_id)
                if tag_name == 'DateTimeOriginal':
                    return value
    except (IOError, AttributeError):
        pass
    except Exception as e:
        print("Erreur lors de la récupération des métadonnées EXIF :", str(e))

    return None

def rename_photo_with_date(image_path, date):
    directory, filename = os.path.split(image_path)
    file_extension = filename.split(".")[-1].lower()  # Get the file extension
    new_filename = date.replace(":", "-", 2).replace(":", "h", 1).replace(":", "m", 1).replace(" ", "_") + "s." + file_extension
    new_path = os.path.join(directory, new_filename)

    if image_path != new_path:
        counter = 1
        while os.path.exists(new_path):
            new_filename = date.replace(":", "-", 2).replace(":", "h", 1).replace(":", "m", 1).replace(" ", "_") + "s_" + str(counter) + "." + file_extension
            new_path = os.path.join(directory, new_filename)
            counter += 1

        os.rename(image_path, new_path)
        return new_path
    else:
        return image_path

def select_folder():
    folder_path = input("Veuillez entrer le chemin du dossier contenant les images : ")
    if folder_path:
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            file_extension = filename.split(".")[-1].lower()  # Get the file extension
            if file_extension in ["jpg", "jpeg", "png", "webp"]:
                photo_date = get_photo_date(file_path)
                if photo_date is not None:
                    new_path = rename_photo_with_date(file_path, str(photo_date))
                    print("Photo renommée : " + new_path)
                else:
                    print("Impossible de récupérer la date de la photo pour : " + file_path)
        print("Renommage terminé.")
    else:
        print("Aucun chemin de dossier spécifié.")

if os.name == 'nt':  # Check if the OS is Windows
    import tkinter as tk
    from tkinter import filedialog

    # Création de la fenêtre principale
    window = tk.Tk()
    window.title("Sélection de dossier")
    window.geometry("300x150")

    # Bouton de sélection de dossier
    select_button = tk.Button(window, text="Sélectionner un dossier", command=select_folder)
    select_button.pack(pady=20)

    # Lancement de la boucle principale de l'interface graphique
    window.mainloop()
else:
    select_folder()
