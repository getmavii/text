# Mavii Text

Extract text and metadata from a URL.

## Setup

You can run the app directly with:

```bash
pip install -r requirements.txt
python -m nltk.downloader punkt

gunicorn app:app
```

Or you can use Docker:

```bash
docker compose up
```

## API

```bash
curl "http://localhost:8000/?url=https://www.newyorker.com/magazine/2022/10/10/are-you-the-same-person-you-used-to-be-life-is-hard-the-origins-of-you"
```

```json
{
  "author": "Cond\u00e9 Nast",
  "description": "Researchers have studied how much of our personality is set from childhood, but what you\u2019re like isn\u2019t who you are.",
  "image": "https://media.newyorker.com/photos/6335b75cb1854f1d3eb5bd74/16:9/w_1280,c_limit/221010_r41126.jpg",
  "keywords": "childhood,personality,relationships,experience,self,researchers",
  "site_name": "The New Yorker",
  "text": "I have few memories of being four[...]",
  "time": 0.45578718185424805,
  "title": "Are You the Same Person You Used to Be?",
  "url": "https://www.newyorker.com/magazine/2022/10/10/are-you-the-same-person-you-used-to-be-life-is-hard-the-origins-of-you"
}
```
