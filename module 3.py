import requests
from tkinter import *
from tkinter.ttk import *
import psycopg2
from tkinter import Tk, Label, Button, Toplevel, StringVar


# Mijn api id
appid = "41b4cded1ecf20968aa176a6963a4f6b"

# Alle API-URL's voor Utrecht, Rotterdam en Arnhem
urlUtrecht = f'http://api.openweathermap.org/data/2.5/weather?q=Utrecht,nl&APPID={appid}&units=metric'
urlRotterdam = f'http://api.openweathermap.org/data/2.5/weather?q=Rotterdam,nl&APPID={appid}&units=metric'
urlArnhem = f'http://api.openweathermap.org/data/2.5/weather?q=Arnhem,nl&APPID={appid}&units=metric'

# Hier wordt HTTP response naar de weer-API voor Utrecht, Rotterdam en Arnhem gedaan
rUt = requests.get(urlUtrecht)
rRt = requests.get(urlRotterdam)
rAr = requests.get(urlArnhem)

# Ik heb jason hier gebruikt zodat ik van de api gemakkelijk info terug krijg
resUt = rUt.json()
resRt = rRt.json()
resAr = rAr.json()

# Hier wordt de waarde van api key opgehaald
basisUt = resUt.get('main', {})
basisRt = resRt.get('main', {})
basisAr = resAr.get('main', {})

# Hier wordt de temperatuur van de api key opgehaald
tempKevUt = basisUt.get('temp', 'N/A')
tempKevRt = basisRt.get('temp', 'N/A')
tempKevAr = basisAr.get('temp', 'N/A')


# Functie voor de laatste 5 berichten
def haal_laatste_berichten_voor_station(station, num_berichten):
    try:
        conn = psycopg2.connect(
            host="40.113.123.172",
            database="stationszuil",
            user="postgres",
            password="postgres",
            port="5432"
        )
        cursor = conn.cursor()
        # hier worden de laatste 5 berichten opgehaald van de database
        cursor.execute("SELECT naam, datum, bericht FROM reiziger WHERE station = %s ORDER BY datum DESC LIMIT %s", (station, num_berichten))
        berichten = cursor.fetchall()

        conn.close()
        return berichten
    # als de code hier boven niet lukt, wordt er een fout opgetreden
    except Exception as e:
        print(f"Fout bij het ophalen van berichten: {e}")
        return []


def toon_laatste_berichten(station):
    # Haalt de laatste berichten op voor het opgegeven station
    berichten = haal_laatste_berichten_voor_station(station, 5)

    if berichten:
        # Als er berichten zijn, formatteer ze en stel de tekstvariabele in
        geformatteerde_berichten = [f"{bericht[1]} - {bericht[0]}: {bericht[2]}" for bericht in berichten]
        berichten_tekst.set("\n".join(geformatteerde_berichten))
    else:
        # Als er geen berichten zijn, geef een melding dat er geen berichten beschikbaar zijn
        berichten_tekst.set(f"Geen berichten beschikbaar voor station {station}.")


# TK kinter
def toon_faciliteiten(station, window):
    # Label gemaakt om de faciliteiten te tonen
    faciliteiten_label = Label(window, text="Faciliteiten op dit station:", font=("Helvetica", 14), bg=background_color, fg=text_color)
    faciliteiten_label.pack(pady=10)

    # Hier zie je de faciliteiten per station
    if station == 'Utrecht':
        faciliteiten = ["Parkeerplaats (PR)", "Lift", "OV-fiets", "Toilet"]
    elif station == 'Arnhem':
        faciliteiten = ["Parkeerplaats (PR)", "OV-fiets", "Toilet"]
    elif station == 'Rotterdam':
        faciliteiten = ["Parkeerplaats (PR)", "Lift", "OV-fiets", "Toilet"]
    else:
        faciliteiten = ["Faciliteiten niet beschikbaar"]

    # Hier worden de faciliteiten op het scherm vertoond
    for faciliteit in faciliteiten:
        faciliteit_label = Label(window, text=faciliteit, font=("Helvetica", 12), bg=background_color, fg=text_color)
        faciliteit_label.pack()


