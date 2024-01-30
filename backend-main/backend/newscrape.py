import requests
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import ast
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import time
from sqlalchemy import create_engine
from flask import *
from sqlalchemy.orm import scoped_session, sessionmaker
from psycopg2.errors import UniqueViolation
import psycopg2.extras

HOST = "localhost"
USER = "postgres"
PASSWORD = "postgres"
PORT = "5432"
DATABASE = "newscraper"

def database_connection():
    connection = psycopg2.connect(
                    user=USER, 
                    password=PASSWORD,
                    host=HOST, 
                    port=PORT, 
                    database=DATABASE)
    return connection

conn = database_connection()
cursor = conn.cursor()

xpath_list = [{'label': 'title', 'xpath': '/html/body/form/div[3]/div/div[2]/div[2]/div[4]/div/div/table/tbody/tr[2]/td/b'}, {'label': 'article', 'xpath': '/html/body/form/div[3]/div/div[2]/div[2]/div[4]/div/div/table/tbody/tr[2]/td/p'}]

options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
# options.add_argument("--headless")
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)

driver.maximize_window()  # You need to download and configure the webdriver
# element = driver.find_element(By.XPATH, xpath)
domain = 'https://www.satp.org/terrorism-update/tribal-elder-killed-in-herat-province'
scraped_data = []
driver.get(domain)
for xpath_dict in xpath_list:
    print(xpath_dict)
    # print(xpath_dict)
    label = xpath_dict['label']
    xpath = xpath_dict['xpath']
    if 'text()' in xpath.split("/"):
        xpath = xpath.replace("/text()", "")
    try:
        print(xpath)
        # time.sleep(10)
        element = driver.find_element(By.XPATH, xpath)
        if element:
                    # Print or use the text of the element
            if element.get_attribute('src'):
                data = {
                            label : element.get_attribute('src')
                        }
                scraped_data.append(data)
            else:
                # scraped_data.append(element.text)
                data = {
                            label : element.text
                        }
                scraped_data.append(data)
        
    except Exception as e:
        print(e)
        continue
try:
    cursor.execute("INSERT INTO extracted_data (url, edata,user_id) VALUES (%s, %s,%s)", (domain, json.dumps(scraped_data),'mark123@gmail.com'))
    conn.commit()
except Exception as e:
    print(e)
finally:
    cursor.close()
    conn.close()
    driver.quit()

