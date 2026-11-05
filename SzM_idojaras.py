import tkinter as tk
from tkinter import messagebox
from datetime import datetime

import requests
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
IDOJARAS_URL = "https://api.open-meteo.com/v1/forecast"


def szm_varos_koordinata(nev):
    valasz = requests.get(GEO_URL, params={"name": nev, "count": 1}, timeout=10)
    valasz.raise_for_status()
    talalatok = valasz.json().get("results")
    if not talalatok:
        return None
    elso = talalatok[0]
    return elso["name"], elso["latitude"], elso["longitude"]


def szm_idojaras_lekerdez(lat, lon):
    parameterek = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": "true",
        "hourly": "temperature_2m",
        "forecast_days": 2,
        "timezone": "auto",
    }
    valasz = requests.get(IDOJARAS_URL, params=parameterek, timeout=10)
    valasz.raise_for_status()
    return valasz.json()


class SzMIdojarasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Időjárás-nézegető")

        felso = tk.Frame(root)
        felso.pack(padx=10, pady=10)

        self.beviteli_mezo = tk.Entry(felso, width=25)
        self.beviteli_mezo.pack(side=tk.LEFT, padx=5)
        self.beviteli_mezo.insert(0, "Budapest")
        self.beviteli_mezo.bind("<Return>", self.kereses)

        self.gomb = tk.Button(felso, text="Keresés", command=self.kereses)
        self.gomb.pack(side=tk.LEFT)

        self.cimke = tk.Label(root, text="Adj meg egy várost!", font=("Arial", 12))
        self.cimke.pack(pady=5)

        self.abra = Figure(figsize=(6, 3.5))
        self.tengely = self.abra.add_subplot(111)
        self.vaszon = FigureCanvasTkAgg(self.abra, master=root)
        self.vaszon.get_tk_widget().pack(padx=10, pady=10)

        root.bind("<Escape>", self.kilepes)

    def kilepes(self, esemeny=None):
        self.root.destroy()

    def kereses(self, esemeny=None):
        nev = self.beviteli_mezo.get().strip()
        if not nev:
            messagebox.showwarning("Hiányzó adat", "Írj be egy városnevet!")
            return
        try:
            hely = szm_varos_koordinata(nev)
            if hely is None:
                messagebox.showinfo("Nincs találat", f"Nem található: {nev}")
                return
            varos, lat, lon = hely
            adatok = szm_idojaras_lekerdez(lat, lon)
        except requests.RequestException:
            messagebox.showerror("Hiba", "Nem sikerült elérni az időjárás-szolgáltatást.")
            return
        self.megjelenit(varos, adatok)

    def megjelenit(self, varos, adatok):
        aktualis = adatok["current_weather"]
        most = datetime.now().strftime("%Y.%m.%d. %H:%M")
        self.cimke.config(
            text=f"{varos} – {aktualis['temperature']} °C, "
            f"szél: {aktualis['windspeed']} km/h ({most})"
        )

        idok = [datetime.fromisoformat(i) for i in adatok["hourly"]["time"]]
        homerseklet = adatok["hourly"]["temperature_2m"]
        kezdet = max(0, datetime.fromisoformat(aktualis["time"]).hour)
        idok = idok[kezdet:kezdet + 24]
        homerseklet = homerseklet[kezdet:kezdet + 24]
        cimkek = [i.strftime("%H:%M") for i in idok]

        self.tengely.clear()
        self.tengely.plot(range(len(homerseklet)), homerseklet, marker="o", color="tab:red")
        self.tengely.set_title(f"{varos} – következő 24 óra")
        self.tengely.set_xlabel("Idő")
        self.tengely.set_ylabel("Hőmérséklet (°C)")
        self.tengely.set_xticks(range(0, len(cimkek), 3))
        self.tengely.set_xticklabels(cimkek[::3])
        self.tengely.grid(True)
        self.abra.tight_layout()
        self.vaszon.draw()
