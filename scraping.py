from bs4 import BeautifulSoup as bs
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException, NoSuchElementException
import time
import pandas as pd



class WebScraper:
    def __init__(self, product, websites):
        self.product = product
        self.websites = websites
        self.driver = self.setup_driver()
        self.results ={"title":[],"price":[],"Vendor":[],"Rating":[],"product_link":[]}
    
    def setup_driver(self):
        logging.basicConfig(filename="C:\\Users\\anshi\\OneDrive\\Desktop\\SIH\\scraper.log", level=logging.INFO)
        options = Options()
        options.add_argument("--headless")  # Uncomment to run in headless mode
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920x1080")
        driver = webdriver.Chrome(options=options)
        return driver

    def scrape(self):
        for i in self.websites:
            if "labx" in i.lower():
                self.scrape_labx(i)
           
            elif "indiamart" in i.lower():
                self.scrape_indiamart(i)
              
            elif "alibaba" in i.lower():
                self.scrape_alibaba(i)
       
                
            elif "flipkart" in i.lower():
                self.scrape_flipkart(i)
             
             
        self.driver.quit()
        return self.results      
    
            
    def scrape_labx(self,web):
       
            url=web+self.product
            logging.info(url)
            self.driver.get(url)
            self.driver.implicitly_wait(10)
            outer_html = self.driver.page_source
            soup=bs(outer_html,"html.parser")
            try:
                link=soup.find("div",class_="grid-right-results svelte-cdavil")
                l=link.find_all("a")
                pro_link=[]
                for i in l:
                    link1="https://www.labx.com"+ i.get("href")
                    pro_link.append(link1)
                print(len(pro_link))
                labx_links=pro_link[0:3]
              
                for i in labx_links:
                    
                    self.driver.get(i)
                    time.sleep(1)
                    outer_html_1 = self.driver.page_source
                    
                    soup=bs(outer_html_1,"html.parser")
                    t=soup.find("h1",class_="svelte-1izlh3j")
                    title=t.get_text()
               

                
                    p=soup.find("div",class_="buy-card-price svelte-1izlh3j")
                    if p:
                        price=p.get_text().strip()
                    else:
                        price="NaN"
                    
            
                    self.results["title"].append(title)
                    self.results["price"].append(price)
                    self.results["Vendor"].append("LabX")
                    self.results["product_link"].append(i)
                    self.results["Rating"].append("NaN")

            except Exception as e:
                print("An error occurred:", e)
                
            
     

 
    def  scrape_indiamart(self,web):
        
            url=web+self.product
            logging.info(url)

            self.driver.get(url)
            self.driver.implicitly_wait(10)
            outer_html = self.driver.page_source
            try:
                link=self.driver.find_elements(By.CLASS_NAME,"cardlinks")
                pro_link=[]
                for j in link:
                    pro_link.append(j.get_attribute("href"))
                
                indiamart_links_1=pro_link[0:1]
                for i in indiamart_links_1:
                
                    self.driver.get(i)
                    time.sleep(1)
                    outer_html_1 = self.driver.page_source
                
                    soup=bs(outer_html_1,"html.parser")
                
                    t=soup.find("h1",class_="bo center-heading centerHeadHeight")
                    title=(t.get_text())

                    p=soup.find("span",class_="bo price-unit")
                    if p:
                        p1 = p.get_text().replace('\u20b9', '')
                        price=f"Rs {p1}"
                    else:
                        price="NaN"
                    
                    r=soup.find("span",class_="bo color")
                

                 
                    self.results["title"].append(title)
                    self.results["price"].append(price)
                    self.results["Vendor"].append("IndiaMart")
                    self.results["product_link"].append(i)
                    self.results["Rating"].append(r.get_text())
            
            except Exception as e:
                print("An error occurred:", e)
                
      
   
    def scrape_alibaba(self,web):
        
            url=web+self.product
            
            logging.info(url)
        
            self.driver.get(url)
            self.driver.implicitly_wait(10)
            outer_html = self.driver.page_source
            soup=bs(outer_html,"html.parser")
            try:
                link=soup.find_all("div",class_="card-info list-card-layout__info")
                pro_link=[]
                for i in link:
                    
                    l=i.find("a")
                    link1="https:"+l['href']
                    pro_link.append(link1)
                    
                alibaba_links_1=pro_link[0:3]
                for i in alibaba_links_1:
                    
                    self.driver.get(i)
                    time.sleep(1)
                    outer_html_1 = self.driver.page_source
                    self.driver.implicitly_wait(10)
                    
                    soup=bs(outer_html_1,"html.parser")

                    t=soup.find("div",class_="product-title-container")
                    title=t.find("h1").get_text()
                
                    p=self.driver.find_element(By.CLASS_NAME,"price")
                    price=p.text
                    
                    r=soup.find("div",class_="score")
                    if r :  
                        ra=r.text
                    else:
                        ra="NaN"
                   
                    self.results["title"].append(title)
                    self.results["price"].append(price)
                    self.results["Vendor"].append("Alibaba")
                    self.results["product_link"].append(i)
                    self.results["Rating"].append(ra)
                    
            except Exception as e:
                print("An error occurred:", e)
               
        


    def scrape_flipkart(self,web):
        
            url=web+self.product
            
            logging.info(url)
            self.driver.get(url)
            self.driver.implicitly_wait(10)
            outer_html = self.driver.page_source
            soup=bs(outer_html,"html.parser")
            
            urls = soup.find_all("a", {"class": "VJA3rP"})
            del urls[0:2] 

            pro_links = ["https://www.flipkart.com" + j["href"] for j in urls]
            
            pro_links_to_scrape = pro_links[0:3]  
            try:

                for product_link in pro_links_to_scrape:
                    self.driver.get(product_link)
                    outer_html_1 = self.driver.page_source

                    # Scrape title
                    title_element = self.driver.find_element(By.CLASS_NAME, "VU-ZEz")
                    title=title_element.text
                    # Scrape price
                    try:
                        price_element = self.driver.find_element(By.CLASS_NAME, "hl05eU")
                        price = price_element.text.split('₹')[1].split('₹')[0]
                        
                    except NoSuchElementException:
                        logging.error("Price element not found")
                        price="NaN"

                    try:
                        rating_element = self.driver.find_element(By.CLASS_NAME, "XQDdHH")
                        r=rating_element.text
                    except NoSuchElementException:
                        logging.error("Rating element not found")
                        r="NaN"
                    self.results["title"].append(title)
                    self.results["price"].append(price)
                    self.results["Vendor"].append("Flipkart")
                    self.results["product_link"].append(product_link)
                    self.results["Rating"].append(r)
            except WebDriverException as e:
                logging.error(f"WebDriver error: {e}")
               
      

if  __name__ == "__main__":
    
    websites=["https://www.labx.com/search/?sw=","https://dir.indiamart.com/search.mp?ss=","https://www.alibaba.com/trade/search?SearchText=","https://www.flipkart.com/search?q="]
    product_name = "arduino" 
    product = product_name.replace(" ", "")
    scraper = WebScraper(product,websites)
    results = scraper.scrape()
    logging.info(results)
    df=pd.DataFrame(results)
    df.to_csv("results.csv")

    


