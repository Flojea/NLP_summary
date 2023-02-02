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
from urllib.request import urlopen
import re








def summarize_article(pop):
    # Specify url of the web page
    source = urlopen(pop).read()

    # Make a soup 
    soup = BeautifulSoup(source,'html.parser') 


    # Extract the plain text content from paragraphs
    paras = []
    for paragraph in soup.find_all('p'):
        paras.append(str(paragraph.text))

    # Extract text from paragraph headers
    heads = []
    for head in soup.find_all('span', attrs={'mw-headline'}):
        heads.append(str(head.text))

    # Interleave paragraphs & headers
    text = [val for pair in zip(paras, heads) for val in pair]
    text = ' '.join(text)

    # Drop footnote superscripts in brackets
    text = re.sub(r"\[.*?\]+", '', text)

    # Replace '\n' (a new line) with '' and end the string at $1000.
    text = text.replace('\n', '')
    
    
    # Specify the title of the Wikipedia page
    


    stop_words = set(stopwords.words("english"))
    words = word_tokenize(text)
    word_frequencies = {}
    for word in words:
        if word not in stop_words:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1
    sentences = sent_tokenize(text)
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
    st.title("Résumé de page wikipedia")
    pop = st.text_input("Entrez la page wikipedia :")
    if pop:
        result = summarize_article(pop)
        st.write("Résumé :")
        st.write(result)



if __name__ == '__main__':
    main()
