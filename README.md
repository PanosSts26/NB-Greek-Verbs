# NB-Greek-Verbs
A *Naive Bayes classifier* about the Verbs of the Greek Language.

For this project a Naive Bayes classifier was created from the `Nltk` **Python** Package.

A word list was scraped in orded to be used as a source for the classifier.

## Scraping
The word list was taken from http://www.greek-language.gr/greekLang/index.html. 
The `Selenium` package was used. Using this package a bot was created that opened a browser, entered the Portal of Greek Language website searched all the *Greek Verbs* and saved only the lexical items in a word list. The data was saved and cleansed in an `xlsx file`.

## Classifier
Then a function was defined that returned the character of the verbs. The word list was divided in two parts according to the conjugation. The conjugation of Greek Verbs is determined by whether or not the last letter is stressed or not. The two word lists were then with a tag according to their conjugation and then randomized with the  `random` package. The data was then divided in a train and test set. Using the `nltk` package the Naives Bayes classifier was created with a 0.869 accuracy.




