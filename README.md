# generative KI für Beamtendeutsch
## Kurzbeschreibung des Projekts
Das Projekt ist ein Lernprojekt von [Michael Heinrich](https://github.com/JimmyKnox2058), dessen Inhalt die Entwicklung eines neuronalen Netzes (NN), für die Generierung von kurzen Text Fragmenten mit ca. 50 Tokens (Worten und Satzzeichen). Der generierte Text hat *nicht* den Anspruch *thematisch sinnvoll* zu sein, soll aber in der kompliziert verklausulierten juristischen Schreibweise, mit bezug auf Gesetze sein. Entsprechend wurden als Vorlage zum lernen, Ausgaben des *gemeinsamen Ministerialblattes* genommen. Die *gemeinsamen Ministerialblätter* sind die seit 1950 von der Bundesregierung Deutschlands herausgegebenen Verwaltungsanweisungen - diese wurden auf der Website fragdenstaat.de als .pdf veröffentlicht. Die juristischen Zusammenhänge dazu werden auf ihrer Webseite, sowie Wikipedia und anderen Nachrichtenmedien veröffentlicht.
Diese Verwaltungsanweisungen sind juristische Texte und geben den Beamten in den Behörden die Anweisung, wie neue Gesetzesänderungen umzusetzten sind.

## Disclaimer:
### Es ist NICHT die Absicht, damit neue Fake Anweisungen zu generieren! Es soll zeigen, wie "KI" sich sehr spezifische Schreibstile aneigenen kann und diese in neu generierten Text einsetzen kann. 

Aspekte des Projekts beinhalten:
- Den Text aus den PDF's sematisch in die richtige Reihenfolge bekommen, welche bei dem zwei Spalten Layout und der bezogenen Quelle umständlich war. (Datacleaning)
- Für das Neural Language Processing (NLP) vorbereiten und tokenizing.
- Erstellen und trainieren des NN mit Long Short-Term Memory layer (LSTM).
- Generierung von neuen Texten

## 
