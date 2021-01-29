from flask import Flask, request, jsonify
from flask_cors import CORS
from wabot import WABot
import json

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['POST'])
def home():
  print(request.json)
  if request.method == 'POST':
    bot = WABot(request.json)
    return bot.processing()

if(__name__) == '__main__':
    app.run(host='185.22.64.75',port=8787,debug=False)