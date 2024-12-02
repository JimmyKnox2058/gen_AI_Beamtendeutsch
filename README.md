# Generative KI für Beamtendeutsch
## Kurzbeschreibung des Projekts
Das Projekt ist ein Lernprojekt von [Michael Heinrich](https://github.com/JimmyKnox2058), dessen Inhalt die Entwicklung eines neuronalen Netzes (NN), für die Generierung von kurzen Textfragmenten mit ca. 50 Tokens (Wörter und Satzzeichen). Der generierte Text soll in der gleichen Schreibweise wie das *gemeinsame Ministerialblatt* - kompliziert, verklausuliert, juristisch - geschrieben sein. Der generierte Text hat dabei *nicht* den Anspruch *thematisch sinnvoll* zu sein. Entsprechend wurden als Vorlage Ausgaben des *gemeinsamen Ministerialblattes* zum Lernen genommen. Die *gemeinsamen Ministerialblätter* sind die seit 1950 von der Bundesregierung Deutschlands herausgegebenen Verwaltungsanweisungen - diese wurden auf der Website fragdenstaat.de als .pdf veröffentlicht. Die juristischen Zusammenhänge dazu werden auf ihrer Webseite, sowie Wikipedia und anderen Nachrichtenmedien veröffentlicht.
Diese Verwaltungsanweisungen sind juristische Texte und geben den Beamten in den Behörden Anweisungen, wie neue Gesetzesänderungen umzusetzen sind.

## Disclaimer:
### Dieses Projekt hat NICHT die Absicht neue Fake-Anweisungen zu generieren! Es soll zeigen, wie "KI" sich sehr spezifische Schreibstile aneignen und diese in neu generierten Text einsetzen kann. 

Aspekte des Projekts beinhalten:
- Den Text aus den PDFs semantisch in die richtige Reihenfolge bekommen. Auf Grund des Zwei-Spalten-Layout und der Quelle erwies sich das als umständlich. (Datacleaning)
- Die Daten für das Natural Language Processing (NLP) vorbereiten und tokenizing.
- Erstellen und trainieren des NN mit Long Short-Term Memory Layers (LSTM).
- Generierung von neuen Texten

## Sneak-Preview
- Die Anfänge, die KI lernt schreiben!
1. 'monatlichen anderung in der bundesfernstraßenverwahung in der bundespolizei = = = = = = = = = = = = = = = = ='

2.  ![Screenshot (41)](https://github.com/user-attachments/assets/aad05da0-dfbf-47dd-89f8-37ead3c3ceff)
3.  ![Screenshot (42)](https://github.com/user-attachments/assets/81f60d55-a9a3-4365-a09f-38034deeaf49)
4.  ![Screenshot (43)](https://github.com/user-attachments/assets/3ed63dba-d9e4-4aa8-ae0d-40f508878e40)

## Technischer Projektablauf
### Datenbeschaffung ist von dem vorherigen Projekt https://github.com/JimmyKnox2058/gem_minis_blatt
### Datacleaning
Für Details bitte in der Powerpoint-Präsentation nachschlagen.
Die von Fragdenstaat.de hinterlegten Textdaten, neben den PDFs, enthalten den Text zeilenweise. Wegen des Zwei-Spalten-Layouts ergeben Zeilen für einen Programm keinen Sinn und einen Parser dafür zu schreiben ist zu umständlich wegen der Unregelmäßigkeiten der Dokumente.
Verschiedene Python PDFreader Bibliotheken erwiesen sich, aufgrund der Datenqualität der PDFs, als äußerst langsam. Deswegen wurde mit Tesseract von der Uni Mannheim gearbeitet, welches ein für deutsche Zeitungen und juristischen Schriften optimiertes OCR-Programm ist. Dieses benutzt ein NN für die Erkennung und hat dank der Ausnutzung aller 24 Threads meiner CPU in nur 3 Stunden 379 PDF's erfolgreich in nutzbare (cleaned) Textsegmente umgewandelt. Leider stellte sich später heraus, dass die OCR-Fehler zu gravierend waren und dies meine "KI" verwirrt hat. Danach wurde auf py_pdf_parser zurückgegriffen, die Anzahl der Dokumente auf 62 verringert. Den Text zu extrahieren dauerte mehr als 2x 3 Stunden, trotz Multiprocessing.

Zum Vergleich:
- pytesseract OCR: 379 Ausgaben, preprocessed Textlänge 2.867.462 mit 187.296 verschiedenen Token (Wörter und Satzzeichen)
- py_pdf_parser: 62 Ausgaben, preprocessed Textlänge 422.399 mit 35743 verschiedenen Token
- Auch mit vielen Neologismen für neue Gesetze, ist bei den 187.296 Tokens davon auszugehen, dass mindestens die Hälfte davon OCR-Fehler sind.
### NLP
Für das nötige Tokenizing wurde Spacy benutzt. Wörter und Satzzeichen werden in Zahlen codiert, damit die "KI" damit rechnen kann.
### NN
Es handelt sich um ein sehr einfaches NN:
- Sequential
- Embedding
- Long Short-Term Memory layer (LSTM)
- Long Short-Term Memory layer (LSTM)
- Dense with relu
- Dense with softmax
- compile with loss='sparse_categorical_crossentropy',optimizer='adam',metrics=['accuracy']
- Das NN sieht einen 50 Token langen Ausschnitt aus dem Text und soll das darauf folgende Wort erraten und lernt dabei.
#### Beispiel eines Tests mit kleinerer Datenmenge (siehe Präsentation Seite 16)
![image](https://github.com/user-attachments/assets/9164db72-f407-416a-b073-0a4ac614977d)
In diesem Fall hätte die "KI" bei 200 Epochen den Text fast auswendig gelernt und wird kaum neuen Texte generieren.

### Generierung von neuen Texten
Um die "KI" nicht zu verwirren, wird eine ihr bekannte Textsequenz von 50 Token gezeigt, worauf diese mit einer guten, aber nicht 100% Chance das 51. Token errät. Bei der neuen Sequenz von 51 Token wird das erste entfernt, die 49 alten Token + 1 generiertes Token werden der "KI" wieder gezeigt, bis keine alten Tokens in der Sequenz sind und alle 50 neu generierte Tokens sind.
Wie im Sneak-Preview gezeigt, kommt es zu Wiederholungen von Tokens, ein "," kommt häufig in Texten vor. Entsprechend ist "," eine hohe Wahrscheinlichkeit zugeordnet, und es kommt zu ", , , , , , , , ,". Dieses Problem wurde gelöst, indem ein Beam-Search-Algorithmus implementiert wurde. Es werden die 3 wahrscheinlichsten Token genommen und für diese das nachfolgende Token gesucht, entsprechend wieder mit den 3 wahrscheinlichsten Token. Somit wird das beste nächste (51.) UND übernächste Token (52.) gefunden, benutzt wird aber nur das nächste Token (51.). Für den aufmerksamen Entwickler klingt dies nach der 4-fachen Rechenzeit. Nimmt man beide, würde man die Rechenzeit nur verdoppeln, leider funktioniert dann das System mit Beam Search nicht mehr gut und die Folgen ", . , . , . , . , ." oder ", . . , , . . ," wären möglich.
Dies war auch ein lustiges Ergebnis während der Implementierung des beam_search
![image](https://github.com/user-attachments/assets/ccb3608a-15c2-4f09-9d0f-abaa30d8a560)

## Kommentare
Die Links am Ende der Präsentation führen zu verschiedenen Versionen des Projekts, die inzwischen leider nicht mehr ausführbar sind. Vermutete Ursache nach debugging: Änderungen im Docker-image von Seiten Kaggle.
In den ipynb auf Kaggle konnte man selbst, verschiedene Modelle ausprobieren und neue Texte generien lassen. Das Projekt wird aber hier in kleinerer Version hochgestellt.

### selbst ausprobieren?
den Ordner für das "interaktive" ipynb runter laden, requirements.txt und los geht's!
