# Sentiment Analysis
This project concentrates on a topic in Natural Language Processing: "Sentiment Analysis", where we aim to find the underlying sentiment of a given text. For this project, the data from car reviews will be used to train and test the models. Two models: Naive Bayes and Support Vector Machine are used to predict the sentiment. Towards the end of the project, a brief comparison of both the models and the final verdict on the winning models is provided.

## Phases of the project:
- Exploratory Data Analysis
- Text Pre-processing
- Demonstration of text pre-processing code
- Creating Bag of Words using CountVectorizer and TF-IDF Vectorizer
- Train and test Naive Bayes model with BoW generated using CountVectorizer
- Train and test SVM model with BoW generated using TF-IDF Vectorizer
- Comparision of model performance using Confusion Matrix with relevant vizualizations

### Text Pre-processing:
The python function `text_preprocess()` is used to pre-process the data by removing:
- punctuations
- non-letters
- converting strings to lower case
- removing stopwords
- stemming of words


Programming Language: Python3

Packages Used: NumPy, Pandas, Scikit-Learn and NLTK
