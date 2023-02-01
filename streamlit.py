import streamlit as st
import requests
from bs4 import BeautifulSoup
import nltk
import heapq
from nltk.tokenize import word_tokenize, sent_tokenize
nltk.download('stopwords')
from nltk.corpus import stopwords
from urlparse import urlparse




dictionnaire = {"www.lemonde.fr":"article__paragraph", "www.lefigaro.fr":"fig-paragraph",
               "www.leparisien.fr":"paragraph text_align_left","www.lesechos.fr" : "sc-14kwckt-6 gPHWRV",
                "www.liberation.fr":"article_link","www.bbc.com":"ssrcss-1q0x1qg-Paragraph eq5iqo00",
                "www.lequipe.fr" :"Paragraph__content"
              }

def summarize_article(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")
    if domain in dictionnaire:
        class_name = dictionnaire[domain]
        paragraphs = soup.find_all("p", class_=class_name)
    else:
    # handle the case where the domain is not in the dictionary
        paragraphs = []
    article_text = ""
    for paragraph in paragraphs:
        article_text += paragraph.get_text()
    if ".fr" in url:
        x="french"
    else :
        x = "english"


    stop_words = set(stopwords.words(x))
    words = word_tokenize(article_text)
    word_frequencies = {}
    for word in words:
        if word not in stop_words:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1
    sentences = sent_tokenize(article_text)
    sentence_scores = {}
    for sentence in sentences:
        for word in word_tokenize(sentence.lower()):
            if word in word_frequencies.keys():
                if len(sentence.split(' ')) < 30:
                    if sentence not in sentence_scores.keys():
                        sentence_scores[sentence] = word_frequencies[word]
                    else:
                        sentence_scores[sentence] += word_frequencies[word]
    summarized_sentences = heapq.nlargest(
    int(len(sentences) * 0.5), sentence_scores, key=sentence_scores.get)
    summary = ' '.join(summarized_sentences)
    return summary

def main():
    st.title("Résumé d'article en ligne")
    url = st.text_input("Entrez le lien de l'article :")
    if url:
        result = summarize_article(url)
        st.write("Résumé :")
        st.write(result)

if __name__ == '__main__':
    main()
