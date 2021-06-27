from usr_data import USR, PASS
import random
from os import path
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

PATH = "C:\Program Files (x86)\chromedriver.exe"
POST = "https://www.instagram.com/p/CP1p3-EhLvD/?utm_medium=copy_link"
ARQ_SEG = "./seg_usuarios/" + USR + ".txt"



driver = webdriver.Chrome(PATH)
driver.get("https://www.instagram.com")
driver.fullscreen_window()


#LOGIN
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "username")))
(driver.find_element_by_name("username")).send_keys(USR)
(driver.find_element_by_name("password")).send_keys(PASS)
(driver.find_element_by_name("username")).send_keys(Keys.RETURN)
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "cmbtv")))
(driver.find_elements_by_tag_name("button"))[1].click()


#PEGANDO LISTA DE SEGUIDORES
driver.fullscreen_window()
driver.get((driver.find_element_by_class_name("gmFkV").get_attribute("href")))
WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CLASS_NAME, "-nal3")))
(driver.find_elements_by_class_name("-nal3"))[1].click()
WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CLASS_NAME, "isgrP")))
altura = 0
while altura != driver.execute_script("return document.getElementsByClassName('isgrP')[0].scrollHeight;"):
    altura = driver.execute_script("return document.getElementsByClassName('isgrP')[0].scrollHeight;")
    driver.execute_script("document.getElementsByClassName('isgrP')[0].scrollTo(0,"+ str(altura) +");")
    sleep(1)


#FILTRANDO CARREGANDO PARA ARQUIVO BUFFER E SALVANDO SEGUIDORES
seguidores_ofical = []
if path.exists(ARQ_SEG) == True :
    arq = open(ARQ_SEG)
    for p in list(arq):
        seguidores_ofical.append(p[0:len(p)-1])
else:
    arq = open(ARQ_SEG,"w")
    lista_seguidores = driver.find_elements_by_class_name("_0imsa")
    seguidores_urls = []
    for seguidor in lista_seguidores:
        seguidores_urls.append(seguidor.get_attribute("href"))
    for url in seguidores_urls:
        driver.get(url)
        try:
            WebDriverWait(driver, 600).until(EC.presence_of_element_located((By.CLASS_NAME, "-vDIg")))
            try:
                driver.find_element_by_class_name("yLUwa")
            except:
                try:
                    bio = str(((driver.find_element_by_class_name("-vDIg")).find_element_by_tag_name("span")).text).upper()
                    if bio.find("LOJA") == -1:
                        seguidores_ofical.append("@" + url[26:len(url)-1])
                        arq.write("@" + url[26:len(url)-1] + "\n")
                except:
                    seguidores_ofical.append("@" + url[26:len(url)-1])
                    arq.write("@" + url[26:len(url)-1] + "\n")
        except:
            driver.refresh()
arq.close()


#ANALISANDO REGRAS
driver.get(POST)
driver.fullscreen_window()
regras = ((((driver.find_elements_by_class_name("C4VMK"))[0]).find_elements_by_tag_name("span"))[1]).text
(driver.find_elements_by_class_name("wpO6b"))[1].click()
(driver.find_elements_by_class_name("wpO6b"))[4].click()
try:
    lista_seguir = ((driver.find_elements_by_class_name("C4VMK"))[0]).find_elements_by_tag_name("a")
    url_seguir = []
    for seguir in lista_seguir:
        url_seguir.append(seguir.get_attribute("href"))
    for seg in url_seguir:
        driver.get(seg)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "yZn4P")))
        if (driver.find_elements_by_class_name("yZn4P"))[0].text == "seguir":
            (driver.find_elements_by_class_name("yZn4P"))[0].click()
except:
    print("nao precisa seguir")


#COMENTANDO
driver.get(POST)
for follower in seguidores_ofical:
    WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CLASS_NAME, "Ypffh")))
    WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.CLASS_NAME, "Ypffh")))
    (driver.find_element_by_class_name("Ypffh")).click()
    (driver.find_element_by_class_name("Ypffh")).send_keys(follower + " ")
    ((driver.find_element_by_class_name("X7cDz")).find_elements_by_tag_name("button"))[1].click()
    sleep(random.randint(30, 60))

driver.close()
exit()


#fechar o driver
#pegar usuario, senha e post pelo arquivo
#diferentes tipos de regras
#modularizar

#from selenium.webdriver.common.action_chains import ActionChains
#action = ActionChains(driver)
#action.move_to_element(seguir)