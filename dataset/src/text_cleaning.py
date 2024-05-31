# text_cleaning.py

import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def clean_text(text):
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)

    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)

    # Convert to lowercase
    text = text.lower()

    # Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)

    # Tokenize into words
    words = word_tokenize(text)

    # Remove stop words
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]

    # Lemmatize words
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]

    # Join words back into a single string
    cleaned_text = ' '.join(words)

    return cleaned_text

def segment_sentences(text):
    # Segment text into sentences
    sentences = sent_tokenize(text)
    return sentences

# Example usage
if __name__ == "__main__":
    sample_text = """
    This is an example sentence. It contains multiple words, punctuation, and other elements that need cleaning.
    <p>This is a paragraph with HTML tags.</p>
    """

    cleaned = clean_text(sample_text)
    sentences = segment_sentences(cleaned)

    print("Cleaned Text:")
    print(cleaned)
    print("\nSegmented Sentences:")
    for sentence in sentences:
        print(sentence)
