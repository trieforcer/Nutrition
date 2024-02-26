import pandas as pd

# Laden der CSV-Datei
df = pd.read_csv("output.csv")

# Gewünschte Kalorien und Makronährstoffverteilung
gewünschte_kalorien = 2500
kohlenhydrate_prozent = 0.4
fett_prozent = 0.3
protein_prozent = 0.3

# Gewünschte Lebensmittelkategorieverteilung
kategorie_verteilung = {
    "Getreide, Getreideprodukte und Kartoffeln": 0.3,
    "Gemüse und Salat": 0.2,
    "Obst": 0.1,
    "Milch und Milchprodukte": 0.2,
    "Fleisch, Wurst, Fisch und Eier": 0.2,
}

# Berechnung der Zielwerte
kohlenhydrate_kalorien = gewünschte_kalorien * kohlenhydrate_prozent
fett_kalorien = gewünschte_kalorien * fett_prozent
protein_kalorien = gewünschte_kalorien * protein_prozent

# Funktionen zur Erstellung des Ernährungsplans
def get_kalorien_pro_kategorie(kategorie, verteilung):
    return gewünschte_kalorien * verteilung[kategorie]

def get_lebensmittel(kategorie, kalorien, df):
    return df[df["Kategorie"] == kategorie].sort_values("Kalorien/100g")

def get_menge(kalorien, kalorien_pro_einheit):
    return kalorien / kalorien_pro_einheit

# Erstellen des Ernährungsplans
plan = {}
for kategorie, verteilung in kategorie_verteilung.items():
    kalorien_pro_kategorie = get_kalorien_pro_kategorie(kategorie, verteilung)
    lebensmittel = get_lebensmittel(kategorie, kalorien_pro_kategorie, df)
    menge = get_menge(kalorien_pro_kategorie, lebensmittel["Kalorien/100g"])
    plan[kategorie] = {
        "Lebensmittel": lebensmittel["Lebensmittel"].tolist(),
        "Menge": menge.tolist(),
    }

# Ausgabe des Ernährungsplans
print(plan)

# Speichern des Ernährungsplans
with open("ernaehrungsplan.csv", "w") as f:
    f.write(plan)