from bs4 import BeautifulSoup
import re 

class Analyzer:
    def __init__(self,article):
        self.url = article.get("url", "")
        self.title = article.get("title", "")
        
        self.md = (article.get("meta_description") or "").strip()

        content_html = article.get("content_html") or ""
        self.soup = BeautifulSoup(content_html, "html.parser")
    
    def direct_answer(self,phrases):
        """
        Checks if there is forbiden phrases after header and content section in first 150 characters of article
        
        Args:
           phrases: list of forbiden phrases

        Returns:
            bool: True if first 150 characters doesnt contain forbiden phrases
        """
        article = self.soup.find("article")

        if article is None:
            return False
        
        text = article.get_text(separator=" ", strip=True).lower()

        header = self.soup.find("header", class_="entry-header")
        
        if header:
            header = header.get_text(separator=" ", strip=True).lower()
            #remove header
            text= text.replace(header,"").lower().strip()

        #if there is content div with links remove them
        div = self.soup.find("div", id="ez-toc-container")
        
        if text.startswith("obsah") and div:
            div = div.get_text(separator=" ", strip=True).lower()
            
            text = text.replace(div,"").strip()
        
        if len(text)>= 150 :
            first_150 = text[:150]
        else: 
            first_150 = text

        for phrase in phrases:
            if phrase.lower() in first_150.lower():
                return False
        return True

    def extract_main_term(self):
        """
        Finds possible main term of article. 
        Conditions: 1. If it is Fitness recept: remove Fitness recept:
                    2. Take everithing before ":","?" and "-" (if there are this sections)
                    3. If this substring contains () remove them -> it could be explanation of abbreviation
                    4. If name of article is question remove ?
        
        Returns:
            t: String of main term
        """
        
        t = self.title.strip()

        #delete preffix Fitness recept if there is one
        t = re.sub(r"^Fitness recept:\s*", "", t, flags=re.IGNORECASE)

        #delete part of string after : or - 
        if ":" in t:
            t = t.split(":", 1)[0].strip()
        if "–" in t:
            t = t.split("–", 1)[0].strip()
        if "?" in t:
            t = t.split("?",1)[0].strip()
        #delete parenthesis and everything between them like Online Kalkulacka 1RM (one rep max)
        t = re.sub(r"\s*\(.*?\)\s*", "", t).strip()

        #delete ? if its question
        t = t.rstrip("?").strip()

        return t.lower()


    def definition(self):
        """
        Finding definitions of words, what could possibly be main terms of article

        Using method extract_main_terms

        Returns:
            bool: True if article has definition of main term
        """
        article = self.soup.find("article")

        if article is None:
            return False
        
        text = self.soup.article.get_text(separator=" ", strip=True).lower()

        t = self.extract_main_term()

        if not t:
            return False

        pattern = re.compile(
        rf"\b{re.escape(t)}\b\s+(je|znamená|predstavuje)\b"
        )

        if pattern.search(text):
            return True

        return False

    def structured_headings(self,how_many_h2):
        """
        Checks if there is at least "how_many_h2" headings

        Args:
           how_many_h2 integer of occurences

        Returns:
            bool: True if article has >= "how_many_occurences" H2
        """
        h2_tags = self.soup.find_all("h2")
        count = len(h2_tags)

        if count < how_many_h2:
            return False
        return True

    def contains_facts(self, min_count):
        """
        Checks if there is at least min_count facts with numbers
        example: 2.5 gram is fact

        Args:
          min_count integer of occurences

        Returns:
            bool: True if article has >= min_count facts
        """
        text = self.soup.get_text(" ", strip=True).lower()

        #\d+\s?(mg|g|kg|%|kcal|ml|mcg|gramov|miligramov) -> finds only kg|mg.. not 5 mg
        #could find random occurences: "html5 garden" would be occurence in this regex pattern
        #2.5 mg or 2,5 mg (number is decimal) doesnt find this as fact and number
        
        #better regex pattern
        pattern = re.compile(
            r"\b\d+(?:[.,]\d+)?\s?(?:mg|g|kg|%|kcal|ml|mcg|gramov|miligramov)\b",
            flags=re.IGNORECASE
        )
        
        matches = pattern.findall(text)
        
        if len(matches) >= min_count:
            return True
        
        return False

    def citation_sources(self, phrases):
        """
        Checks if there are citations

        Args:
           phrases: list of phrases indicating citations section, or just citation

        Returns:
            bool: True if article has at least one citation
        """
        article = self.soup.find("article")

        if article is None:
            return False
        
        text = self.soup.article.get_text(separator=" ", strip=True).lower()
        
        for phrase in phrases:
            if phrase in text:
                return True
        return False

    def faq_section(self, phrases):
        """
        Checks if there is faq section

        Args:
           phrases: list of possible names for faq section

        Returns:
            bool: True if article has faq section
        """
        
        article = self.soup.find("article")

        if article is None:
            return False
        
        text = self.soup.article.get_text(separator=" ", strip=True).lower()
        
        #if there is phrase return True
        for phrase in phrases:
            if phrase in text:
                return True
            
        return False

    def contains_lists(self):
        """
        Checks if there is <ul> or <ol> EXCEPT content section after header if there is one

        Returns:
            bool: True if article has at least one <ul> or <ol> tag
        """
        soup_copy = BeautifulSoup(str(self.soup), "html.parser")

        article = soup_copy.find("article")

        if article is None:
            return False

        html_doc_article = soup_copy.article

        header = soup_copy.find("header", class_="entry-header")

        #remove header
        if header : header.decompose()
        
        #if there is content div with links remove them
        div = soup_copy.find("div", id="ez-toc-container")
        
        if div: div.decompose()
        
        if html_doc_article.find("ul") or html_doc_article.find("ol"):
            return True

        return False

    def contains_tables(self):
        """
        Checks if there is table

        Returns:
            bool: True if there is table
        """
        
        table = self.soup.find("table")

        if table is None:
            return False

        return True

    def adequate_length(self, word_count):
        """
        Checks if article has adequate legth

        Args:
           word_count: required length of article

        Returns:
            bool: True if article has more then word_count
        """
        article = self.soup.find("article")

        if article is None:
            return False

        text = self.soup.article.get_text(separator=" ", strip=True).lower()
        
        #Split to words
        words = text.split(" ")
        
        #print(text)
        #print("Dĺžka slov",len(words))
        
        if len(words) < word_count:
            return False
        
        return True

    def length_verify_md(self):
        """
        Checks if meta_description has between 120-160 characters

        Returns:
            bool: True if article has between 120-160 characters
        """
       
        if len(self.md) <= 120 or len(self.md) >= 160 :
            return False
    
        return True