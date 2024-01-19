import psycopg2  # Importeer de psycopg2-module voor het werken met PostgreSQL
import csv # Importeer de CSV-module om met CSV-bestanden te werken
from datetime import datetime

# Dit is voor verbinding maken met de database
conn = psycopg2.connect(
    host="40.113.123.172",
    database="stationszuil",
    user="postgres",
    password="postgres",
    port="5432"
)
cursor = conn.cursor()

scheldwoorden = ["kanker", "fuck", "shit", "kaolo", "kut", "tering", "tyfus"] # Lijst van de scheldwoorden

# Hier word de feedback verwerkt uit het CSV-bestand
with open("feedback.csv", newline='') as file:
    reader = csv.reader(file)
    for row in reader:
        if len(row) == 5:  # Controleert of er 5 rijen zijn
            bericht, datum_tijd, naam, station, status = row

            print(f"Verwerken: {bericht}, {datum_tijd}, {naam}, {station}, {status}")

            if status == "Nog niet gemodereerd":
                goedgekeurd = "ja"  # Standaard goedkeuren
                for scheldwoord in scheldwoorden:   # Hier wordt een lus gestart om door elk scheldwoord in de lijst scheldwoorden te itereren.
                    if scheldwoord in bericht:      # Controleert of het huidige scheldwoord aanwezig is in het bericht.
                        goedgekeurd = "nee"         # Als een scheldwoord wordt gevonden, afkeuren

                print(f"Goedkeuren: {goedgekeurd}") # Status van bericht

                if goedgekeurd == "ja": # Code is goedgekeurd
                    cursor.execute("INSERT INTO reiziger (naam, datum, station, bericht) VALUES (%s, %s, %s, %s)",
                                   (naam, datum_tijd, station, bericht))
                    conn.commit()

                datum_tijd_moderatie = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                emailadres = input("Voer het e-mailadres van de moderator in: ")
                naam = input("Naam van moderator: ")
                goedkeuring = (goedgekeurd == "ja")

                print(f"Moderator: {emailadres}, {naam}, Goedkeuring: {goedkeuring}")

                if 'goedkeuring' in locals(): # Controle of de variable goedkeuring bestaat
                    row[4] = "Goedgekeurd" if goedkeuring else "Afgekeurd" # Als goedkeuring waar is, wordt goedgekeurd toegewezen aan row[4].

# Sluit de databaseverbinding
cursor.close()
conn.close()
