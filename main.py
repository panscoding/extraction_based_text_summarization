#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This is a text summarization code using simple extraction method.
Please install nltk and bs4 using pip.
1. error： ssl.SSLError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:847)
https://stackoverflow.com/questions/41691327/ssl-sslerror-ssl-certificate-verify-failed-certificate-verify-failed-ssl-c

2. error: Resource stopwords not found.
    Please use the NLTK Downloader to obtain the resource:
    >>> import nltk
    >>> nltk.download('stopwords')

3. error:Resource punkt not found.
    Please use the NLTK Downloader to obtain the resource:
    >>> import nltk
    >>> nltk.download('punkt')

A Survey on Text Simplification: https://arxiv.org/pdf/2008.08612.pdf
"""
# importing libraries
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import urllib.request
import bs4 as BeautifulSoup
from helper import fetch_content_from_url, create_dictionary_table, calculate_sentence_scores, calculate_average_score, get_article_summary

def _run_article_summary(article):
    #1 creating a dictionary for the word frequency table
    frequency_table = create_dictionary_table(article)

    #2 tokenizing the sentences, split by period
    sentences = sent_tokenize(article)
    # print("sentences: ", sentences)

    #3 algorithm for scoring a sentence by its words
    sentence_scores = calculate_sentence_scores(sentences, frequency_table)
    # print("sentence_scores: ", sentence_scores)
    # for key in sentence_scores:
    #     print(key, " --> ", sentence_scores[key])

    #4 getting the threshold
    threshold = calculate_average_score(sentence_scores)
    # print("threshold(average_score): ", threshold)

    #5 producing the summary
    # article_summary = _get_article_summary(sentences, sentence_scores, 1.5 * threshold)
    article_summary = get_article_summary(sentences, sentence_scores, 1.0 * threshold)

    return article_summary

if __name__ == '__main__':
    # URL = 'https://en.wikipedia.org/wiki/21th_century'
    # article_content = fetch_content_from_url(URL)

    article_content = "Junk foods taste good that’s why it is mostly liked by everyone of any age group especially kids and school going children. " \
                      "They generally ask for the junk food daily because they have been trend so by their parents from the childhood. " \
                      "They never have been discussed by their parents about the harmful effects of junk foods over health. " \
                      "According to the research by scientists, it has been found that junk foods have negative effects on the health in many ways."
    print("article_content: ", article_content)
    summary_results = _run_article_summary(article_content)
    print("summary_results: ", summary_results)

