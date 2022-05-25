from bs4 import BeautifulSoup
import re

#open_txt = open("C:/Users/mkind/OneDrive/Desktop/Bondehuset_fullpage.txt", encoding="utf8")
open_txt = open("C:/Users/mkind/OneDrive/Desktop/Json_Hotel_test_fullpage.txt", encoding="utf8")

read_txt = open_txt.read()

soup = BeautifulSoup(read_txt, "lxml")
travelers_choice = soup.select("div.fwcnV")

print(travelers_choice)
print(type(travelers_choice))




