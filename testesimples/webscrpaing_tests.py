import requests
import bs4
import openvino 


res = requests.get("https://webflow.com/made-in-webflow/thumbnail")

#print (type(res))
#print (res.text)
soup = bs4.BeautifulSoup(res.text,"lxml")
#print (soup)
#print (soup.select('Title'))
#print (soup.select(".toctext"))
print (soup.select(".thumbimage"))
