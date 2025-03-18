#!/bin/bash
mkdir -p ~/.nltk_data
python -c "import nltk; nltk.download('punkt', download_dir='/root/.nltk_data'); nltk.download('stopwords', download_dir='/root/.nltk_data'); nltk.download('wordnet', download_dir='/root/.nltk_data'); nltk.download('omw-1.4', download_dir='/root/.nltk_data')"
export NLTK_DATA="/root/.nltk_data"
