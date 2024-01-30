from flask import Flask, render_template, request, redirect, url_for, jsonify
import psycopg2
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
app = Flask(__name__)

# Database connection parameters
db_params = {
    'dbname': 'fapp',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': '5432'
}

# Create a connection to the PostgreSQL database
conn = psycopg2.connect(**db_params)
cursor = conn.cursor()

# Create a table to store the submitted data
create_table_query = """
CREATE TABLE IF NOT EXISTS user_data (
    id SERIAL PRIMARY KEY,
    input1 VARCHAR,
    input2 VARCHAR,
    input3 VARCHAR,
    input4 VARCHAR,
    input5 VARCHAR
)
"""
cursor.execute(create_table_query)
conn.commit()

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/submit', methods=['POST'])
def submit():
    data = request.form
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user_data (input1, input2, input3, input4, input5) VALUES (%s, %s, %s, %s, %s)",
                   (data['name'], data['email'], data['phone'], data['address'], data['city']))
    conn.commit()
    cursor.close()
    return redirect(url_for('display'))

@app.route('/display')
def display():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_data")
    data = cursor.fetchall()
    cursor.close()
    return render_template('display.html', data=data)

@app.route('/process', methods=['POST'])
def process():
    selected_ids = request.form.getlist('selected')
    selected_data = []
    cursor = conn.cursor()
    for id in selected_ids:
        cursor.execute("SELECT * FROM user_data WHERE id = %s", (id,))
        row = cursor.fetchone()
        selected_data.append(row)
        # print(selected_data)
    cursor.close()
    
    # Web scraping using Selenium and processing selected data
    scraped_data = []
    chrome_options = Options()
    # chrome_options.headless = True
    #options.headless = True
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument('--ignore-certificate-errors')
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()  # You need to download and configure the webdriver
    for row in selected_data:
        print(row)
        # Assuming 'address' is the XPath of the element you want to scrape
        driver.get(row[1])  # Assuming 'address' is in the 5th column
        element2 = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div[2]/div[1]/div/div/div[1]/div[1]/div[2]/div[1]/div/div/div[1]/div[1]/img')
        scraped_data.append(element2.get_attribute('src'))
        print(scraped_data)
        element3 = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div[2]/div[1]/div/div/div[1]/div[1]/div[2]/div[1]/div/header/h1')
        scraped_data.append(element3.text)
        print(scraped_data)
        element4 = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div[2]/div[1]/div/div/div[1]/div[1]/div[2]/div[1]/div/header/h1/div/a[1]')
        scraped_data.append(element4.text)
        print(scraped_data)
        element5 = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div[2]/div[1]/div/div/div[1]/div[1]/div[2]/div[1]/div/div/div[1]/div[3]')
        scraped_data.append(element5.text)
        print(scraped_data)
    driver.quit()
    # Process selected items (you can define your processing logic here)
    return jsonify({"message": scraped_data})


if __name__ == '__main__':
    app.run(debug=True,port=5000)
