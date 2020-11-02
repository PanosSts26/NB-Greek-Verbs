# Naive Bayes Classifer about the Greek Verbs
This project a *Naive Bayes classifier* about the Verbs of the Greek Language. A word list was scraped in orded to be used as data for the classifier. The words consist of the entirety of the Verbs of the Greek Language taken from the Portal of the Greek Language Website which incorporates an online dictionary. The data then was divided into two lists according to the **conjugation** of the verbs. The **conjugation** of Greek Verbs is determined by whether or not the last letter is stressed or not. The second feature used for the classifier was the **character** of those verbs. 
The Naive Bayes classifier was created from the `Nltk` **Python** Package.


## Dependencies
Since we are making a Feature Classifier for verbs we should use the *Natural Language Toolkit* package since it incorporates a Naive Bayes classifier as well as tools to assess the classifier and its results.
```
pip install nltk
```
For this project the word list was taken from http://www.greek-language.gr/greekLang/index.html. 
The `Selenium` package was used. 
```
pip install selenium
```
After the scraping finishes we will have to save and cleanse our data. We will use the `pandas` and `xlrd` packages
```
pip install pandas
pip install xlrd
```
## Scraping

Using `Selenium` package we can create a bot that opens a browser, enters the Portal of Greek Language website and searches all the *Greek Verbs* saving only the lexical items in a word list. `Selenium` offers choices for accessing search bars, finding and saving the right elements of a webpage and clicking on certain buttons which is are all features needed for our project.

In order for the bot to detect and scrape only the lemmas from the Greek dictionary the following function was created
```python
data=[]
def scrape():
    content = driver.find_element_by_id("content")
    lemmas = content.find_element_by_id("lemmas")
    definitions= lemmas.find_elements_by_tag_name("dt")
   
        for definition in definitions:
            words = definition.find_element_by_tag_name("b").text
            data.append(words)
```
Then we can incorporate the *scrape* function to a while loop. This way the bot after scraping will press the *next page* button and scrape the word results from the Greek Lanugage Dictionary etc. 
After the scraping was finished the word list was saved  in a `xlsx file` and then was cleansed.


## Classifier
Then a function was defined that returned the character of the verbs. 
The word list was divided in two parts according to the conjugation.
The two word lists were then incorporated with a tag according to their conjugation and then randomized with the `random` package.
In order to isolate the **character** of every verb in our datalist the following function was created
```python
def char(word):
    return{"χαρακτήρας": word[-2]} #χαρακτήρας is the greek word for "character"
```
The data was then divided in a train and test set. Using the `nltk` package the Naives Bayes classifier was created with a 0.869 accuracy.

The results were the following
```
Most Informative Features
              χαρακτήρας = 'ζ'            πρώτη  : δεύτερ =     48.9 : 1.0
              χαρακτήρας = 'μ'            δεύτερ : πρώτη  =     42.5 : 1.0
              χαρακτήρας = 'λ'            δεύτερ : πρώτη  =      7.8 : 1.0
              χαρακτήρας = 'γ'            δεύτερ : πρώτη  =      7.1 : 1.0
              χαρακτήρας = 'τ'            δεύτερ : πρώτη  =      6.4 : 1.0
              χαρακτήρας = 'θ'            δεύτερ : πρώτη  =      4.9 : 1.0
              χαρακτήρας = 'π'            δεύτερ : πρώτη  =      4.9 : 1.0
              χαρακτήρας = 'φ'            δεύτερ : πρώτη  =      4.1 : 1.0
              χαρακτήρας = 'κ'            δεύτερ : πρώτη  =      3.3 : 1.0
              χαρακτήρας = 'δ'            δεύτερ : πρώτη  =      3.0 : 1.0
```
