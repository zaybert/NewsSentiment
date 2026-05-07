import requests
from bs4 import BeautifulSoup
import tkinter as tk

# Allowed sites
# https://www.bbc.com/business
# https://www.cnn.com/business
# https://www.npr.org/sections/business/

# Requesting website
URL_web = input("Enter URL: ")
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(URL_web, headers=headers)
print("The response code is : ", response)

#Parsing HTML Document
soup=BeautifulSoup(response.content,'html.parser')

#Extract headline
headlines=soup.find_all('h1')
for headline in headlines:
    print(headline.text, "\n")
    
#Test comment
    