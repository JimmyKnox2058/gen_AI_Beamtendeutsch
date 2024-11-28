# work in progress
# generative KI für Beamtendeutsch
## Kurzbeschreibung des Projekts
Das Projekt ist ein Lernprojekt von [Michael Heinrich](https://github.com/JimmyKnox2058), dessen Inhalt die Entwicklung eines neuronalen Netzes (NN), für die Generierung von kurzen Text Fragmenten mit ca. 50 Tokens (Worten und Satzzeichen). Der generierte Text hat *nicht* den Anspruch *thematisch sinnvoll* zu sein, soll aber in der kompliziert verklausulierten juristischen Schreibweise, mit Bezug auf Gesetze sein. Entsprechend wurden als Vorlage zum lernen, Ausgaben des *gemeinsamen Ministerialblattes* genommen. Die *gemeinsamen Ministerialblätter* sind die seit 1950 von der Bundesregierung Deutschlands herausgegebenen Verwaltungsanweisungen - diese wurden auf der Website fragdenstaat.de als .pdf veröffentlicht. Die juristischen Zusammenhänge dazu werden auf ihrer Webseite, sowie Wikipedia und anderen Nachrichtenmedien veröffentlicht.
Diese Verwaltungsanweisungen sind juristische Texte und geben den Beamten in den Behörden die Anweisung, wie neue Gesetzesänderungen umzusetzen sind.

## Disclaimer:
### Es ist NICHT die Absicht, damit neue Fake Anweisungen zu generieren! Es soll zeigen, wie "KI" sich sehr spezifische Schreibstile aneignen kann und diese in neu generierten Text einsetzen kann. 

Aspekte des Projekts beinhalten:
- Den Text aus den PDF's semantisch in die richtige Reihenfolge bekommen, welche bei dem zwei Spalten Layout und der bezogenen Quelle umständlich war. (Datacleaning)
- Für das Natural Language Processing (NLP) vorbereiten und tokenizing.
- Erstellen und trainieren des NN mit Long Short-Term Memory Layer (LSTM).
- Generierung von neuen Texten

## Sneak-preview
- Die Anfänge, die KI lernt schreiben!
1. 'monatlichen anderung in der bundesfernstraßenverwahung in der bundespolizei = = = = = = = = = = = = = = = = ='

2.  ![Screenshot (41)](https://github.com/user-attachments/assets/aad05da0-dfbf-47dd-89f8-37ead3c3ceff)
3.  ![Screenshot (42)](https://github.com/user-attachments/assets/81f60d55-a9a3-4365-a09f-38034deeaf49)
4.  ![Screenshot (43)](https://github.com/user-attachments/assets/3ed63dba-d9e4-4aa8-ae0d-40f508878e40)

## Technischer Projektablauf
### Datenbeschaffung ist von dem vorherigen Projekt https://github.com/JimmyKnox2058/gem_minis_blatt
### Datacleaning
Für Details bitte in der Powerpoint Präsentation nachschlagen.
Die hinterlegten Textdaten von der Quelle, neben den PDFs, haben den Text zeilenweise enthalten, wegen dem zwei Spalten Layout ergibt es keinen Sinn und ein Parser dafür zu schreiben ist zu umständlich wegen der Unregelmäßigkeit der Dokumente.
Verschiedene Python PDFreader Bibliotheken, erwiesen sich als äußerst langsam, aufgrund der Datenqualität der PDFs. So wurde mit Tesseract von der Uni Mannheim gearbeitet, welches ein für deutsche Zeitungen und juristischen Schriften optimiertes OCR Programm ist. Dieses benutzt ein NN für die Erkennung und war dank der Ausnutzung aller 24 Threads meiner CPU in nur 3 Stunden 379 PDF's erfolgreich in nutzbare (cleaned) Textsegmente wandelte. Leider stellte sich später heraus, dass die OCR Fehler zu gravierend waren und dies meine "KI" verwirrt hat. Danach wurde auf py_pdf_parser zurückgegriffen, die Anzahl der Dokumente auf 62 verringert, den Text zu extrahieren dauerte mehr als 3 Stunden, trotz multiprocessing.

Zum Vergleich:
- pytesseract OCR: 379 Ausgaben, preprocessed Textlänge 2.867.462 mit 187.296 verschiedenen Token (Wörter und Satzzeichen)
- py_pdf_parser: 62 Ausgaben, preprocessed Textlänge 422.399 mit 35743 verschiedenen Token
- Auch mit viel Neologismus für neue Gesetze, ist bei den 187.296 Tokens davon auszugehen, dass mindestens die Hälfte davon, OCR Fehler sind.
### NLP
Für das nötige tokenizing, wurde Spacy benutzt. Wörter und Satzzeichen werden in Zahlen codiert, damit die "KI" damit rechnen kann.
### NN
Es handelt sich um sehr einfaches NN:
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
in diesem Fall, hätte die "KI" bei 200 Epochen, den Text fast auswendig gelernt und wird kaum neuen Texte generieren.

### Generierung von neuen Texten
Um die "KI" nicht zu verwirren, wird eine Ihr bekannte Text-Sequenz von 50 Token gezeigt, worauf diese, mit einer guten, aber nicht 100% Chance das 51 Token errät. Bei der neuen Sequenz von 51 Token wird das erste entfernt, die 49 alten Token + 1 generiertes Token werden der "KI" wieder gezeigt, bis keine alten Tokens in der Sequenz sind und alle 50 neu generierte Token sind.
Wie im Sneak-Preview gezeigt, kommt es zu Wiederholungen von Tokens, ein "," kommt häufig in Texten vor entsprechend ist diesem eine hohe Wahrscheinlichkeit gegeben, und es kommst zu ", , , , , , , , ,". Dieses Problem wurde gelöst, indem ein beam search Algorithmus implementiert wurde. Es werden die 3 wahrscheinlichsten Token genommen und für diese, das nachfolgende Token gesucht, entsprechend wieder mit den 3 wahrscheinlichsten Token. Somit wird das beste nächste UND übernächste Token gefunden, benutzt wird aber nur das nächste Token. Für den aufmerksamen Entwickler klingt dies nach der 4-fachen Rechenzeit, nimmt man beide, würde man die Rechenzeit nur verdoppeln, leider funktioniert dann das System mit den Gridsearch nicht mehr gut und die Folge ist ein ", . , . , . , . , ."
Dies war auch ein lustiges Ergebnis während der Implementierung des beam_search
![image](https://github.com/user-attachments/assets/ccb3608a-15c2-4f09-9d0f-abaa30d8a560)

## Kommentare
Die Links am Ende der Präsentation führen zu verschiedenen Versionen des Projekts, die inzwischen leider nicht mehr ausführbar sind. Vermutete Ursache nach debugging: Änderungen im Docker-image von Kaggle seitens.
Um etwas im ipynb rum klicken und verschiedene Modelle und andere seeds ausprobieren funktioniert dort nicht wird aber hier in kleiner Version hochgestellt.
TODO: 
Anleitung für ipynb schreiben
