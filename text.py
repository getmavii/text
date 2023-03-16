from flask import Flask
from flask import request
import requests
import justext
import metadata_parser

app = Flask(__name__)

@app.route("/")
def index():
  url = request.args.get("url")

  if url is None:
    return { "error": "No URL provided" }
  else:
    return parse(url)

def parse(url):
  response = requests.get(url)
  content = response.content

  text = parse_text(content)
  metadata = parse_metadata(url, content)

  return { "text": text, **metadata }

def parse_text(content):
  paragraphs = justext.justext(content, justext.get_stoplist("English"))
  text_paragraphs = [paragraph.text for paragraph in paragraphs if not paragraph.is_boilerplate]
  
  return "\n".join(text_paragraphs)

def parse_metadata(url, content):
  page = metadata_parser.MetadataParser(url=url, html=content)

  return {
    "url": page.get_discrete_url(),
    "title": page.get_metadata("title"),
    "site_name": page.get_metadata("site_name"),
    "description": page.get_metadata("description"),
    "image": page.get_metadata_link("image"),
    "keywords": page.get_metadata("keywords"),
    "author": page.get_metadata("author"),
  }