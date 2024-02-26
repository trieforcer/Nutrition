import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from tkinter import Canvas, PhotoImage
from tkinter.ttk import Treeview
from pathlib import Path
import TKinterModernThemes as TKMT
import numpy as np

# Pfade definieren
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Leni\Ernährungsplan\Tkinter-Designer-master\Tkinter-Designer-master\build\assets\frame0")

# Hilfsfunktion für relativen Pfad zu Assets
def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# GUI erstellen
class App(TKMT.ThemedTKinterFrame):
    def __init__(self):
        super().__init__("MaxNutrition", "park", "dark")
        
        # Vollbildmodus
        self.master.attributes('-fullscreen', True)
        self.master.configure(bg="#EFEFEF")
        self.master.resizable(True, True)

        # Canvas erstellen
        self.canvas = Canvas(
            self.master,
            bg="#EFEFEF",
            height=self.master.winfo_screenheight(),
            width=self.master.winfo_screenwidth(),
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        # Bilder einfügen
        self.image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
        self.image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
        self.image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
        self.image_image_4 = PhotoImage(file=relative_to_assets("image_4.png"))
        self.image_image_5 = PhotoImage(file=relative_to_assets("image_5.png"))
        self.image_image_6 = PhotoImage(file=relative_to_assets("image_6.png"))
        self.image_image_7 = PhotoImage(file=relative_to_assets("image_7.png"))
        self.image_image_8 = PhotoImage(file=relative_to_assets("image_8.png"))
        self.image_image_9 = PhotoImage(file=relative_to_assets("image_9.png"))
        self.image_image_10 = PhotoImage(file=relative_to_assets("image_10.png"))
        self.image_image_11 = PhotoImage(file=relative_to_assets("image_11.png"))

        self.canvas.create_image(
            177.0,
            540.0,
            image=self.image_image_1
        )
        self.canvas.create_image(
            1137.0,
            50.0,
            image=self.image_image_2
        )
        self.canvas.create_image(
            570.0,
            202.0,
            image=self.image_image_3
        )
        self.canvas.create_image(
            950.0,
            202.0,
            image=self.image_image_4
        )
        self.canvas.create_image(
            1330.0,
            202.0,
            image=self.image_image_5
        )
        self.canvas.create_image(
            1709.0,
            202.0,
            image=self.image_image_6
        )
        self.canvas.create_image(
            760.0,
            499.0,
            image=self.image_image_7
        )
        self.canvas.create_image(
            760.0,
            888.0,
            image=self.image_image_8
        )
        self.canvas.create_image(
            1519.0,
            888.0,
            image=self.image_image_9
        )
        self.canvas.create_image(
            1330.0,
            499.0,
            image=self.image_image_10
        )
        self.canvas.create_image(
            1709.0,
            499.0,
            image=self.image_image_11
        )

        # Daten laden
        data_nutrition_plan = pd.read_csv("nutrition_plan.csv")  # Daten aus der ersten CSV-Datei
        data_output = pd.read_csv("output.csv")  # Daten aus der zweiten CSV-Datei

        # TreeViews für Tabellen erstellen
        columns_tag = ["Tag"]
        self.table_tag = Treeview(master=self.master, columns=columns_tag, show="headings")
        for column in columns_tag:
            self.table_tag.heading(column, text=column)
            self.table_tag.column(column, width=90)
        for index, row in data_nutrition_plan.iterrows():
            self.table_tag.insert("", "end", values=row.tolist())
        self.table_tag.place(x=415, y=320, height=360)

        columns_lebensmittel = ["Lebensmittel", "Menge"]  # Hinzufügen der Spalte "Menge"
        self.table_lebensmittel = Treeview(master=self.master, columns=columns_lebensmittel, show="headings")
        for column in columns_lebensmittel:
            self.table_lebensmittel.heading(column, text=column)
            self.table_lebensmittel.column(column, width=108)
        self.table_lebensmittel.place(x=550, y=320, height=360)

        # Funktion für Klick auf TreeView-Element
        def on_treeview_click(event):
            item = event.widget.focus()
            selected_tag = event.widget.item(item)['values'][0]

            if event.widget == self.table_tag:  # Nur löschen, wenn Klick im table_tag erfolgt ist
                for row in self.table_lebensmittel.get_children():
                    self.table_lebensmittel.delete(row)

            for index, row in data_nutrition_plan.iterrows():
                if row["Tag"] == selected_tag:
                    for lebensmittel, Menge in zip(row["Lebensmittel"].strip("[]").replace("'", "").split(", "), row["Menge"].strip("[]").split(", ")):
                        self.table_lebensmittel.insert("", "end", values=(lebensmittel.strip(), Menge.strip()))
                    # Neu: Piechart aus der ersten CSV-Datei anzeigen
                    plt.clf()

                    labels = ["Kh", "Fette", "Proteine"]
                    sizes = [float(row["Kohlenhydrate"]), float(row["Fette"]), float(row["Proteine"])]

                    fig, ax = plt.subplots(figsize=(4, 2), facecolor="#313131")
                    wedges, texts, autotexts = ax.pie(sizes, labels=None, autopct='%1.1f%%', startangle=140, wedgeprops=dict(width=0.4), colors=['#ff0404','#044fff','#ffd216'])

                    ax.axis('equal')

                    bbox_props = dict(boxstyle="square,pad=0.3", fc="#313131", ec="#313131", lw=0)
                    kw = dict(arrowprops=dict(arrowstyle="-"),
                            bbox=bbox_props, zorder=0, va="center")

                    for i, p in enumerate(wedges):
                        ang = (p.theta2 - p.theta1)/2. + p.theta1
                        y = np.sin(np.deg2rad(ang))
                        x = np.cos(np.deg2rad(ang))
                        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
                        connectionstyle = f"angle,angleA=0,angleB={ang}"
                        kw["arrowprops"].update({"connectionstyle": connectionstyle})
                        ax.annotate(labels[i], xy=(x, y), xytext=(1.1*np.sign(x), 1.2*y),
                                    horizontalalignment=horizontalalignment,color="white", **kw)
                        ax.text(0, 0, f'{row["Kalorien"]} Kcal', ha='center', va='center', fontsize=8, color='white')

                    pie_canvas = FigureCanvasTkAgg(fig, master=self.master)
                    pie_canvas.draw()
                    pie_canvas_widget = pie_canvas.get_tk_widget()
                    pie_canvas_widget.place(x=810, y=320, width=295, height=177.5)



            for index, row in data_output.iterrows():
                if row["Lebensmittel"] == selected_tag:
                    # Neu: Piechart aus der zweiten CSV-Datei anzeigen
                    plt.clf()  # Lösche vorherige Diagramme
                    labels = ["Kh", "Fette", "Proteine"]
                    sizes = [float(row["Kohlenhydrate"]), float(row["Fette"]), float(row["Proteine"])]
                    fig, ax = plt.subplots(figsize=(2, 1), facecolor="#313131")
                    wedges, texts, autotexts = ax.pie(sizes, labels=None, autopct='%1.1f%%', startangle=140, wedgeprops=dict(width=0.4), colors=['#ff0404','#044fff','#ffd216'])

                    ax.axis('equal')

                    bbox_props = dict(boxstyle="square,pad=0.3", fc="#313131", ec="#313131", lw=0)
                    kw = dict(arrowprops=dict(arrowstyle="-"),
                            bbox=bbox_props, zorder=0, va="center")

                    for i, p in enumerate(wedges):
                        ang = (p.theta2 - p.theta1)/2. + p.theta1
                        y = np.sin(np.deg2rad(ang))
                        x = np.cos(np.deg2rad(ang))
                        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
                        connectionstyle = f"angle,angleA=0,angleB={ang}"
                        kw["arrowprops"].update({"connectionstyle": connectionstyle})
                        ax.annotate(labels[i], xy=(x, y), xytext=(1.1*np.sign(x), 1.2*y),
                                    horizontalalignment=horizontalalignment,color="white", **kw)
                        ax.text(0, 0, f'{row["Kalorien"]} Kcal', ha='center', va='center', fontsize=8, color='white')

                    pie_canvas = FigureCanvasTkAgg(fig, master=self.master)
                    pie_canvas.draw()
                    pie_canvas_widget = pie_canvas.get_tk_widget()
                    pie_canvas_widget.place(x=810, y=502, width=295, height=177.5)
                    

        self.table_tag.bind("<ButtonRelease-1>", on_treeview_click)
        self.table_lebensmittel.bind("<ButtonRelease-1>", on_treeview_click)

# Hauptloop starten
if __name__ == "__main__":
    app = App()
    app.run()
