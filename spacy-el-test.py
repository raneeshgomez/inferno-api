import spacy
import urllib.request
from bs4 import BeautifulSoup
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# ========================================================
# Extracting entities and retrieving WikiData KB IDs
# ========================================================

nlp = spacy.load("en_core_web_sm")
doc = nlp("Ada Lovelace was born in London")

# token level
for ent in doc.ents:
    print('Entity Name: ' + ent.text)
    print('Entity Type: ' + ent.label_)
    print('KB ID: ' + ent.kb_id_)

    # =================================================
    # Extracting text from the entity's Wiki page
    # =================================================

    url = "https://www.wikidata.org/wiki/" + ent.kb_id_
    print('=============================================================================================')
    print("Wiki of " + ent.text + ": " + url)
    print('=============================================================================================')
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html)

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract() # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    print(text)