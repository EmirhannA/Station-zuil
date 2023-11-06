import psycopg2
import csv
from datetime import datetime

conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="Emirhanakin2006!",
    host="localhost"
)
cursor = conn.cursor()

with open("feedback.csv", newline='') as file:
    reader = csv.reader(file)
    for row in reader:
        if len(row) == 5:  # 5 waarden beschikbaar zijn om uit te pakken
            bericht, datum_tijd, naam, station, status = row
            if status == "Nog niet gemodereerd":
                goedgekeurd = input(f"Bericht van {naam} op {station}:\n{bericht}\nGoedkeuren? (ja/nee): ")
                if goedgekeurd.lower() == "ja":
                    status = "Goedgekeurd"
                else:
                    status = "Afgekeurd"

                cursor.execute("INSERT INTO reiziger (naam, datum, station, bericht) VALUES (%s, %s, %s, %s)",
                               (naam, datum_tijd, station, bericht))
                conn.commit()

                datum_tijd_moderatie = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                emailadres = input("Voer het e-mailadres van de moderator in: ")
                naam = input("Naam van moderator: ")
                goedkeuring = (status == "Goedgekeurd")

                cursor.execute(
                    "INSERT INTO moderator (naam, datum_tijd, emailadres, goedkeuring) VALUES (%s, %s, %s, %s)",
                    (naam, datum_tijd_moderatie, emailadres, goedkeuring))
                conn.commit()

                row[4] = status

cursor.close()
conn.close()
