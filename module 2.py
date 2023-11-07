import psycopg2
import csv
from datetime import datetime

# Verbinding maken met de database
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="Emirhanakin2006!",
    host="localhost"
)
cursor = conn.cursor()

scheldwoorden = ["kanker", "fuck", "shit", "kaolo", "kut", "tering", "tyfus"]

# Verwerk feedback uit het CSV-bestand
with open("feedback.csv", newline='') as file:
    reader = csv.reader(file)
    for row in reader:
        if len(row) == 5:  # 5 waarden beschikbaar zijn om uit te pakken
            bericht, datum_tijd, naam, station, status = row

            print(f"Verwerken: {bericht}, {datum_tijd}, {naam}, {station}, {status}")

            if status == "Nog niet gemodereerd":
                goedgekeurd = "ja"  # Standaard goedkeuren
                for scheldwoord in scheldwoorden:
                    if scheldwoord in bericht:
                        goedgekeurd = "nee"  # Als een scheldwoord wordt gevonden, afkeuren

                print(f"Goedkeuren: {goedgekeurd}")

                cursor.execute("INSERT INTO reiziger (naam, datum, station, bericht) VALUES (%s, %s, %s, %s)",
                               (naam, datum_tijd, station, bericht))
                conn.commit()

                datum_tijd_moderatie = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                emailadres = input("Voer het e-mailadres van de moderator in: ")
                naam = input("Naam van moderator: ")
                goedkeuring = (goedgekeurd == "ja")

                print(f"Moderator: {emailadres}, {naam}, Goedkeuring: {goedkeuring}")

                cursor.execute(
                    "INSERT INTO moderator_beoordeling (datum_tijd, goedkeuring) VALUES (%s, %s)",
                    (datum_tijd_moderatie, goedkeuring))
                conn.commit()

                row[4] = "Goedgekeurd" if goedkeuring else "Afgekeurd"

# Sluit de databaseverbinding
cursor.close()
conn.close()
