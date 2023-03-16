from flask import Flask
from flask import request
import requests
import justext

app = Flask(__name__)

@app.route("/")
def index():
  url = request.args.get("url")

  if url is None:
    return { "error": "No URL provided" }
  else:
    return { "text": get_text(url) }

def get_text(url):
  response = requests.get(url)
  paragraphs = justext.justext(response.content, justext.get_stoplist("English"))
  text_paragraphs = [paragraph.text for paragraph in paragraphs if not paragraph.is_boilerplate]

  # Join paragraphs together
  return "\n".join(text_paragraphs)
