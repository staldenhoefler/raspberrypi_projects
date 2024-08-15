import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import psycopg2 as db
import time
import os


class DB_Connection():
    def __init__(self):
        self.db_connection = None
        self.db_cursor = None

    def make_DB_connection(self):
        connection_established = False
        while not connection_established:
            try:
                self.db_connection = db.connect(dbname="zwanzigminuten", user="postgres", password="vQVXEEnnhC",
                                                host="100.106.239.63", port="5433")
                self.db_cursor = self.db_connection.cursor()
                connection_established = True
            except:
                print("Connection_Failed")
                time.sleep(5)

    def close_DB_connection(self):
        self.db_cursor.close()
        self.db_connection.close()

    def log_data(self, url, html):
        self.make_DB_connection()
        self.db_cursor.execute("INSERT INTO htmlraw (url, html) VALUES (%s, %s)",(url, html))
        self.db_connection.commit()
        self.close_DB_connection()




def get_all_links(url):
    # Sende eine HTTP-Anfrage an die Webseite
    response = requests.get(url)

    # Überprüfe, ob die Anfrage erfolgreich war
    if response.status_code != 200:
        print(f"Fehler beim Abrufen der Webseite: {response.status_code}")
        return []

    # Parse den HTML-Inhalt der Seite
    soup = BeautifulSoup(response.text, 'html.parser')

    # Finde alle <a>-Tags und extrahiere die Links
    links = set()
    for a_tag in soup.find_all('a', href=True):
        href = a_tag.get('href')
        # Konvertiere relative Links zu absoluten URLs
        if href.startswith('/story'):
            full_url = urljoin(url, href)
            links.add(full_url)

    return links


def save_links_to_file(links, filename):
    # Neue Links anfügen wenn der Link noch nicht in der Datei ist
    neue_links = []
    if os.access(filename, os.F_OK):
        with open(filename, 'a') as f:
            for link in links:
                if link not in open(filename).read():
                    f.write(link + '\n')
                    neue_links.append(link)
        f.close()
    else:
        raise ValueError('Fehler beim Zugriff auf die Datei')

    return neue_links



def get_html(url):
    # Sende eine HTTP-Anfrage an die Webseite
    response = requests.get(url)

    # Überprüfe, ob die Anfrage erfolgreich war
    if response.status_code != 200:
        print(f"Fehler beim Abrufen der Webseite: {response.status_code}")
        return []

    # Parse den HTML-Inhalt der Seite
    soup = BeautifulSoup(response.text, 'html.parser')

    return response.text

# Hauptfunktion
if __name__ == "__main__":
    # Die URL, von der die Links extrahiert werden sollen
    start_url = "https://www.20min.ch/"
    while True:
        # Extrahiere alle Links von der Startseite
        links = get_all_links(start_url)

        # Speichere die Links in einer Datei
        neue_links = save_links_to_file(links, 'extracted_links.txt')
        print(f'Anzahl neuer Links: {len(neue_links)}')
        db_connection = DB_Connection()

        for link in neue_links:
            html = get_html(link)
            url = link
            db_connection.log_data(url, html)
            time.sleep(1)
            print(f'Gespeichert: {link}')

        time.sleep(900)

