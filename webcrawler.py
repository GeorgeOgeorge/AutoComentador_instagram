#importando webdriver 
from selenium import webdriver

#criando um objeto mavegador baseado no driver baixado
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get("https://www.youtube.com/watch?v=Xjv1sY630Uc")
print(driver.title)
driver.close()