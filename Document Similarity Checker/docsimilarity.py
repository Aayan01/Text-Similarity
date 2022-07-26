# -*- coding: utf-8 -*-
"""DocSimilarity.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1JquXRA6inVMYVgVKaSmXgCCxZBxeRawN
"""

import nltk
from gensim import corpora, models, similarities
import numpy as np
from nltk.tokenize import word_tokenize, sent_tokenize

# function to open file & split sentences.


def openf(filename):
    file_doc = []
    with open(filename) as f:
        tokens = sent_tokenize(f.read())
        for line in tokens:
            file_doc.append(line)
    return file_doc


# Driver code
file_doc1 = []
file_doc2 = []

file_doc1 = openf('file1.txt')
file_doc2 = openf('file2.txt')  # create 2nd txt file
# word tokenization (NLTK)
gen_docs = [[w.lower() for w in word_tokenize(text)]
            for text in file_doc1]
# dictionary obj map each word to uniqueID (Gensim)
dictionary = corpora.Dictionary(gen_docs)
# Bag-of-Words
corpus = [dictionary.doc2bow(gen_doc) for gen_doc in gen_docs]
# TF-IDF
tf_idf = models.TfidfModel(corpus)
# Similarity Obj created to sort index matrix in workdir
sims = similarities.Similarity('workdir/', tf_idf[corpus],
                               num_features=len(dictionary))

# upadate existing dictionary-> include new words.
for line in file_doc2:
    query_doc = [w.lower() for w in word_tokenize(line)]
    query_doc_bow = dictionary.doc2bow(query_doc)
# perform a similarity query against the corpus
query_doc_tf_idf = tf_idf[query_doc_bow]
# get Avg similarity %
sum_of_sims = (np.sum(sims[query_doc_tf_idf], dtype=np.float32))
percentage_of_similarity = round(float((sum_of_sims / len(file_doc1)) * 100))
print(f'Similarity Percentage: {percentage_of_similarity}%')


""" Sample text: 
text_1: 
A human could easily determine that these 2 sentences convey a very similar meaning despite being written in 2 completely different formats; 
The intersection of the 2 sentences only has one word in common, "is", and it doesn't provide any insight into how similar the sentences. 
Nonetheless, we'd still expect a similarity algorithm to return a score that informs us that the sentences are very similar.
text_2:
Despite being written in quite different styles, a human might readily tell that these two statements mean the same thing. 
The intersection of the two sentences only contains the word "is" in common; this doesn't reveal anything about how similar the sentences are. 
However, we would still anticipate a similarity algorithm to provide us with a score indicating that the sentences are really similar.
text_3: 
This phenomenon describes what we'd refer to as semantic text similarity,
where we aim to identify how similar documents are based on the context of
each document. This is quite a difficult problem because of the complexities
that come with natural language.

output: text_1 vs text_2 => 28%
output: text_1 vs text_3 => 10%
output: text_2 vs text_3 => 20%
"""
