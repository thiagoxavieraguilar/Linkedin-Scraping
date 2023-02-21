import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
from bs4 import BeautifulSoup
import pandas as pd

# Set up the ChromeOptions object
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

# Create a new instance of the Chrome driver
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 10)
#company to scrapy all posts
driver.get('https://www.linkedin.com/company/posts/')
time.sleep(10)

#your email and a password
email = "your_email"
password= "your_password"

#email and passwod field
driver.find_element(By.ID, "username").send_keys(email)
driver.find_element(By.ID, "password").send_keys(password)
time.sleep(5)
#submit button
driver.find_element(By.XPATH, "/html/body/div/main/div[2]/div[1]/form/div[3]/button").click()

time.sleep(7)
#get height of the page
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    #scroll to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    #wait for the page to load new content
    time.sleep(7)
    
    #get the new height of the page
    new_height = driver.execute_script("return document.body.scrollHeight")
    
    #if the new height is equal to the last height, break the loop
    if new_height == last_height:
        break
    
    #update the last height with the new height
    last_height = new_height
    
time.sleep(5)
#get button to show comments
comments_button = driver.find_elements(By.CSS_SELECTOR, "ul > li.social-details-social-counts__item.social-details-social-counts__comments.social-details-social-counts__item--with-social-proof > button")
for comment in comments_button:
    try:
        comment.click()
        time.sleep(3)
        #button to load all more comments
        try:
            button_more_comment = driver.find_element(By.CLASS_NAME, 'comments-comments-list__show-previous-container').click()
            if button_more_comment:
                button_more_comment.click
        except:
            print('no more load comment')
    except:
        print('no button comment')
    

        
#get html source code
html_source = driver.page_source
#convert html in soup object 
soup = BeautifulSoup(html_source, "html.parser")
all_divs = soup.find_all("div", {"class": "ember-view occludable-update"})



mylist = []
#get all info about each post
for div in all_divs:
    myimgs = []
    #get title 
    try:
        title = div.find("span", {"class": "break-words"}).text
    except:
        title = "No title"
    #get img
    img = div.find("img", {"class": "ivm-view-attr__img--centered update-components-image__image update-components-image__image--constrained lazy-image ember-view"})    
    try:
        img = img['src']
        myimgs.append([img])
    except:
        try:
            img = div.find_all("img", {"class": "ivm-view-attr__img--centered update-components-image__image lazy-image ember-view"})   
            for i in img:
                img = i['src']
                myimgs.append([img])
        except:
            img = 'No img'
            myimgs.append([img])
    #get number likes or reactions
    try:
        reactions = div.find("span", {"class": "social-details-social-counts__reactions-count"}).text
    except:
        reactions = 'No reactions'
    
    try:
        shares = div.find("button", {"class": "ember-view t-black--light t-12 hoverable-link-text"}).text.strip()
        
    except:
        shares = 'No shares'
    
    
    comments = div.find_all("div", {"class": "comments-post-meta comments-comment-item__post-meta"})
    if comments:
        
            
        all_comments = div.find_all("span", {"class": "comments-comment-item__main-content feed-shared-main-content--comment t-14 t-black t-normal"})        
        
        for i, each_comment in enumerate(all_comments):
            list_comments = []                
            name_comments = div.find_all("span", {"class": "comments-post-meta__name-text hoverable-link-text mr1"})
            each_comment_text = each_comment.text
            name_comment = name_comments[i].text     
            list_comments.append(name_comment)
            list_comments.append(each_comment_text)
            mylist.append([title,myimgs,reactions,shares,list_comments])
            
    else:
        mylist.append([title,myimgs,reactions,shares,"No comments"])
        
driver.quit()
#save to excel
columns = ["Title","Img", "Reactions", "Shares", "Comments"]
df = pd.DataFrame(mylist, columns=columns)
df.to_excel("linkedin.xlsx",index=False)