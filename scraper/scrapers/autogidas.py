from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

def portal_1():
   driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
   cars=[] #List to store models
   prices=[] #List to store prices
   descriptions=[] #List to store parameters
   car_links=[] #List to store links
   for page in range(1, 5):
      driver.get("https://autogidas.lt/skelbimai/automobiliai/?f_50=kaina_asc&page={page}")
      content = driver.page_source
      soup = BeautifulSoup(content)
      for a in soup.findAll('a',href=True, attrs={'class':'item-link'}):
         car=a.find('h2', attrs={'class':'item-title'})
         price=a.find('div', attrs={'class':'item-price'})
         description=a.find('div', attrs={'class':'item-description'})
         #car_link=a.find('a'['href'], attrs={'class':'item-link'})
   
         cars.append(car.text.strip("\n$"))
         prices.append(price.text.strip("\n$"))
         descriptions.append(description.text.strip("\n$"))
         #car_links.append(description.text.strip("\n$"))

      df = pd.DataFrame({'Car Model':cars,'Price':prices,'Parameters':descriptions})
      df.to_csv('Autogidas.csv', index=True)