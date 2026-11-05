# Időjárás-nézegető

## Hallgató
Szabó Márió

## Feladat leírása
Asztali alkalmazás, amely egy megadott város aktuális időjárását (hőmérséklet, szélsebesség) és a következő 24 óra hőmérséklet-előrejelzését mutatja grafikonon. Az adatokat az ingyenes Open-Meteo API szolgáltatja (API-kulcs nem kell).

Használat: írd be a város nevét, majd Enter vagy a Keresés gomb. Az Esc billentyű kilép.

## Indítás
```
pip install -r requirements.txt
python main.py
```

## Modulok és a bennük használt függvények
- **tkinter** (tanult): `Tk`, `Frame`, `Entry`, `Button`, `Label`, `bind`, `mainloop`, `messagebox.showerror/showwarning/showinfo`
- **datetime** (tanult): `datetime.now`, `datetime.fromisoformat`, `strftime`
- **matplotlib** (bemutatandó): `Figure`, `add_subplot`, `plot`, `set_title`, `set_xlabel`, `set_ylabel`, `grid`, `FigureCanvasTkAgg.draw`
- **requests** (web): `get`, `raise_for_status`, `json`
- **SzM_idojaras** (saját modul): a függvényeket és az osztályt tartalmazza

## Saját függvények (SzM_idojaras.py)
- `szm_varos_koordinata(nev)` – városnévből koordináta
- `szm_idojaras_lekerdez(lat, lon)` – időjárás-adatok lekérése

## Osztály
- `SzMIdojarasApp` – az ablak felépítése és eseménykezelése (`kereses`, `megjelenit`, `kilepes`)

## Eseménykezelés
Gombnyomás (`command`), Enter (`<Return>`), Esc (`<Escape>`)
