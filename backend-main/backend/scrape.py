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

xpath_list = [{'label': 'title', 'xpath': '/html/body/form/div[3]/div/div[2]/div[2]/div[4]/div/div/table/tbody/tr[2]/td/b'}, {'label': 'article', 'xpath': '/html/body/form/div[3]/div/div[2]/div[2]/div[4]/div/div/table/tbody/tr[2]/td/p'}]

chrome_options = Options()
# chrome_options.headless = True
# options.headless = True
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--headless")
headers = {'User-Agent': 'Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'}
chrome_options.add_argument(f"user-agent={headers['User-Agent']}")
chrome_options.add_argument(f"Accept-Language={headers['Accept-Language']}")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument('--ignore-certificate-errors')
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()  # You need to download and configure the webdriver
# element = driver.find_element(By.XPATH, xpath)
domain = 'https://www.satp.org/'
response = requests.get(domain)
finallink = set()
# Check if the request was successful (status code 200)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    links = set(soup.find_all('a'))
    for linkes in links:
        href = linkes.get('href')
        domain = urlparse(domain).scheme + "://" + urlparse(domain).hostname
        if href != None:
            if not href.startswith('http'):
                # Create an absolute URL by joining with the domain
                absolute_url = urljoin(domain, href)
                finallink.add(absolute_url) 
                # print(absolute_url,"===")
            else:
                finallink.add(href)
                pass
finallink = ['https://www.satp.org/terrorism-update/tribal-elder-killed-in-herat-province']
for link in finallink:
    scraped_data = []
    driver.get(link)
    current_url = driver.current_url
    # Send a GET request using requests and retrieve the response code
    response = requests.get(current_url)
    response_code = response.status_code
    if response_code == 200:
        for xpath_dict in xpath_list:
            print(xpath_dict)
            # print(xpath_dict)
            label = xpath_dict['label']
            xpath = xpath_dict['xpath']
            if 'text()' in xpath.split("/"):
                xpath = xpath.replace("/text()", "")
            try:
                print(xpath)
                time.sleep(10)
                element = driver.find_element(By.XPATH, xpath)
                print(element)
            except Exception as e:
                print(e)
                continue
            
            if element:
                print("innnn")
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
                # print(data)
                # print(f"Link: {link}, Label: {label}, Content: {element.text}")
                print(scraped_data,"====",link)
            else:
                print(f"Link: {link}, Label: {label}, Element not found using the provided XPath.")
    # try:
    #     cursor.execute("INSERT INTO extracted_data (url, edata,user_id) VALUES (%s, %s,%s)", (link, json.dumps(scraped_data),request_data['email_id']))
    #     conn.commit()
    #     cursor.close()
    #     conn.close()
    #     return "Data inserted successfully"
    # except Exception as e:
    #     print(e)
            # return jsonify(e)