import time
import requests
import trafilatura
from trafilatura.settings import use_config
import metadata_parser
from flask import Flask
from flask import request
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

USER_AGENT = "Mozilla/5.0 (compatible; MaviiBot/1.0; +https://mavii.com/bots)"
TIMEOUT = 20

# Disable extraction timeout to fix "signal only works in the main thread" error
tconfig = use_config()
tconfig.set("DEFAULT", "EXTRACTION_TIMEOUT", "0")

app = Flask(__name__)

@app.route("/")
def index():
  url = request.args.get("url")
  includeSummary = request.args.get("summarize") == "true"

  if url:
    try:
      return parse(url, includeSummary)
    except Exception as e:
      print(e)
      return { "error": str(e) }
  else:
    return { "error": "No URL provided" }
  
@app.route("/status")
def status():
  return "ok"

def parse(url, includeSummary = False):
  start_time = time.time()
  headers = { "User-Agent": USER_AGENT }

  try:
    response = requests.get(url, headers=headers, timeout=TIMEOUT)
    response.raise_for_status()
  except requests.exceptions.Timeout:
    raise Exception("Timeout fetching page.")
  except requests.exceptions.RequestException as e:
    raise Exception("Error fetching page: " + str(e))

  html = response.content
  text = trafilatura.extract(html, config=tconfig)
  metadata = parse_metadata(url, html)

  page = { "text": text, **metadata }

  if includeSummary:
    page["summary"] = summarize(text)

  page["time"] = time.time() - start_time

  return page

def parse_metadata(url, html):
  page = metadata_parser.MetadataParser(url=url, html=html, search_head_only=False)

  return {
    "url": page.get_discrete_url(),
    "title": page.get_metadata("title"),
    "site_name": page.get_metadata("site_name"),
    "description": page.get_metadata("description"),
    "image": page.get_metadata_link("image"),
    "keywords": page.get_metadata("keywords"),
    "author": page.get_metadata("author"),
  }

def summarize(text, sentences_count=10, language="english"):
  stemmer = Stemmer(language)
  summarizer = Summarizer(stemmer)
  summarizer.stop_words = get_stop_words(language)

  parser = PlaintextParser.from_string(text, Tokenizer(language))
  sentences = summarizer(parser.document, sentences_count)

  return " ".join([str(sentence) for sentence in sentences])
