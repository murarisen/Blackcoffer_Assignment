# -*- coding: utf-8 -*-
"""Blackcoffer_assignement.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1SsauS9ZkmfEKu7z0OMe81HjXFP0x-__e
"""

from google.colab import drive
drive.mount('/content/drive')

!unzip /content/drive/MyDrive/20211030 Test Assignment-20240906T171838Z-001/20211030 Test Assignment/MasterDictionary.zip

!unzip /content/drive/MyDrive/20211030 Test Assignment-20240906T171838Z-001/20211030 Test Assignment/StopWords.zip

# Install the required libraries
!pip install textstat beautifulsoup4 requests nltk openpyxl

import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
import textstat
import re
import pandas as pd
import os
import string

# Download necessary NLTK data
nltk.download('punkt')

# Function to load stopwords from all files in the StopWords folder with error handling
def load_stopwords(stopwords_folder):
    stop_words = set()
    try:
        for file_name in os.listdir(stopwords_folder):
            if file_name.endswith('.txt'):  # Only process text files
                file_path = os.path.join(stopwords_folder, file_name)
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                    for line in file:
                        stop_words.add(line.strip().lower())  # Add stopwords in lowercase
        print(f"Successfully loaded stopwords from {stopwords_folder}")
    except Exception as e:
        print(f"Error loading stopwords: {e}")
    return stop_words

# Load custom stop words from Google Drive folder
stopwords_folder = '/content/drive/MyDrive/20211030 Test Assignment-20240906T171838Z-001/20211030 Test Assignment/StopWords'
custom_stop_words = load_stopwords(stopwords_folder)

# Function to clean text by removing stop words
def clean_text(text, stop_words):
    words = word_tokenize(text)
    cleaned_words = [word for word in words if word.lower() not in stop_words]  # Remove stop words
    return cleaned_words

# Example text for cleaning
sample_text = "This is a sample sentence to test the removal of stop words."

# Clean the text using the custom stop words loader
cleaned_text = clean_text(sample_text, custom_stop_words)

# Example: Print the cleaned text
print("Original Text:", sample_text)
print("Cleaned Text:", cleaned_text)

# Load the Excel file
import pandas as pd
input_df = pd.read_excel('/content/drive/MyDrive/20211030 Test Assignment-20240906T171838Z-001/20211030 Test Assignment/Input.xlsx')

# Function to extract text from a URL
import requests
from bs4 import BeautifulSoup

def extract_text(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract title and article content (adjust the tags as per the website structure)
        title = soup.find('h1').text
        paragraphs = soup.find_all('p')
        article_text = ' '.join([para.text for para in paragraphs])

        return title, article_text
    except Exception as e:
        print(f"Error extracting {url}: {e}")
        return None, None

# Extract text for each URL
for index, row in input_df.iterrows():
    url_id = row['URL_ID']
    url = row['URL']

    title, article_text = extract_text(url)

    # Save the text in a file
    if title and article_text:
        with open(f"{url_id}.txt", "w") as file:
            file.write(title + "\n" + article_text)

# Load Positive and Negative words
positive_words = open('/content/drive/MyDrive/20211030 Test Assignment-20240906T171838Z-001/20211030 Test Assignment/MasterDictionary/positive-words.txt', 'r', encoding='utf-8', errors='ignore').read().splitlines()
negative_words = open('/content/drive/MyDrive/20211030 Test Assignment-20240906T171838Z-001/20211030 Test Assignment/MasterDictionary/negative-words.txt', 'r', encoding='utf-8', errors='ignore').read().splitlines()

# Load stopwords for cleaning
stop_words = set(stopwords.words('english'))

# Function to clean text
def clean_text(text):
    text = text.lower()  # convert to lowercase
    text = text.translate(str.maketrans('', '', string.punctuation))  # remove punctuation
    words = word_tokenize(text)
    words = [word for word in words if word not in stop_words]  # remove stopwords
    return words

# Function to compute sentiment scores
def sentiment_analysis(text):
    words = clean_text(text)

    positive_score = sum(1 for word in words if word in positive_words)
    negative_score = sum(1 for word in words if word in negative_words)

    polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
    subjectivity_score = (positive_score + negative_score) / (len(words) + 0.000001)

    return positive_score, negative_score, polarity_score, subjectivity_score

# Function to compute readability and other metrics
def readability_analysis(text):
    sentences = sent_tokenize(text)
    words = clean_text(text)

    avg_sentence_length = len(words) / len(sentences)
    complex_words = [word for word in words if textstat.syllable_count(word) > 2]
    percentage_complex_words = len(complex_words) / len(words)
    fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)

    syllable_per_word = sum(textstat.syllable_count(word) for word in words) / len(words)
    personal_pronouns = len(re.findall(r'\b(I|we|my|ours|us)\b', text, re.I))
    avg_word_length = sum(len(word) for word in words) / len(words)

    return avg_sentence_length, percentage_complex_words, fog_index, syllable_per_word, personal_pronouns, avg_word_length

output_data = []

for index, row in input_df.iterrows():
    url_id = row['URL_ID']

    # Read the extracted text
    with open(f"{url_id}.txt", "r") as file:
        text = file.read()

    # Perform Sentiment Analysis
    positive_score, negative_score, polarity_score, subjectivity_score = sentiment_analysis(text)

    # Perform Readability Analysis
    avg_sentence_length, percentage_complex_words, fog_index, syllable_per_word, personal_pronouns, avg_word_length = readability_analysis(text)

    # Word count (after cleaning)
    word_count = len(clean_text(text))

    # Append the results
    output_data.append({
        'URL_ID': url_id,
        'Positive Score': positive_score,
        'Negative Score': negative_score,
        'Polarity Score': polarity_score,
        'Subjectivity Score': subjectivity_score,
        'Avg Sentence Length': avg_sentence_length,
        'Percentage Complex Words': percentage_complex_words,
        'Fog Index': fog_index,
        'Word Count': word_count,
        'Syllable Per Word': syllable_per_word,
        'Personal Pronouns': personal_pronouns,
        'Avg Word Length': avg_word_length
    })

output_df = pd.DataFrame(output_data)
output_df.to_excel('Output.xlsx', index=False)

# Download the output files
from google.colab import files
files.download('Output.xlsx')