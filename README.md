# NB-Greek-Verbs
A *Naive Bayes classifier* about the Verbs of the Greek Language.

For this project a Naive Bayes classifier was created from the `Nltk` **Python** Package.

A word list was scraped in orded to be used as data for the classifier.
## Dependencies
Since we are Feature Classifier
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

Using this package we can create a bot that opens a browser, enters the Portal of Greek Language website and searches all the *Greek Verbs* saving only the lexical items in a word list. 

#In  order for the Selenium Package to work chromedriver must be installed"
PATH= "Define working directory\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get('http://www.greek-language.gr/greekLang/modern_greek/tools/lexica/triantafyllides/advsearch.html')

#Finding The Greek Verbs
select = Select(driver.find_element_by_id("lemma_type"))
select.select_by_visible_text("Ρήμα") #Ρήμα is the greek word for "Verb"
search=driver.find_element_by_name("alq")
search.send_keys(Keys.RETURN)
```

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
Then we can incorporate the scrape function to a while loop 
```python
while True:
    try:
        element = WebDriverWait (driver, 10).until (EC.presence_of_element_located ((By.CLASS_NAME, 'next_page')))
        scrape()
        element.click()
    except TimeoutException:
        break
```
After the scraping was finished the word list was saved  in a `xlsx file` and then was cleansed.


## Classifier
Then a function was defined that returned the character of the verbs. 
The word list was divided in two parts according to the conjugation. The conjugation of Greek Verbs is determined by whether or not the last letter is stressed or not.
The two word lists were then with a tag according to their conjugation and then randomized with the  `random` package. The data was then divided in a train and test set. Using the `nltk` package the Naives Bayes classifier was created with a 0.869 accuracy.

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
