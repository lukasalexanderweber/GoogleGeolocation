# GoogleGeolocation

### Konzept
![Alt Text](https://github.com/lukasalexanderweber/GoogleGeolocation/blob/master/img/concept.PNG)

Aaaalso das Tool sollte wenn möglich eine kleine Oberfläche haben (hier mit ArcGIS zusammengeklatscht :D). Die CSV wird (evt mit numpy?) eingelesen und die Adresse extrahiert (als Ad-on könnte der Nutzer auch eine Reihenfolge von Feldern angeben die dann automatisch zu einer ganzen Adresse zusammengeführt werden -> "Straße" + "Hausnummer" + "PLZ" + "Ort")

Soweit ich weiß sind pro API-Key 5 Abfragen pro Sekund erlaubt und 2500 pro Tag. Das sollten wir berücksichtigen. Am besten benachrichtigt man den Nutzer, dass er das Tool am nächsten Tag nochmal laufen lassen soll und man skipt die Zeilen die schon Koordinaten haben (wäre jetzt meine erste Idee)
