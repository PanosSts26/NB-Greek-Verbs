# NB-Greek-Verbs
A *Naive Bayes classifier* about the Verbs of the Greek Language.

For this project a Naive Bayes classifier was created from the `Nltk` **Python** Package.

A word list was scraped in orded to be used as data for the classifier.

## Scraping
For this project The word list was taken from http://www.greek-language.gr/greekLang/index.html. 
The `Selenium` package was used. 
```
pip install selenium
```
Using this package a bot was created that opened a browser, entered the Portal of Greek Language website searched all the *Greek Verbs* and saved only the lexical items in a word list. 
```python
import selenium
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


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

In order for the bot to detect and scrape only the lemmas from the Greek dictionary the following function was created,
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
Then 
```python
while True:
    try:
        element = WebDriverWait (driver, 10).until (EC.presence_of_element_located ((By.CLASS_NAME, 'next_page')))
        scrape()
        element.click()
    except TimeoutException:
        break
```
The data was saved and cleansed in an `xlsx file`.
```python
#export in xlsx format και manual data cleansing
import pandas as pd
df = pd.DataFrame(data)
writer = pd.ExcelWriter('test.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='welcome', index=False)
writer.save()
```


## Classifier
Then a function was defined that returned the character of the verbs. 
```python
def char(word):
    return{"χαρακτήρας": word[-2]} #χαρακτήρας is the greek word for "character"
```

The word list was divided in two parts according to the conjugation. The conjugation of Greek Verbs is determined by whether or not the last letter is stressed or not.
```python
from tqdm import tqdm
from time import sleep
a_conj = []
b_conj = []
for word in tqdm(refined_datalist):
    if word[-1] == "ω":
        a_conj.append(word)
    elif word[-1] == "ώ":
        b_conj.append(word)
```
The two word lists were then with a tag according to their conjugation and then randomized with the  `random` package. The data was then divided in a train and test set. Using the `nltk` package the Naives Bayes classifier was created with a 0.869 accuracy.


```
pip install nltk
```
```python
import nltk
from nltk import classify
from nltk import NaiveBayesClassifier
classifier = nltk.NaiveBayesClassifier.train(train_set)
classifier.show_most_informative_features(10)
classifier.classify((char(refined_datalist[18])))
print(nltk.classify.accuracy(classifier, test_set))
```



