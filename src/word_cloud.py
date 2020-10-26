from os import path
from pathlib import Path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os

from wordcloud import WordCloud, STOPWORDS

def generate_word_cloud(languages):

    text = ''
    path_up = str(Path(__file__).parents[1])

    if ("C#" in languages):
        text += open(path.join(path_up, 'Datasets/C#_text_commit.txt')).read()
    
    if ("C++" in languages):
        text += open(path.join(path_up, 'Datasets/C++_text_commit.txt')).read()

    if ("Java" in languages):
        text += open(path.join(path_up, 'Datasets/Java_text_commit.txt')).read()

    if ("JavaScript" in languages):
        text += open(path.join(path_up, 'Datasets/JavaScript_text_commit.txt')).read()
    
    if ("Python" in languages):
        text += open(path.join(path_up, 'Datasets/Python_text_commit.txt')).read()

    git_mask = np.array(Image.open(path.join(path_up, "src/git.png")))

    stopwords = set(STOPWORDS)
    stopwords.add("org")
    stopwords.add("ref")
    stopwords.add("refs")
    stopwords.add("heads")
    stopwords.add("Aug")
    stopwords.add("Oct")
    stopwords.add("Apr")
    stopwords.add("Mar")
    stopwords.add("May")
    stopwords.add("Sep")
    stopwords.add("Jun")
    stopwords.add("Nov")
    stopwords.add("Feb")
    stopwords.add("https")

    wc = WordCloud(width=800, height=800,scale=5, background_color="white", max_words=2000, mask=git_mask,
                stopwords=stopwords, contour_width=4, contour_color='orange', min_word_length=3, colormap='hot').generate(text)

    wc.to_file(path.join(path_up+"/src", "word-cloud.png"))
