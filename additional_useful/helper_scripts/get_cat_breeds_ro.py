from bs4 import BeautifulSoup
import pandas as pd

import requests
from termcolor import colored

link = 'https://ro.wikipedia.org/wiki/List%C4%83_de_rase_de_pisici'
page = requests.get(link)

soup = BeautifulSoup(page.content, 'html.parser')
# print(soup.prettify())
# print(list(soup.children))

html = list(soup.children)[2]
body = list(html.children)[3]

# bc = body.find("div", {"id": "bodyContent"})
bc = body.find(class_="mw-parser-output")

print(bc)
breeds_list = []

ols = bc.find_all("ul")
for ol in ols:
    for item in ol.find_all("li")[:-1]:

        item_a = item.find("a")
        print("itema:", item_a)
        if item_a and item_a.text.lower() != "rase de pisici":
            breeds_list.append(item_a.text)

def preprocess_breed(raw_breed_text):
    result = raw_breed_text.split("#")[0].split("(")[0].replace("\u2060", "")
    result = result.lower()
    return result

def replace_ro_diacritics(text):
    replacements = {
        "ă": "a",
        "ţ": "t",
        "ț": "t", 
        "ş": "s",
        "ș": "s",
        "î": "i",
        "â": "a"
    }
    for key, value in replacements.items():
        text = text.replace(key, value)
    
    return text


breeds_list = [preprocess_breed(x) for x in breeds_list]
print("preprocessed:")
print(breeds_list)

extended_breeds_set = set(breeds_list)

for breed in breeds_list:
    w  = replace_ro_diacritics(breed)
    print(w)
    extended_breeds_set.add(replace_ro_diacritics(breed))

extended_breeds_list = list(extended_breeds_set)
extended_breeds_list.sort()
print(colored("extended breeds list:", "blue"), extended_breeds_list)

f_breeds = open("cat_breeds_list.txt", "w+")
for breed in breeds_list:
    f_breeds.write(breed + "\n")
f_breeds.close()

f_extended_breeds = open("extended_cat_breeds_list.txt", "w+")
for breed in extended_breeds_list:
    f_extended_breeds.write(breed + "\n")
f_extended_breeds.close()