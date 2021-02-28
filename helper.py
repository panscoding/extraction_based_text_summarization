#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
helper, including function:
create_dictionary_table
calculate_sentence_scores
calculate_average_score
get_article_summary
"""
# importing libraries
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import urllib.request
import bs4 as BeautifulSoup

def fetch_content_from_url(URL):
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

def create_dictionary_table(text_string) -> dict:
    """
    create a dictionary table from input text
    :param text_string:
    :return: frequency_table
    """
    # removing stop words, init the stop words set
    stop_words = set(stopwords.words("english"))

    words = word_tokenize(text_string)

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


def calculate_sentence_scores(sentences, frequency_table) -> dict:
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


def calculate_average_score(sentence_weight) -> int:
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


def get_article_summary(sentences, sentence_weight, threshold):
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


def run_article_summary(article):
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


