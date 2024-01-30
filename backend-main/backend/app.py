from flask import Flask, request, jsonify
from flask_cors import CORS
from environment import *
from werkzeug.security import generate_password_hash, check_password_hash
import sys,os
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
import schedule,time

app = Flask(__name__,template_folder='templates')
CORS(app)

# Define an API endpoint for creating an account
@app.route('/api/createAccount', methods=['POST'])
def create_account():
    try:
        # Get the JSON data from the request
        data = request.json
        print(data)
        # Extract email and password from the data
        email = data.get('email')
        password = data.get('password')
        _hashed_password = generate_password_hash(password)

        # Check if account exists using MySQL
        try:
            conn = database_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
            account = cursor.fetchone()
            # print(account[1])
            if account:
                print("Innnnnnnnnnnn")
                response_data = {'message': 'Account already exists'}
                return jsonify(response_data)
            else:
                print("Else")
                cursor.execute("INSERT INTO users (email, password) VALUES (%s,%s)",
                                    (email, _hashed_password))
                conn.commit()
                response_data = {'message': 'Account created successfully'}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            response_data = {'message': 'Account creation failed'}
            return jsonify(response_data), 500
        finally:
            cursor.close()
            conn.close()

        # Return a JSON response
        return jsonify(response_data), 200
        # Perform account creation logic here (e.g., save to a database)
        # Replace this with your actual account creation logic
        # For this example, we'll just return a success message
        
    except Exception as e:
        print(e)
        # Handle any exceptions or errors that occur during account creation
        response_data = {'message': 'Account creation failed'}
        return jsonify(response_data), 500

@app.route('/api/login', methods=['POST'])
def login():
    # Get the JSON data from the request
    data = request.get_json()

    # Establish a database connection
    conn = database_connection()
    cursor = conn.cursor()

    try:
        # Execute a query to check if the user exists in the database
        cursor.execute("SELECT * FROM users WHERE email = %s", (data.get('email'),))
        user = cursor.fetchone()
        
        if user and check_password_hash(user[2], data.get('password')):
            # Authentication successful
            response = {'message': 'Login successful'}
            return jsonify(response), 200
        else:
            # Authentication failed
            response = {'message': 'Invalid email or password'}
            return jsonify(response), 401
    except Exception as e:
        # Handle other possible errors
        print(e)
        response = {'message': 'An error occurred during login'}
        return jsonify(response), 500
    finally:
        cursor.close()
        conn.close()



def insert_data(link, xpaths):
    try:
        conn = database_connection()
        cursor = conn.cursor()

        # Assuming you have a table named 'link_xpaths' with columns 'link' and 'xpath'
        # for xpath in xpaths:
        cursor.execute("INSERT INTO link_xpaths (links, xpaths) VALUES (%s, %s)", (link, xpaths))

        conn.commit()
        cursor.close()
        conn.close()

        return True, "Data inserted successfully"
    except Exception as e:
        return False, str(e)

@app.route('/api/addxpaths', methods=['POST'])
def addxpaths():
    data = request.get_json()
    link = data['link']
    xpaths = str(data['xpaths'])

    success, message = insert_data(link, xpaths)

    if success:
        response = {'message': message}
        return jsonify(response), 200
    else:
        response = {'error': message}
        return jsonify(response), 500
    
@app.route('/api/addcrons', methods=['POST'])
def addcrons():
    data = request.get_json()
    print(data)
    domain = data['link']
    xpaths = data['xpaths']
    crontime = data['crontime']
    script_completed
    
    code_to_save = f'''
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
    DATABASE = "webscrapper"

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

    xpath_list = {xpaths}

    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    driver.maximize_window()  # You need to download and configure the webdriver

    domain = {domain}
    response = requests.get(domain)
    finallink = set()
    scraped_data = []
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        links = set(soup.find_all('a'))
        for linkes in links:
            href = linkes.get('href')
            domain = urlparse({domain}).scheme + "://" + urlparse({domain}).hostname
            if href != None:
                if not href.startswith('http'):
                    # Create an absolute URL by joining with the domain
                    absolute_url = urljoin({domain}, href)
                    finallink.add(absolute_url) 
                    # print(absolute_url,"===")
                else:
                    finallink.add(href)
                    pass
    for nested_link in finallink:
        driver.get(nested_link)
        for xpath_dict in xpath_list:
            print(xpath_dict)
            label = xpath_dict['label']
            xpath = xpath_dict['xpath']
            if 'text()' in xpath.split("/"):
                xpath = xpath.replace("/text()", "")
            try:
                print(xpath)
                element = driver.find_element(By.XPATH, xpath)  
                if element:
                    if element.get_attribute('src'):
                        data = {{label: element.get_attribute('src')}}
                        scraped_data.append(data)
                    else:
                        data = {{label: element.text}}
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
    '''
    conn = database_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO cronscripts (cron,time,domain) VALUES (%s,%s,%s)", (code_to_save,crontime,domain))
        conn.commit()
    except Exception as e:
        print(e,"===")
    finally:
        cursor.close()
        conn.close()
    schedule.every().day.at(crontime).do(exec(code_to_save))
    return jsonify("Cron saved successfully!"), 200

