from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
driver.get('https://www.springfair.com/exhibitors')
import csv

time.sleep(5)

name = []
hall = []
stand = []
area = []
country = []
website = []

try:
    WebDriverWait(driver,10).until(EC.element_to_be_clickable(driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]'))).click()
except:
    pass

time.sleep(5)

driver.get('https://www.springfair.com/exhibitors')
soup = BeautifulSoup(driver.page_source, 'html.parser')
companies = soup.find_all('li', attrs={'class': 'm-exhibitors-list__items__item js-link js-librarylink-entry m-exhibitors-list__items__item--status-standard js-library-item'})

print(len(companies), 'companies found')
for i in range(len(companies)):
    company = companies[i] 
    try:
        link = company.find('a').get('href')
        link = 'https://www.springfair.com/' + link
    except:
        link = company.find('a').get_attribute('href')
        link = 'https://www.springfair.com/' + link
        
    driver.switch_to.new_window('tab')
    driver.get(link)    
    #name      
    name1 = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/main/div/div/div/div[2]/div[1]/div/h1')
    name.append(name1.text)
    print('Name: ', name1.text)
    #hall#stand    
    hall_stand = driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/main/div/div/div/div[2]/div[1]/div/div')    
    # words = hall_stand.split()
    # hall_index = words.index('Hall')
    # stand_index = words.index('Stand')
    # hall_number = words[hall_index+1]
    # stand_number = words[stand_index+1]
    # print('Hall: ', hall_number)
    # print('Stand: ', stand_number)
    print('Hall: ', hall_stand.text.split()[2])
    print('Stand: ', hall_stand.text.split()[-1])
    hall.append(hall_stand.text.split()[2])
    stand.append(hall_stand.text.split()[-1])
    
    
    #Address
    try:
        address = driver.find_element(By.CLASS_NAME, 'm-exhibitor-entry__item__body__contacts__address')
    except:
        address = 'No Address Found'
    try:
        address,city, country_var = address.text.strip().split('\n')
    except:
        address,country_var = address.text.strip().split('\n')
            
    print('City: ', city.strip())
    print('Country: ', country_var.strip())     
    area.append(city.strip())
    country.append(country_var.strip())
    #Website
    try:
        website1 = driver.find_element(By.CLASS_NAME, 'm-exhibitor-entry__item__body__contacts__additional__website')
        website.append(website1.text)
        print('Website: ', website1.text)
    except:
        website1 = 'No Website Found'
        website.append(website1)
        
    
   
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    
with open('data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    headers = ['Name', 'Hall', 'Stand', 'Area', 'Country', 'Website']
    writer.writerow(headers)
    for i in range(len(name)):
        writer.writerow([name[i], hall[i], stand[i], area[i], country[i], website[i]])

    
