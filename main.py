import csv  # Heb dit geimporteerd om een csv bestand te openen
import random
from datetime import datetime

stations = ['Utrecht', 'Arnhem', 'Rotterdam']

naam = input("Voer uw naam in (laat leeg voor anoniem): ") # Vraag de gebruiker om hun naam in te voeren
bericht = input("Voer uw bericht in (maximaal 140 karakters): ") # Vraag de gebruiker om hun feedback in te voeren

if len(bericht) > 140: # Controleer of het bericht niet langer is dan 140 karakters
    print("Het bericht mag maximaal 140 karakters bevatten.")
else:
    station = random.choice(stations) # Een random station uit de lijst word gekozen
    datum_tijd = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # de huidige datum en tijd op van de bericht
    if not naam: # Als naam niet word doorgegeven dan word de gebruiker zijn naam anoniem
        naam = "anoniem"

    with open("feedback.csv", mode='a', newline='') as file: # Het CSV-bestand word geopend als 'a' dat staat voor toevoegen
        writer = csv.writer(file)
        writer.writerow([bericht, datum_tijd, naam, station, "Nog niet gemodereerd"]) # De gegevens word gestuurd naar het CSV-bestand



