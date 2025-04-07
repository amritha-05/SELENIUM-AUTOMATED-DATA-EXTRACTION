import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pypyodbc as pyodbc
import os

# MS SQL Server connection details 
server = "AMY\\SQLEXPRESS"
database = "AMYDB"
username_db = os.getenv('DB_USERNAME', 'amy\\amrit')  
password_db = os.getenv('DB_PASSWORD', '1953')  

# URLs
login_url = 'http://10.134.0.87/'
data_url = "http://10.134.0.87/readtags.html"

# Path to WebDriver 
webdriver_path = r"C:\Users\amrit\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"

# Login credentials
login_username = 'admin'
login_password = 'change'

# Function to configure and return WebDriver
def get_driver(webdriver_path):
    options = Options()
    service = Service(webdriver_path)
    return webdriver.Chrome(service=service, options=options)

# Function to extract data from the webpage
def extract_data(driver, data_url):
    try:
        driver.get(data_url)
        driver.switch_to.frame("Login")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'tagsT')))

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        table = soup.find('table', {'id': 'tagsT'})

        headers = [header.text.strip() for header in table.find_all('th')]
        data = []

        for row in table.find_all('tr'):
            columns = row.find_all('td')
            if columns:
                item = {headers[i]: columns[i].text.strip() for i in range(len(columns))}
                data.append(item)
        driver.switch_to.default_content()
        return headers, data

    except Exception as e:
        print(f"An error occurred during data extraction: {e}")
        return [], []

# Function to check for duplicates and store new data in MS SQL
def store_data_in_mssql(headers, data, server, database, username_db, password_db):
    conn_str = (
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={server};'
        f'DATABASE={database};'
        f'UID={username_db};'
        f'PWD={password_db}'
    )

    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    table_name = 'your_table_name'
    create_table_query = f"""
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='{table_name}' and xtype='U')
    CREATE TABLE {table_name} (
        {headers[0]} VARCHAR(255),
        {headers[1]} VARCHAR(255),
        system_time DATETIME,
        PRIMARY KEY ({headers[0]}, {headers[1]})
    )
    """
    cursor.execute(create_table_query)

    for item in data:
        columns = ', '.join(item.keys())
        placeholders = ', '.join(['?' for _ in item.keys()])
        values = tuple(item.values()) + (datetime.now(),)

        check_query = f"""
        SELECT COUNT(*) FROM {table_name} 
        WHERE {headers[0]} = ? AND {headers[1]} = ?
        """
        cursor.execute(check_query, (item[headers[0]], item[headers[1]]))
        if cursor.fetchone()[0] == 0:
            insert_query = f"""
            INSERT INTO {table_name} ({columns}, system_time)
            VALUES ({placeholders}, ?)
            """
            cursor.execute(insert_query, values)

    conn.commit()
    cursor.close()
    conn.close()

# Main function to execute the steps
def main():
    driver = get_driver(webdriver_path)
    try:
        driver.get(login_url)
        print("Navigated to login URL")
        driver.switch_to.frame("Login")
        print("Switched to Login frame")
        
        password_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        print("Password element located")
        password_element.send_keys(login_password)
        
        login_button = driver.find_element(By.ID, 'LoginId-button')
        login_button.click()
        print("Clicked login button")
            
        driver.switch_to.default_content()
        print("Switched to default content")
        
        WebDriverWait(driver, 20).until(
            EC.frame_to_be_available_and_switch_to_it((By.NAME, "menuId"))
        )
        print("Switched to navigation frame")
        
        read_tags_element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '#ReadTags')]"))
        )
        print("Located read tags link")
        read_tags_element.click()
        print("Clicked read tags link")
        
        WebDriverWait(driver, 20).until(EC.url_to_be(data_url))
        print("Navigated to data URL")
        
        while True:
            headers, data = extract_data(driver, data_url)
            if headers and data:
                store_data_in_mssql(headers[:2], data, server, database, username_db, password_db)
                print("Data extraction and storage completed successfully!")
            else:
                print("No data to store.")
            time.sleep(60)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()

