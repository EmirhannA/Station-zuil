import csv
import random
from datetime import datetime

stations = ['Utrecht', 'Arnhem', 'Almere', 'Amersfoort', 'Breda', 'Amsterdam', 'Den Haag', 'Gouda', 'Rotterdam', 'Hilversum']

naam = input("Voer uw naam in (laat leeg voor anoniem): ")
bericht = input("Voer uw bericht in (maximaal 140 karakters): ")

if len(bericht) > 140:
    print("Het bericht mag maximaal 140 karakters bevatten.")
else:
    station = random.choice(stations)
    datum_tijd = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if not naam:
        naam = "anoniem"

    with open("feedback.csv", mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([bericht, datum_tijd, naam, station, "Nog niet gemodereerd"])



