#Import Packages
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

#entering the website
#In  order for the Selenium Package to work the chromedriver must be installed"
PATH= "Define working directory\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get('http://www.greek-language.gr/greekLang/modern_greek/tools/lexica/triantafyllides/advsearch.html')


#Finding The Greek Verbs
select = Select(driver.find_element_by_id("lemma_type"))
select.select_by_visible_text("Ρήμα") #Ρήμα is the greek word for "Verb"
search=driver.find_element_by_name("alq")
search.send_keys(Keys.RETURN)


#Scraping Lexical Items
data=[]
def scrape():
    content = driver.find_element_by_id("content")
    lemmas = content.find_element_by_id("lemmas")
    definitions= lemmas.find_elements_by_tag_name("dt")
        for definition in definitions:
            words = definition.find_element_by_tag_name("b").text
            data.append(words)

#Webpage changing and saving content
while True:
    try:
        element = WebDriverWait (driver, 10).until (EC.presence_of_element_located ((By.CLASS_NAME, 'next_page')))
        scrape()
        element.click()
    except TimeoutException:
        break
 
print(data)
#Temporary save
import pickle
with open ('words_data.txt', 'rb') as fp:
    data = pickle.load(fp)

#export in xlsx format και manual data cleansing
import pandas as pd
df = pd.DataFrame(data)
writer = pd.ExcelWriter('test.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='welcome', index=False)
writer.save()

#import data
import pandas as pd
import xlrd
refined_data = pd.read_excel(r"C:\Users\panos\PycharmProjects\untitled\refined_data.xlsx", header=None)
refined_datalist= list(refined_data[0])

#Define character function
def char(word):
    return{"χαρακτήρας": word[-2]} #χαρακτήρας is the greek word for "character"

from tqdm import tqdm
from time import sleep

#Writing word lists according to conjugation
a_conj = []
b_conj = []
for word in tqdm(refined_datalist):
    if word[-1] == "ω":
        a_conj.append(word)
    elif word[-1] == "ώ":
        b_conj.append(word)

#Concatenation of the two lists along with their conjugation tags
tagged_list = ([(words,"πρώτη συζυγία")for words in a_conj]+[(words,"δεύτερη συζυγία") for words in b_conj])

#Shuffle and character feature
import random
random.shuffle(tagged_list)
char_list = [(char(v), conj) for (v, conj) in tagged_list]
train_set, test_set = char_list[1000:], char_list[:1000]


#Naive Bayes Classifier
import nltk
from nltk import classify
from nltk import NaiveBayesClassifier
classifier = nltk.NaiveBayesClassifier.train(train_set)
classifier.show_most_informative_features(10)
classifier.classify((char(refined_datalist[18])))
print(nltk.classify.accuracy(classifier, test_set))
