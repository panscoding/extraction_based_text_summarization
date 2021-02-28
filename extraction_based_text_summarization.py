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


def _fetch_content_from_url(URL):
    """
    fetching the content from the URL
    :param url:
    :return:
    """
    # fetching the content from the URL
    fetched_data = urllib.request.urlopen(URL)

    article_read = fetched_data.read()

    # parsing the URL content and storing in a variable
    article_parsed = BeautifulSoup.BeautifulSoup(article_read, 'html.parser')

    # returning <p> tags
    paragraphs = article_parsed.find_all('p')

    article_content = ''

    # looping through the paragraphs and adding them to the variable
    for p in paragraphs:
        article_content += p.text

    return article_content

def _create_dictionary_table(text_string) -> dict:
    """
    create a dictionary table from input text
    :param text_string:
    :return: frequency_table
    """
    # removing stop words, init the stop words set
    stop_words = set(stopwords.words("english"))

    words = word_tokenize(text_string)
    print("words: ", words)

    # reducing words to their root form
    stem = PorterStemmer()

    # creating dictionary for the word frequency table
    frequency_table = dict()
    for wd in words:
        wd = stem.stem(wd)
        if wd in stop_words: #skip stop word
            continue
        if wd in frequency_table:
            frequency_table[wd] += 1
        else:
            frequency_table[wd] = 1
    # for key in frequency_table:
    #     print(key, '->', frequency_table[key])
    return frequency_table


def _calculate_sentence_scores(sentences, frequency_table) -> dict:
    """
    algorithm for scoring a sentence by its words
    :param sentences:
    :param frequency_table:
    :return: sentence_weight
    """
    sentence_weight = dict()

    for sentence in sentences:
        sentence_wordcount = (len(word_tokenize(sentence)))
        sentence_wordcount_without_stop_words = 0
        for word_weight in frequency_table: # for each vale in dictionary
            if word_weight in sentence.lower():
                sentence_wordcount_without_stop_words += 1
                # print("word_weight: ", word_weight)
                # print("sentence", sentence)
                # print("sentence[:7]", sentence[:7])

                # add all word frequency, get first 7 character as the dic key
                if sentence[:7] in sentence_weight:
                    sentence_weight[sentence[:7]] += frequency_table[word_weight]
                else:
                    sentence_weight[sentence[:7]] = frequency_table[word_weight]
        # print("sentence_weight[sentence[:7]]", sentence_weight[sentence[:7]])
        sentence_weight[sentence[:7]] = sentence_weight[sentence[:7]] / sentence_wordcount_without_stop_words

    return sentence_weight


def _calculate_average_score(sentence_weight) -> int:
    """
    alculating the average score for the sentences
    :param sentence_weight:
    :return: average_score
    """
    sum_values = 0
    for entry in sentence_weight:
        sum_values += sentence_weight[entry]

    # getting sentence average value from source text
    average_score = (sum_values / len(sentence_weight))

    return average_score


def _get_article_summary(sentences, sentence_weight, threshold):
    """
    get the article summary. if the sentence weight great than threshold, then add to the summary.
    :param sentences:
    :param sentence_weight:
    :param threshold:
    :return:
    """
    sentence_counter = 0
    article_summary = ''

    for sentence in sentences:
        if sentence[:7] in sentence_weight and sentence_weight[sentence[:7]] >= (threshold):
            article_summary += " " + sentence
            sentence_counter += 1

    return article_summary


def _run_article_summary(article):
    #1 creating a dictionary for the word frequency table
    frequency_table = _create_dictionary_table(article)

    #2 tokenizing the sentences, split by period
    sentences = sent_tokenize(article)
    print("sentences: ", sentences)

    #3 algorithm for scoring a sentence by its words
    sentence_scores = _calculate_sentence_scores(sentences, frequency_table)
    print("sentence_scores: ", sentence_scores)
    # for key in sentence_scores:
    #     print(key, " --> ", sentence_scores[key])

    #4 getting the threshold
    threshold = _calculate_average_score(sentence_scores)
    print("threshold(average_score): ", threshold)

    #5 producing the summary
    # article_summary = _get_article_summary(sentences, sentence_scores, 1.5 * threshold)
    article_summary = _get_article_summary(sentences, sentence_scores, 1.0 * threshold)

    return article_summary

if __name__ == '__main__':
    # URL = 'https://en.wikipedia.org/wiki/20th_century'
    # article_content = _fetch_content_from_url(URL)

    article_content = "Junk foods taste good that’s why it is mostly liked by everyone of any age group especially kids and school going children. " \
                      "They generally ask for the junk food daily because they have been trend so by their parents from the childhood. " \
                      "They never have been discussed by their parents about the harmful effects of junk foods over health. " \
                      "According to the research by scientists, it has been found that junk foods have negative effects on the health in many ways."
    print("article_content: ", article_content)
    summary_results = _run_article_summary(article_content)
    print("summary_results: ", summary_results)