@app.route('/api/savedcrons',methods=['GET'])
def savedcrons():
    try:
        # Connect to the database
        conn = database_connection()
        cursor = conn.cursor()

        # Execute your SQL query to select data from the table
        cursor.execute("SELECT * FROM cronscripts")

        # Fetch all the records
        records = cursor.fetchall()

        # Create a list of dictionaries for each row
        data = []
        for row in records:
            data.append({
                'id' : row[0],
                'domain': row[4],
                'time':row[2]
                # 'column2': row[1],
                # Add more columns as needed
            })

        # Close the database connection
        cursor.close()
        conn.close()

        return jsonify(data)

    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/api/savedlinks',methods=['GET'])
def savedlinks():
    try:
        # Connect to the database
        conn = database_connection()
        cursor = conn.cursor()

        # Execute your SQL query to select data from the table
        cursor.execute("SELECT * FROM link_xpaths")

        # Fetch all the records
        records = cursor.fetchall()

        # Create a list of dictionaries for each row
        data = []
        for row in records:
            data.append({
                'id' : row[0],
                'links': row[1],
                # 'column2': row[1],
                # Add more columns as needed
            })

        # Close the database connection
        cursor.close()
        conn.close()

        return jsonify(data)

    except Exception as e:
        return jsonify({'error': str(e)})
    
@app.route('/api/process_selected_links',methods=['POST'])
def process_selected_links():
    conn = database_connection()
    cursor = conn.cursor()
    # Execute your SQL query to select data from the table
    # cursor.execute("SELECT xpaths FROM link_xpaths where id=%s")
    request_data = request.get_json()
    # print(data)
    link = request_data['selectedLinks']
    # print(request_data['email_id'])
    fetcheddata = []
    for li in link:
        # print(li['id'])
        cursor.execute("SELECT links,xpaths FROM link_xpaths where id = %s",(str(li['id']),))
        fetcheddata.append(cursor.fetchall())
    # print(fetcheddata)
    # Use list comprehension to flatten the list
    flattened_list = [item for sublist in fetcheddata for item in sublist]
    # Web scraping using Selenium and processing selected data
    chrome_options = Options()
    # chrome_options.headless = True
    #options.headless = True
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--headless")
    headers = {'User-Agent': 'Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'}
    chrome_options.add_argument(f"user-agent={headers['User-Agent']}")
    chrome_options.add_argument(f"Accept-Language={headers['Accept-Language']}")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument('--ignore-certificate-errors')
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()  # You need to download and configure the webdriver
    # Iterate through the list of tuples
    for link, xpath_dict_list in flattened_list:
        scraped_data = []
        driver.get(link)
        current_url = driver.current_url

        # Send a GET request using requests and retrieve the response code
        response = requests.get(current_url)
        response_code = response.status_code
        if response_code == 200:

            json_string = xpath_dict_list.replace("'", '"')

            # Use ast.literal_eval to safely convert the modified string to a Python list
            xpath_list = ast.literal_eval(json_string)
            # Iterate through the list of dictionaries containing XPaths
            for xpath_dict in xpath_list:
                # print(xpath_dict)
                label = xpath_dict.get('label', '')
                xpath = xpath_dict.get('xpath', '')
                if 'text()' in xpath.split("/"):
                    xpath = xpath.replace("/text()", "")
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
                    # print(data)
                    # print(f"Link: {link}, Label: {label}, Content: {element.text}")
                else:
                    print(f"Link: {link}, Label: {label}, Element not found using the provided XPath.")
            try:
                cursor.execute("INSERT INTO extracted_data (url, edata,user_id) VALUES (%s, %s,%s)", (link, json.dumps(scraped_data),request_data['email_id']))
                conn.commit()
                cursor.close()
                conn.close()
                return "Data inserted successfully"
            except Exception as e:
                print(e)
                # return jsonify(e)
        else:
            print(f"Failed to retrieve the web page: {link}")
    return jsonify(link)

@app.route('/api/delete_selected_links',methods=['POST'])
def delete_selected_links():
    conn = database_connection()
    cursor = conn.cursor()
    data = request.get_json()
    print(data)
    link = data['selectedLinks']
    fetcheddata = []
    for li in link:
        # print(li['id'])
        cursor.execute("delete FROM link_xpaths where id = %s",(str(li['id']),))
        conn.commit()    
    return jsonify("Hi")

@app.route('/api/delete_selected_crons',methods=['POST'])
def delete_selected_crons():
    conn = database_connection()
    cursor = conn.cursor()
    data = request.get_json()
    print(data)
    link = data['selectedCrons']
    fetcheddata = []
    for li in link:
        # print(li['id'])
        cursor.execute("delete FROM cronscripts where id = %s",(str(li['id']),))
        conn.commit()    
    return jsonify("Hi")

if __name__ == '__main__':
    app.run(debug=True)
