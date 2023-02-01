import streamlit as st
import requests
try:
    from bs4 import BeautifulSoup
except :
    from BeautifulSoup import BeautifulSoup 
import nltk
import heapq
from nltk.tokenize import word_tokenize, sent_tokenize
nltk.download('stopwords')
from nltk.corpus import stopwords
from urllib.parse import urlparse
nltk.download('punkt')




def summarize_article(url):
    dictionnaire = {"www.lemonde.fr":"article__paragraph", "www.lefigaro.fr":"fig-paragraph",
               "www.leparisien.fr":"paragraph text_align_left","www.lesechos.fr" : "sc-14kwckt-6 gPHWRV",
                "www.liberation.fr":"article_link","www.bbc.com":"ssrcss-1q0x1qg-Paragraph eq5iqo00",
                "www.lequipe.fr" :"Paragraph__content"}
    
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    if domain in dictionnaire:
        class_name = dictionnaire[domain]
        paragraphs = soup.find_all("p", class_=class_name)
    else:
    # handle the case where the domain is not in the dictionary
        paragraphs = []
    article_text = ""
    for paragraph in paragraphs:
        article_text += paragraph.get_text()
        
    stopwords_language = "french" if(".fr" in url or ".info" in url) else "english"
        
    stop_words = set(stopwords.words(stopwords_language))
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
expander = st.sidebar.expander("What is this?")
expander.write(
    """
This app allows users to view migration between states from 2018-2019.
Overall US plots all states with substantial migration-based relationships with other states.
Any other option plots only migration from or to a given state. This map will be updated
to show migration between 2019 and 2020 once new census data comes out.
Incoming: Shows for a given state, the percent of their **total inbound migration from** another state.
Outgoing: Shows for a given state, the percent of their **total outbound migration to** another state.
"""
)


if __name__ == '__main__':
    main()
