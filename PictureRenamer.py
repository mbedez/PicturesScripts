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

import os

def rename_photo_with_date(image_path, date):
    directory, filename = os.path.split(image_path)
    _name_without_extension, extension = os.path.splitext(filename)

    new_filename = date.replace(":", "-", 2).replace(":", "h", 1).replace(":", "m", 1).replace(" ", "_") + "s" + extension
    new_path = os.path.join(directory, new_filename)

    if image_path != new_path:
        counter = 1
        while os.path.exists(new_path):
            new_filename = date.replace(":", "-", 2).replace(":", "h", 1).replace(":", "m", 1).replace(" ", "_") + "s_" + str(counter) + extension
            new_path = os.path.join(directory, new_filename)
            counter += 1

        os.rename(image_path, new_path)
        return new_path
    else:
        return image_path


def select_folder_linux():
    folder_path = input("Veuillez entrer le chemin du dossier contenant les images : ")
    RenamePictures(folder_path)

def select_folder_windows():
    folder_path = filedialog.askdirectory()
    RenamePictures(folder_path)

def RenamePictures(folder_path):
    for filename in os.listdir(folder_path):
        suffixs = (".jpg", ".jpeg", ".png", ".webp")
        if filename.endswith(suffixs):
            file_path = os.path.join(folder_path, filename)
            photo_date = get_photo_date(file_path)
            if photo_date is not None:
                new_path = rename_photo_with_date(file_path, str(photo_date))
                print("Photo renommée : " + new_path)
            else:
                print("Impossible de récupérer la date de la photo pour : " + file_path)
    print("Renommage terminé.")

if os.name == 'nt':  # Check if the OS is Windows
    import tkinter as tk
    from tkinter import filedialog

    # Création de la fenêtre principale
    window = tk.Tk()
    window.title("Sélection de dossier")
    window.geometry("300x150")

    # Bouton de sélection de dossier
    select_button = tk.Button(window, text="Sélectionner un dossier", command=select_folder_windows)
    select_button.pack(pady=20)

    # Lancement de la boucle principale de l'interface graphique
    window.mainloop()
else:
    select_folder_linux()
