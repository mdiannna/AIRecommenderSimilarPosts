from bs4 import BeautifulSoup
import pandas as pd

import requests
from termcolor import colored

link = 'https://encycolorpedia.ro/named'
page = requests.get(link)

soup = BeautifulSoup(page.content, 'html.parser')
# print(soup.prettify())

html = list(soup.children)[1]

colors_list = []

# for item in soup.find_all(class_="ads-list-photo-item"):
ol = soup.find("ol")
for item in ol.find_all("li"):
    item_a = item.find_all("a")[0]
    colors_list.append(item_a.text)

def preprocess_color(raw_color_text):
    result = raw_color_text.split("#")[0].split("(")[0].replace("\u2060", "")
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


colors_list = [preprocess_color(x) for x in colors_list]
print("preprocessed:")
print(colors_list)

extended_colors_set = set(colors_list)

for color in colors_list:
    w  = replace_ro_diacritics(color)
    print(w)
    extended_colors_set.add(replace_ro_diacritics(color))

extended_colors_list = list(extended_colors_set)
extended_colors_list.sort()
print(colored("extended colors list:", "blue"), extended_colors_list)

f_colors = open("colors_list.txt", "w+")
for color in colors_list:
    f_colors.write(color + "\n")
f_colors.close()

f_extended_colors = open("extended_colors_list.txt", "w+")
for color in extended_colors_list:
    f_extended_colors.write(color + "\n")
f_extended_colors.close()