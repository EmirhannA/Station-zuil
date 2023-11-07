import csv
import random
from datetime import datetime
import tkinter as tk
import psycopg2
import requests

api_key = "41b4cded1ecf20968aa176a6963a4f6b"

stations = ['Utrecht', 'Arnhem', 'Rotterdam']

# Here, I've defined the random facilities for each station
faciliteiten_per_station = {
    "Utrecht": ['OV-fietsen', 'Lift', 'Toilet', 'P+R'],
    "Arnhem": ['OV-fietsen', 'Toilet', 'P+R'],
    "Rotterdam": ['Lift', 'P+R'],
}

def haal_berichten_op_voor_station(station):
    try:
        conn = psycopg2.connect(
            host="40.113.123.172",
            database="stationszuil",
            user="postgres",
            password="postgres",
            port="5432"
        )
        cursor = conn.cursor()

        cursor.execute("SELECT naam, datum, bericht FROM reiziger WHERE station = %s", (station,))
        berichten = cursor.fetchall()

        conn.close()
        return berichten  # Return messages including name and date

    except Exception as e:
        print(f"Fout bij het ophalen van berichten: {e}")
        return []

def get_weather(station_name):
    # Define the API URL
    url = f'https://api.openweathermap.org/data/2.5/weather?q={station_name}&appid={api_key}'

    response = requests.get(url)
    data = response.json()

    # Convert temperatures from Kelvin to Celsius and provide station name, weather information, and temperature.
    if response.status_code == 200:
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp'] - 273.15
        return f'Weer op {station_name}: {weather_description}, Temperatuur: {temperature:.2f}°C'
    else:
        return f'Fout bij het ophalen van de weergegevens voor {station_name}'

def toon_faciliteiten():
    geselecteerde_faciliteiten = []
    for idx in faciliteiten_lijst.curselection():
        geselecteerde_faciliteiten.append(faciliteiten_lijst.get(idx))
    faciliteiten_tekst.set(", ".join(geselecteerde_faciliteiten))

def toon_berichten():
    geselecteerd_station = station_var.get()
    berichten = haal_berichten_op_voor_station(geselecteerd_station)

    if berichten:
        geformatteerde_berichten = [f"{bericht[1]} - {bericht[0]}: {bericht[2]}" for bericht in berichten]
        berichten_tekst.set("\n".join(geformatteerde_berichten))
    else:
        berichten_tekst.set("Geen berichten beschikbaar voor dit station.")

def update_weerbericht():
    selected_station = station_var.get()
    weer_info = get_weather(selected_station)
    weer_label.config(text=weer_info)

root = tk.Tk()
root.title("Stationshalscherm")

img = tk.PhotoImage(file='c:/Emirh/Gebruikers/Downloads/ns-logo.png')

# Create a Label widget for the image
label_image = tk.Label(root, image=img)
label_image.pack()

station_var = tk.StringVar()
station_var.set("Arnhem")
station_menu = tk.OptionMenu(root, station_var, *stations)
station_menu.pack()

update_knop = tk.Button(root, text="Update Weer", command=update_weerbericht)
update_knop.pack()

faciliteiten_tekst = tk.StringVar()
faciliteiten_label = tk.Label(root, text="Beschikbare faciliteiten:")
faciliteiten_label.pack()
faciliteiten_lijst = tk.Listbox(root, height=5, selectmode=tk.MULTIPLE)
faciliteiten_lijst.insert(1, "OV-fietsen")
faciliteiten_lijst.insert(2, "Lift")
faciliteiten_lijst.insert(3, "Toilet")
faciliteiten_lijst.insert(4, "P+R")
faciliteiten_lijst.pack()

toon_faciliteiten_knop = tk.Button(root, text="Toon geselecteerde faciliteiten", command=toon_faciliteiten)
toon_faciliteiten_knop.pack()

faciliteiten_weergave = tk.Label(root, textvariable=faciliteiten_tekst)
faciliteiten_weergave.pack()



berichten_tekst = tk.StringVar()
berichten_label = tk.Label(root, text="Berichten:")
berichten_label.pack()
berichten_weergave = tk.Label(root, textvariable=berichten_tekst, wraplength=300)
berichten_weergave.pack()

toon_berichten_knop = tk.Button(root, text="Toon Berichten", command=toon_berichten)
toon_berichten_knop.pack()

weer_label = tk.Label(root, text="", wraplength=300)
weer_label.pack()

root.mainloop()
