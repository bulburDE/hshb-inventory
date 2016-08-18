# hshb-inventory
Python tool to help with documenting Hackerspace Inventory.

Ein Python Tool, um die Dokumentation der Geräte im Hackerspace zu erleichtern.
Entwickelt für die Kombination aus Dokuwiki und Yourls im Hackerspace Bremen.

## Systemvoraussetzungen
Benötigt **Python 2.7** mit wxPython 3.0.
Weitere benötigte Pakete können mit `pip install -r requirements.txt` installiert werden.

## Installation
Das Repository klonen oder herunterladen.

## Benutzung
Starten mit `python wxgui.py`.

### Erster Aufruf
Als erstes den Button **Login** drücken und die Yourls Signatur sowie Benutzername und Passwort fürs Wiki eintragen. Hier kann auch der Name der lokalen Datenbank-Datei eingetragen werden. Alle Angaben bis auf das Passwort werden gespeichert.

Über den Button **Teilweises Update** werden immer die nächsten 11 Inventarnummern geprüft und gegebenenfalls in die lokale DB eingetragen. Die Funktion **Komplettes Update** überprüft alle 9999 möglichen Inventarnummern und dauert entsprechend lange.

### Neuen Eintrag anlegen
Im oberen Bereich werden die Inventarnummer, der Titel für die Wikiseite und gegebenenfalls der Unterordner im Wiki eingetragen / ausgewählt. Der Eintrag wird über die Funktion **Neuen Eintrag anlegen** im Wiki angelegt und es wird ein Shortlink bei Yourls eingetragen.

### Etikett erstellen
Über den Button **Erzeuge Etikett* wird für den markierten Eintrag ein Eitkett erzeugt, auf dem der Titel, die Inventanummer und die Shorturl als Tet und als QR-Code zu finden sind.
