import json
from analyzer import * 
from reporter import *

def load_articles(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data["articles"]

def safe_check(output, fn, default=False, err_label=""):
    try:
        return fn()
    except Exception as e:
        # nech ti to nespadne a zároveň nech vidíš, čo sa stalo
        output["recomandations"] = (output.get("recomandations","") + f", ERROR({err_label}): {e}").strip()
        return default
    
articles = load_articles("data/articles_test.json")

outputs = []
for article in articles:
    analyzer = Analyzer(article)
    output = {"url": article["url"],
              "title": article["title"],
              "score": 0,
              "recomandations": ""
            }
    score = 0

    if safe_check(output, lambda: analyzer.direct_answer(["v tomto článku", "poďme sa pozrieť", "dozviete sa", "povieme si"]), err_label="direct_answer"):
        score += 1
        output["direct_answer"] = 1
    else:
        output["recomandations"] = output["recomandations"] + " " + "Na začiatok článku pridať konkrétne tvrdenie"
        output["direct_answer"] = 0

    if safe_check(output, lambda:analyzer.definition(), err_label="definiton"):
        score += 1
        output["definiton"] = 1
    else:
        output["recomandations"] = output["recomandations"] + ", " + "určte jasnú definíciu hlavného pojmu"
        output["definiton"] = 0

    if safe_check(output, lambda:analyzer.structured_headings(3),err_label="headings"):
        score += 1
        output["headings"] = 1
    else:
        output["recomandations"] = output["recomandations"] + ", " + "pridajte nádpisy" 
        output["headings"] = 0

    if safe_check(output, lambda:analyzer.contains_facts(3), err_label="facts"):
        score += 1
        output["facts"] = 1
    else:
        output["recomandations"] = output["recomandations"] + ", " + "doplňte číselné údaje"
        output["facts"] = 0

    if safe_check(output, lambda:analyzer.citation_sources(["zdroje", "references", "štúdie", "pubmed.ncbi.nlm.nih.gov", "examine.com"]),err_label="sources"):
        score += 1
        output["sources"] = 1
    else:
        output["recomandations"] = output["recomandations"] + ", " + "doplňte citácie"
        output["sources"] = 0

    if safe_check(output, lambda:analyzer.faq_section(["faq","často kladené otázky","otázky a odpovede"]),err_label="faq"):
        score += 1
        output["faq"] = 1
    else:
        output["recomandations"] = output["recomandations"] + ", " + "doplňte sekciu FAQ"
        output["faq"] = 0

    if safe_check(output, lambda:analyzer.contains_lists(), err_label="lists"):
        score += 1
        output["lists"] = 1
    else:
        output["recomandations"] = output["recomandations"] + ", " + "doplňte odrážkový alebo číselný zoznam"
        output["lists"] = 0

    if safe_check(output, lambda:analyzer.contains_tables(), err_label="tables"):
        score += 1
        output["tables"] = 1
    else:
        output["recomandations"] = output["recomandations"] + ", " + "pridajte tabuľku"
        output["tables"] = 0

    if safe_check(output, lambda:analyzer.adequate_length(500),err_label="lenght_ok"):
        score += 1
        output["length_ok"] = 1
    else:
        output["recomandations"] = output["recomandations"] + ", " + "pridajte zopár viet"
        output["length_ok"] = 0

    if safe_check(output, lambda:analyzer.length_verify_md(),err_label="meta_ok"):
        score += 1
        output["meta_ok"] = 1
    else:
        output["recomandations"] = output["recomandations"] + ", " + "pridajte meta popis"
        output["meta_ok"] = 0

    output["score"] = score
    
    if output["recomandations"].startswith(','):
        output["recomandations"] = output["recomandations"][1:].strip()
        output["recomandations"] = output["recomandations"][0].upper() + output["recomandations"][1:].strip() + "."
    
    print(output)

    outputs.append(output)

reporter = Reporter(outputs)
reporter.outputs_to_csv()
reporter.outputs_to_html()
#    print(article["title"])
#    print("1. direct_answer:", analyzer.direct_answer(["v tomto článku", "poďme sa pozrieť", "dozviete sa", "povieme si"]))
#    print("2. definition:", analyzer.definition())
#    print("3. structured_headings:", analyzer.structured_headings(3))
#    print("4. contain_facts:", analyzer.contains_facts(3))
#    print("5. citation_sources:", analyzer.citation_sources(["zdroje", "references", "štúdie", "pubmed.ncbi.nlm.nih.gov", "examine.com"]))
#    print("6. faq_section:", analyzer.faq_section(["faq","často kladené otázky","otázky a odpovede"]))
#    print("7. contains_list:", analyzer.contains_lists())
#    print("8. contains_table:", analyzer.contains_tables())
#    print("9. adequate_length:", analyzer.adequate_length(500))
#    print("10. length_verify_md:", analyzer.length_verify_md())
#    
#    #print(article["content_html"])