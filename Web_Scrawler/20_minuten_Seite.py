import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd


def get_infos(url):
    # Sende eine HTTP-Anfrage an die Webseite
    response = requests.get(url)

    # Überprüfe, ob die Anfrage erfolgreich war
    if response.status_code != 200:
        print(f"Fehler beim Abrufen der Webseite: {response.status_code}")
        return []

    # Parse den HTML-Inhalt der Seite
    soup = BeautifulSoup(response.text, 'html.parser')

    # Finde alle <a>-Tags und extrahiere die Links
    print(str(response.text))



get_infos("https://www.20min.ch/story/zuerich-der-mann-wollte-offensichtlich-juden-angreifen-103167044")