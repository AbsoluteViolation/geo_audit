import requests
import json
import os
from bs4 import BeautifulSoup

urls = [
        "https://gymbeam.sk/blog/fitness-recept-gyoza-knedlicky-s-kuracim-masom/",
        "https://gymbeam.sk/blog/ako-si-vybrat-protein-porovnanie-true-whey-just-whey-a-dalsich-gymbeam-bestsellerov/",
        "https://gymbeam.sk/blog/pilates-pre-zaciatocnikov-13-cvikov-na-spevnenie-core-a-uvolnenie-chrbta/",
        "https://gymbeam.sk/blog/ako-chudnut-s-ozempicom-ci-wegovy-bez-rizik-a-zbytocnych-chyb/",
        "https://gymbeam.sk/blog/cortisol-face-co-sposobuje-ranny-opuch-tvare-a-ako-sa-ho-zbavit/",
        "https://gymbeam.sk/blog/ako-nabrat-svaly-sprievodca-treningom-stravou-a-regeneraciou-s-jakubom-enzlom/",
        "https://gymbeam.sk/blog/online-kalkulacka-1rm-one-rep-max/"
       ]

for url in urls:

    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.find("h1").get_text(strip=True)

    article = soup.find("article")

    meta = soup.find("meta", attrs={"name": "description"})
    meta_description = meta["content"].strip() if meta and meta.get("content") else ""

    content_html = str(article)

    new_article = {
        "url": url,
        "title": title,
        "meta_description": meta_description,
        "content_html": content_html
    }

    file_path = "data/articles.json"

    # load articles alredy in file
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            print(data)
    else:
        data = {"articles": []}

    # check for non duplicate articles
    json_urls = [article["url"] for article in data["articles"]]

    if url not in json_urls:
        data["articles"].append(new_article)
        print("Článok pridaný.")
    else:
        print("Článok už existuje v JSON.")

#safe
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print("Uložené do articles.json")