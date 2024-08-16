import requests
from bs4 import BeautifulSoup
import psycopg2 as db
import time
import json




class DB_Connection():
    def __init__(self):
        self.db_connection = None
        self.db_cursor = None

    def make_DB_connection(self):
        connection_established = False
        while not connection_established:
            try:
                self.db_connection = db.connect(dbname="postgres", user="postgres",
                                                password="vQVXEEnnhC", host="100.106.239.63", port="5433")
                self.db_cursor = self.db_connection.cursor()
                connection_established = True
            except:
                print("Connection_Failed")
                time.sleep(5)

    def close_DB_connection(self):
        self.db_cursor.close()
        self.db_connection.close()

    def log_data(self, eingangsleistung, ausgangsleistung, status, zeit):
        self.make_DB_connection()
        self.db_cursor.execute("INSERT INTO Solaranlage1 (eingangsleistung, ausgangsleistung, status, zeit) VALUES (%s, %s, %s, %s)", (eingangsleistung, ausgangsleistung, status, zeit))
        self.db_connection.commit()
        self.close_DB_connection()


    def read_solar(self):
        # URL der Webseite
        url = 'http://192.168.0.194/api/dxs.json?dxsEntries=33556736&dxsEntries=67109120&dxsEntries=16780032'

        # HTTP-Anfrage an die Webseite senden
        response = requests.get(url)
        # Überprüfen, ob die Anfrage erfolgreich war (Statuscode 200)
        if response.status_code == 200:
            # HTML-Inhalt der Seite parsen
            soup = BeautifulSoup(response.content, 'html.parser')

            data = json.loads(soup.text)
            dxs_entries = data['dxsEntries']
            np_list = []
            # Loop through each entry and print the dxsId and value
            for entry in dxs_entries:
                value = entry['value']
                np_list.append(value)

            return np_list[0], np_list[1], np_list[2], time.strftime('%Y-%m-%d %H:%M:%S')


        else:
            print(f"Fehler beim Abrufen der Webseite: {response.status_code}")



def main():
    while True:
        db_connection = DB_Connection()
        eingangsleistung, ausgangsleistung, status, zeit = db_connection.read_solar()
        db_connection.log_data(eingangsleistung, ausgangsleistung, status, zeit)
        time.sleep(10)

main()