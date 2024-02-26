from typing import Dict, List, Tuple
import pandas as pd
import os
import random
import csv
import tkinter as tk
from tkinter import ttk


class DataModel:
    def __init__(self):
        self.df: pd.DataFrame = None

    def load_data(self, folder_path: str) -> pd.DataFrame:
        all_data = pd.DataFrame()

        for file_name in os.listdir(folder_path):
            if file_name.endswith(".xlsx"):
                category = os.path.splitext(file_name)[0]
                df = pd.read_excel(os.path.join(folder_path, file_name))
                df["Kategorie"] = category
                all_data = pd.concat([all_data, df], ignore_index=True)

        self.df = all_data
        return all_data


def generate_nutrition_plan(
    df: pd.DataFrame,
    calories_needed: float,
    macronutrient_distribution: Dict[str, float],
    category_distribution: Dict[str, float],
    num_days: int = 20,
) -> List[Tuple]:
    nutrition_plan = []

    for _ in range(num_days):
        meal = []
        quantities = []

        for category, percentage in category_distribution.items():
            category_data = df[df["Kategorie"] == category]
            sample_size = int(len(category_data) * percentage / 100)
            selected_foods = category_data.sample(n=sample_size)

            meal.extend(selected_foods["Lebensmittel"].tolist())
            quantities.extend([random.randint(50, 200) for _ in range(sample_size)])

        total_calories = 0
        total_carbs = 0
        total_fats = 0
        total_proteins = 0

        for food, quantity in zip(meal, quantities):
            food_data = df[df["Lebensmittel"] == food].iloc[0]

            total_calories += float(str(food_data["Kalorien"]).replace(",", "."))
            total_carbs += float(str(food_data["Kohlenhydrate"]).replace(",", "."))
            total_fats += float(str(food_data["Fette"]).replace(",", "."))
            total_proteins += float(str(food_data["Proteine"]).replace(",", "."))

        nutrition_plan.append(
            (
                f"Tag {len(nutrition_plan)+1}",
                meal,
                quantities,
                round(total_calories, 2),
                round(total_carbs, 2),
                round(total_fats, 2),
                round(total_proteins, 2),
            )
        )

    return nutrition_plan


def display_nutrition_plan(nutrition_plan: List[Tuple]) -> None:
    root = tk.Tk()
    root.title("Automatisierter Ernährungsplan")

    tree = ttk.Treeview(root)
    tree["columns"] = (
        "Tag",
        "Lebensmittel",
        "Menge",
        "Kalorien",
        "Kohlenhydrate",
        "Fette",
        "Proteine",
    )
    tree["show"] = "headings"

    for column in tree["columns"]:
        tree.heading(column, text=column)

    for item in nutrition_plan:
        quantities_str = ', '.join(map(str, item[2]))
        tree.insert("", "end", values=(item[0], item[1], quantities_str, item[3], item[4], item[5], item[6]))

    tree.pack(expand=True, fill=tk.BOTH)
    root.mainloop()


def save_nutrition_plan(nutrition_plan: List[Tuple], file_name: str = "nutrition_plan.csv") -> None:
    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Tag", "Lebensmittel", "Menge", "Kalorien", "Kohlenhydrate", "Fette", "Proteine"])
        for item in nutrition_plan:
            quantities_str = ', '.join(map(str, item[2]))
            writer.writerow((item[0], item[1], quantities_str, item[3], item[4], item[5], item[6]))

    print(f"Ernährungsplan wurde erfolgreich in {file_name} gespeichert.")


def main():
    folder_path = "Lebensmittelnährwerte"
    model = DataModel()
    df = model.load_data(folder_path)

    if not df.empty:
        calories_needed = 2500
        macronutrient_distribution = {"Kohlenhydrate": 40, "Fette": 30, "Proteine": 30}
        category_distribution = {
            "Getreide, Getreideprodukte und Kartoffeln": 30,
            "Gemüse und Salat": 20,
            "Obst": 10,
            "Milch und Milchprodukte": 20,
            "Fleisch, Wurst, Fisch und Eier": 20,
        }

        nutrition_plan = generate_nutrition_plan(df, calories_needed, macronutrient_distribution, category_distribution)
        display_nutrition_plan(nutrition_plan)
        save_nutrition_plan(nutrition_plan)
    else:
        print("Fehler: Keine Daten gefunden.")


if __name__ == "__main__":
    main()