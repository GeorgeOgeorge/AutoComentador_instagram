import random
from os import path
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class WebBot:
    
    #Class constructor
    def __init__(self, driverPath):
        self.driver = webdriver.Chrome(driverPath)
        self.username = None
        self.backupFile = None

    def setUsername(self, username):
        self.username = username
        self.backupFile = "./" + self.username + ".txt"

    #waiting for the login form to load -> actually doing the login -> skiping the remember button
    def login(self, username, password):
        self.setUsername(username)
        self.driver.get("https://www.instagram.com")
        self.driver.fullscreen_window()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))
        (self.driver.find_element_by_name("username")).send_keys(username)
        (self.driver.find_element_by_name("password")).send_keys(password)
        (self.driver.find_element_by_name("username")).send_keys(Keys.RETURN)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "cmbtv")))
        (self.driver.find_elements_by_tag_name("button"))[1].click()

    def getFollowers(self):
        self.openFollowers()
        finalFollowers = None
        if path.exists(self.backupFile):
            finalFollowers = self.fileBackup()
        else:
            finalFollowers = self.createBackup()
        return finalFollowers

    def comment(self, post):
        self.driver.get(post)
        self.checkRules(post)
        followers = self.getFollowers()
        for follower in followers:
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "Ypffh")))
            WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, "Ypffh")))
            (self.driver.find_element_by_class_name("Ypffh")).click()
            (self.driver.find_element_by_class_name("Ypffh")).send_keys(follower + " ")
            ((self.driver.find_element_by_class_name("X7cDz")).find_elements_by_tag_name("button"))[1].click()
            sleep(random.randint(30, 60))

    def openFollowers(self):
        self.driver.fullscreen_window()
        self.driver.get("https://www.instagram.com/" + self.username + "/")
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "-nal3")))
        (self.driver.find_elements_by_class_name("-nal3"))[1].click()
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "isgrP")))
        altura = 0
        while altura != self.driver.execute_script("return document.getElementsByClassName('isgrP')[0].scrollHeight;"):
            altura = self.driver.execute_script("return document.getElementsByClassName('isgrP')[0].scrollHeight;")
            self.driver.execute_script("document.getElementsByClassName('isgrP')[0].scrollTo(0,"+ str(altura) +");")
            sleep(1)

    def fileBackup(self):
        file = open(self.backupFile)
        finalFollowers = None
        for follower in list(file):
            finalFollowers.append(follower[0:len(follower)-1])
        return finalFollowers

    def createBackup(self):
        file = open(self.backupFile,"w")
        finalFollowers = None
        followerListAux = self.driver.find_elements_by_class_name("_0imsa")
        followersUrls = []
        for follower in followerListAux:
            followersUrls.append(follower.get_attribute("href"))
        for url in followersUrls:
            self.driver.get(url)
            self.filterFollower(file,finalFollowers,url)
        file.close()
        return finalFollowers
        
    def filterFollower(self,file,finalFollowers,url):
        try:
            WebDriverWait(self.driver, 600).until(EC.presence_of_element_located((By.CLASS_NAME, "-vDIg")))
            try:
                self.driver.find_element_by_class_name("yLUwa")
            except:
                try:
                    bio = str(((self.driver.find_element_by_class_name("-vDIg")).find_element_by_tag_name("span")).text).upper()
                    if bio.find("LOJA") == -1:
                        finalFollowers.append("@" + url[26:len(url)-1])
                        file.write("@" + url[26:len(url)-1] + "\n")
                except:
                    finalFollowers.append("@" + url[26:len(url)-1])
                    file.write("@" + url[26:len(url)-1] + "\n")
        except:
            self.driver.refresh()

    def checkRules(self,post):
        rules = ((((self.driver.find_elements_by_class_name("C4VMK"))[0]).find_elements_by_tag_name("span"))[1]).text
        (self.driver.find_elements_by_class_name("wpO6b"))[1].click()
        (self.driver.find_elements_by_class_name("wpO6b"))[4].click()
        try:
            urlList = ((self.driver.find_elements_by_class_name("C4VMK"))[0]).find_elements_by_tag_name("a")
            followList = []
            for url in urlList:
                followList.append(url.get_attribute("href"))
            for follow in followList:
                self.driver.get(follow)
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "yZn4P")))
                if (self.driver.find_elements_by_class_name("yZn4P"))[0].text == "seguir":
                    (self.driver.find_elements_by_class_name("yZn4P"))[0].click()
        except:
            pass
        self.driver.get(post)
