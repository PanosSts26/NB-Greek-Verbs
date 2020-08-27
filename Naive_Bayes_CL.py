#Εισαγωγή πακέτων
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

#Είσοδος σε ιστοσελίδα
PATH= "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get('http://www.greek-language.gr/greekLang/modern_greek/tools/lexica/triantafyllides/advsearch.html')


#Εύρεση Ρημάτων
select = Select(driver.find_element_by_id("lemma_type"))
select.select_by_visible_text("Ρήμα")
search=driver.find_element_by_name("alq")
search.send_keys(Keys.RETURN)


#Scraping Περιεχομένου
data=[]
def scrape():
    content = driver.find_element_by_id("content")
    lemmas = content.find_element_by_id("lemmas")
    definitions= lemmas.find_elements_by_tag_name("dt")
        for definition in definitions:
            words = definition.find_element_by_tag_name("b").text
            data.append(words)

#προσπέλαση σελίδας
while True:
    try:
        element = WebDriverWait (driver, 10).until (EC.presence_of_element_located ((By.CLASS_NAME, 'next_page')))
        scrape()
        element.click()
    except TimeoutException:
        break
    finally :
        driver.close ()

print(data)
#προσωρινή αποθήκευση λίστας
import pickle
with open ('words_data.txt', 'rb') as fp:
    data = pickle.load(fp)

#export σε excel και manual έλεχγος δεδομένων
import pandas as pd
df = pd.DataFrame(data)
writer = pd.ExcelWriter('test.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='welcome', index=False)
writer.save()

#import δεδομένων
import pandas as pd
import xlrd
refined_data = pd.read_excel(r"C:\Users\panos\PycharmProjects\untitled\refined_data.xlsx", header=None)
refined_datalist= list(refined_data[0])

#συνάρτηση για εύρεσης χαρακτήρα
def char(word):
    return{"χαρακτήρας": word[-2]}

from tqdm import tqdm
from time import sleep

#Δημιουργία λίστας πρώτης και δεύτερης συζυγίας
a_conj = []
b_conj = []
for word in tqdm(refined_datalist):
    if word[-1] == "ω":
        a_conj.append(word)
    elif word[-1] == "ώ":
        b_conj.append(word)

#Ένωση της λίστας της πρώτης συζυγίας με την αντίστοιχη της δεύτερης μαζί με το tag τους
tagged_list = ([(words,"πρώτη συζυγία")for words in a_conj]+[(words,"δεύτερη συζυγία") for words in b_conj])

#Shuffle και εισαγωγή feature χαρακτήρα
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
