##### app.py zum Laufen bringen: #####
Die Datei "app.py" ist das "backend" zu Testzwecken.
(bash)
python  app.py

Kann sein, dass du Fehler bekommst und Pakete nachinstallieren musst, 
die Datei sagt dir ja auch, was sie braucht: 

"from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import GPT2LMHeadModel, GPT2Tokenizer"

Wenn das skript erstmal läuft, lauscht es nach Aufforderungen des frontend.


##### backend testen #####
(neue eingabeaufforderung)

cd "Pfad zu erklartextgen/frontend"
npm install #installiert npm
npm run dev #startet das backend


##### alles im browser ansehen #####
Im browser auf http://localhost:5173/ gehen, dort siehst du, was das frontend so macht.
Ich habe stark gegen die größe von containern gekämft, vielleicht ist der code von 
OutputPage.vue und PromptPage.vue (im Ordner frontend/src) unnötig kompliziert...