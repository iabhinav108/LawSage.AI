import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.services.document_processing.pdf_extractor import PDFExtractor
# nltk.download('punkt_tab')

class TextCleaner:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))

    def remove_special_characters(self, text):
        """Remove special characters and punctuation."""
        text = re.sub(r'[^\w\s]', '', text)
        return text

    def remove_numbers(self, text):
        """Remove numbers from the text."""
        return re.sub(r'\d+', '', text)

    def remove_whitespace(self, text):
        """Remove excess whitespace."""
        return " ".join(text.split())

    def lowercase_text(self, text):
        """Convert all text to lowercase."""
        return text.lower()

    def remove_stopwords(self, text):
        """Remove stopwords."""
        tokens = word_tokenize(text)
        filtered_text = [word for word in tokens if word.lower() not in self.stop_words]
        return ' '.join(filtered_text)

    def preprocess_text(self, text):
        """Clean and preprocess the text."""
        text = self.lowercase_text(text)
        text = self.remove_special_characters(text)
        text = self.remove_numbers(text)
        text = self.remove_whitespace(text)
        text = self.remove_stopwords(text)
        return text

# Example Usage:
if __name__ == "__main__":
    file_path = 'static/uploads/test1.pdf'
    extractor = PDFExtractor(file_path)
    text = extractor.extract_text()
    cleaner = TextCleaner()
    # text = "This is a sample sentence, with numbers 123 and special characters!?"
    cleaned_text = cleaner.preprocess_text(text)
    print(cleaned_text)
