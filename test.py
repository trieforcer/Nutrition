import pandas as pd
import os

def read_excel_and_write_to_csv(folder_path, output_csv):
    # Dictionary, um die Kategorien den Dateinamen zuzuordnen
    category_mapping = {
        "Fleisch, Wurst, Fisch und Eier.xlsx": "Fleisch, Wurst, Fisch und Eier",
        "Gemüse und Salat.xlsx": "Gemüse und Salat",
        "Getreide, Getreideprodukte und Kartoffeln.xlsx": "Getreide, Getreideprodukte und Kartoffeln",
        "Milch und Milchprodukte.xlsx": "Milch und Milchprodukte",
        "Obst.xlsx": "Obst",
        "Öle und Fette.xlsx": "Öle und Fette"
    }
    
    # Leeres DataFrame erstellen, um die Daten zu speichern
    df_all = pd.DataFrame(columns=["Kategorie", "Lebensmittel", "Kalorien", "Kohlenhydrate", "Fette", "Proteine"])
    
    for filename in os.listdir(folder_path):
        if filename.endswith(".xlsx"):
            file_path = os.path.join(folder_path, filename)
            category = category_mapping.get(filename)
            if category:
                df = pd.read_excel(file_path)
                df["Kategorie"] = category
                df_all = pd.concat([df_all, df], ignore_index=True)
    
    # CSV-Datei erstellen
    df_all.to_csv(output_csv, index=False)
    print("CSV-Datei erfolgreich erstellt:", output_csv)

# Pfade für den Ordner mit den Excel-Dateien und die Ausgabedatei angeben
folder_path = "Lebensmittelnährwerte"
output_csv = "output.csv"

# Funktion aufrufen, um die Excel-Dateien zu lesen und in eine CSV-Datei zu schreiben
read_excel_and_write_to_csv(folder_path, output_csv)
