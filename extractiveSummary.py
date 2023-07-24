import spacy
import networkx as nx
import numpy as np

nlp = spacy.load("en_core_web_sm")

def summarize(text):    
    doc = nlp(text=text)

    # Split the text into individual sentences
    sentences = [sent.text.strip() for sent in doc.sents]

    # Create a list of stopwords
    stopwords = list(nlp.Defaults.stop_words)

    # Remove stopwords and punctuation, and lemmatize the remaining words
    lemmatized_sentences = []
    for sentence in sentences:
        words = []
        for word in nlp(sentence):
            if not word.is_stop and not word.is_punct:
                words.append(word.lemma_)
        lemmatized_sentences.append(" ".join(words))

    # Calculate the similarity matrix
    similarity_matrix = []
    for i in range(len(lemmatized_sentences)):
        row = []
        for j in range(len(lemmatized_sentences)):
            row.append(nlp(lemmatized_sentences[i]).similarity(nlp(lemmatized_sentences[j])))
        similarity_matrix.append(row)

    # Convert the similarity matrix to a graph
    graph = nx.from_numpy_array(np.array(similarity_matrix))

    # Calculate the PageRank scores
    scores = nx.pagerank(graph)

    # Sort the sentences by their scores and extract the top N sentences
    num_sentences = 3
    top_sentence_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:num_sentences]
    summary = [sentences[i] for i in top_sentence_indices]

    return summary