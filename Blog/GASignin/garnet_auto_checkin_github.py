from urllib2 import urlopen
import selenium
from selenium import webdriver
import time

#Configure the script
config_ip = "50.200.196.50" #Your General Assembly Campus's IP Address
config_username = #Your Github Username
config_password = #Your Github Password
config_link_text = "DC DSI 4" #Your course title in Garnet

def right_ip(ga_ip):
    if urlopen('https://ip.42.pl/raw').read() == ga_ip:
        return True
    else:
        print "Incorrect IP Address"
        return False

def click_link(url, ga_username, ga_password, link_text):
    #Pull Up Firefox
    driver = webdriver.Firefox()
    driver.get(url)

    #Github Sign In - They made this hard to automate...
    driver.find_element_by_link_text("Sign in with Github").click()
    time.sleep(3)
    username = driver.find_element_by_name("login")
    password = driver.find_element_by_name("password")
    username.send_keys(ga_username)
    password.send_keys(ga_password)
    driver.find_element_by_name("commit").click()

    #Click DSI 4 Link
    time.sleep(5)
    driver.find_element_by_link_text(link_text).click()

    #Click on check in
    time.sleep(5)
    driver.find_element_by_xpath("/html/body/main/form[1]").submit()
    print "Signed in to Garnet!"

if right_ip(config_ip) is True:
    click_link("https://garnet.wdidc.org/", config_username, config_password, config_link_text)
