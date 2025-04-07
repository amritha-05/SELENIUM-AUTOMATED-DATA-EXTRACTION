# SELENIUM-AUTOMATED-DATA-EXTRACTION
A web scraping tool to extract data from a dynamic website loaded with JS and based with HTML. This data is then stored in an MS SQL database for further analysis and use. 
Technologies Used: 
• Selenium: A powerful tool for automating web browsers, used here to navigate and 
extract data from the webpage. 
• MS SQL Database: The database where the extracted data is stored for analysis. 
Process: 
1. Browser Automation: 
o Selenium is used to initialize and automate a Chrome browser. This allows 
the script to navigate to the target webpage and perform actions as a human 
user would. 
o The automation involves launching the browser, navigating to the webpage, 
and interacting with the webpage elements. 
2. Data Extraction: 
o The webpage contains data formatted in HTML and JavaScript. Using 
Selenium, the script identifies and extracts the relevant data by inspecting 
the HTML elements. 
o Each URL and data point are extracted using HTML inspection, which involves 
identifying the HTML tags and attributes that contain the desired 
information. 
3. Data Storage: 
o Once extracted, the data is formatted and stored in an MS SQL database. This 
involves connecting to the database, creating tables if necessary, and 
inserting the data into the appropriate tables. 
o The stored data can then be queried and analysed for various purposes, such 
as monitoring the performance of the antenna reader or generating reports. 
Applications and Benefits: 
• Automated Data Collection: The web scraping tool automates the process of data 
collection, making it more efficient and less prone to human error. 
• Data Analysis: The extracted data can be analysed to gain insights into the 
performance of the antenna reader, identify trends, and make informed decisions. 
• Resource Efficiency: Automating the data extraction process saves time and 
resources, allowing personnel to focus on more critical tasks.
