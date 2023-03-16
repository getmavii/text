from flask import Flask
from flask import request
import time
import requests
import justext
import metadata_parser

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

import nltk

# Make sure punkt is downloaded
nltk.download("punkt")

# Setup summarizer
LANGUAGE = "english"
stemmer = Stemmer(LANGUAGE)
summarizer = Summarizer(stemmer)
summarizer.stop_words = get_stop_words(LANGUAGE)

app = Flask(__name__)

@app.route("/")
def index():
  url = request.args.get("url")
  includeSummary = request.args.get("summarize") == "true"

  if url is None:
    return { "error": "No URL provided" }
  else:
    return parse(url, includeSummary)

def parse(url, includeSummary = False):
  start_time = time.time()
  response = requests.get(url)
  html = response.content

  text = parse_text(html)
  metadata = parse_metadata(url, html)

  page = { "text": text, **metadata }

  if includeSummary:
    page["summary"] = summarize(text)

  page["time"] = time.time() - start_time

  return page

def parse_text(html):
  paragraphs = justext.justext(html, justext.get_stoplist("English"))
  text_paragraphs = [paragraph.text for paragraph in paragraphs if not paragraph.is_boilerplate]
  
  return "\n\n".join(text_paragraphs)

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

def summarize(text, sentences_count=10):
  parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))
  sentences = summarizer(parser.document, sentences_count)

  return " ".join([str(sentence) for sentence in sentences])