def Arnhem():
    newWindow = Toplevel(master) # Hier maak ik een nieuwe venster
    newWindow.title("Station Arnhem")
    newWindow.geometry("720x580")
    Label(newWindow, text="Welkom op Station Arnhem!", bg=background_color, fg=button_color, font=("Helvetica", 16)).pack() # Label gemaakt zodat op de gui 'Welkom op Station Arnhem' komt staan
    Label(newWindow, text=f"Het is momenteel {tempKevAr} Graden op station Arnhem", bg=background_color, fg=text_color).pack()
    toon_laatste_berichten('Arnhem', newWindow)  # Laat de laatste 5 berichten zien voor Arnhem
    toon_faciliteiten('Arnhem', newWindow)  # Toon de faciliteiten voor Arnhem

# Zelfde proces
def Utrecht():
    newWindow = Toplevel(master)
    newWindow.title("Station Utrecht")
    newWindow.geometry("720x580")
    Label(newWindow, text="Welkom op Station Utrecht!", bg=background_color, fg=button_color, font=("Helvetica", 16)).pack()
    Label(newWindow, text=f"Het is momenteel {tempKevUt} Graden op station Utrecht", bg=background_color, fg=text_color).pack()
    toon_laatste_berichten('Utrecht', newWindow)
    toon_faciliteiten('Utrecht', newWindow)

# Zelfde proces
def Rotterdam():
    newWindow = Toplevel(master)
    newWindow.title("Station Rotterdam")
    newWindow.geometry("720x580")
    Label(newWindow, text="Welkom op Station Rotterdam!", bg=background_color, fg=button_color, font=("Helvetica", 16)).pack()
    Label(newWindow, text=f"Het is momenteel {tempKevRt} Graden op station Rotterdam", bg=background_color, fg=text_color).pack()
    toon_laatste_berichten('Rotterdam', newWindow)
    toon_faciliteiten('Rotterdam', newWindow)
# Function definitions

def toon_laatste_berichten(station, window):
    # Hier wordt de laatste 5 berichten op voor het opgegeven station
    berichten = haal_laatste_berichten_voor_station(station, 5)

    if berichten:
        # Als er berichten zijn:
        # Formatteer elk bericht met de naam, datum en berichttekst
        geformatteerde_berichten = [f"{bericht[1]} - {bericht[0]}: {bericht[2]}" for bericht in berichten]

        # De geformatteerde berichten wordt in een enkele tekst met nieuwe regels gezet
        berichten_tekst.set("\n".join(geformatteerde_berichten))
        berichten_weergave = Label(window, textvariable=berichten_tekst, wraplength=300, bg=background_color, fg=text_color)
        berichten_weergave.pack()
    else:
        berichten_tekst.set(f"Geen berichten beschikbaar voor station {station}.")
        berichten_weergave = Label(window, textvariable=berichten_tekst, wraplength=300, bg=background_color, fg=text_color)
        berichten_weergave.pack()

# Tkinter opzetten
master = Tk() # De hoofdvenster
master.minsize(600, 300)
master.geometry("235x270")
master.title('NS Stationszuil')

# Stylen
background_color = "#FFFF00"  # Geel
text_color = "#333333"
button_color = "#0000FF"  # Blauw
button_text_color = "white"

# Configuratie gedaan om het hoofdvenster gebruikt wordt op de gegeven achtergrondkleur
master.configure(bg=background_color)

# Hier worden de labels gemaakt

labeltwee = Label(master=master, text='Welkom bij NS!', bg=background_color, fg=button_color, font=("Helvetica", 16))
labeltwee.pack(pady=10)

label = Label(master, text="Kies een station", bg=background_color, fg=text_color)
label.pack(pady=10)

# Zorgt ervoor dat de berichten worden weergegeven op de tkinter
berichten_tekst = StringVar()

# Hier worden de buttons gemaakt
btn = Button(master, text="Arnhem", command=Arnhem, font=("Helvetica", 12))
btn.configure(bg=button_color, fg=button_text_color)
btn.pack(pady=10)

btn = Button(master, text="Utrecht", command=Utrecht, font=("Helvetica", 12))
btn.configure(bg=button_color, fg=button_text_color)
btn.pack(pady=10)

btn = Button(master, text="Rotterdam", command=Rotterdam, font=("Helvetica", 12))
btn.configure(bg=button_color, fg=button_text_color)
btn.pack(pady=10)

master.mainloop()

