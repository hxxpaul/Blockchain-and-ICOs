
# coding: utf-8

# # Scrape data from tokendata.io
# 

# In[12]:


from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
from selenium import webdriver
import pandas as pd
import time


# ### Data from "token sales" tag
# - Using selenium package, simulate page down operation until reaching the last page
# - Scrape text or url in each designed attribute of each ICO
# - Successfully scraped all 2340 ICOs published on tokendata.io

# In[14]:


# data from "token sales" tag
## set driver
driver_path = 'C:/Users/Administrator/chromedriver.exe'
driver = webdriver.Chrome(driver_path)
driver.get('https://www.tokendata.io/')
time.sleep(1)

homepage, name, blurb, symbol, status, usd_raised = [],[],[],[],[],[]
duration, month, sale_price, current_price, current_return, whitepaper = [],[],[],[],[],[]

## define a function to scrape data
def scraper():
    # list of tr tags in one page
    tr_list = driver.find_elements_by_css_selector('table[id="sample_1"] tbody tr[role="row"]')
    # list of td tags in one tr tag
    for tr in tr_list:
        td_list = tr.find_elements_by_css_selector('td')
        # scrape data in each td tag
        ## homepage link
        if len(td_list[0].find_elements_by_css_selector('a')) != 0:
            homepage.append(td_list[0].find_elements_by_css_selector('a')[0].get_attribute('href'))
        else:
            homepage.append('')
        ## name
        name.append(td_list[1].text)
        ## blurb
        if len(td_list[1].find_elements_by_css_selector('span')) != 0:
            blurb.append(td_list[1].find_elements_by_css_selector('span')[0].get_attribute('data-original-title'))
        else:
            blurb.append('')
        ## symbol
        symbol.append(td_list[2].text)
        ## status
        status.append(td_list[3].text)
        ## usd_raised
        usd_raised.append(td_list[4].text)
        ## duration
        if len(td_list[5].find_elements_by_css_selector('span')) != 0:
            duration.append(td_list[5].find_elements_by_css_selector('span')[0].get_attribute('data-original-title'))
        else:
            duration.append('')
        ## month
        month.append(td_list[5].text)
        ## sale_price
        sale_price.append(td_list[6].text)
        ## current_price
        current_price.append(td_list[7].text)
        ## current_return
        current_return.append(td_list[8].text)
        ## whitepaper link
        if len(td_list[9].find_elements_by_css_selector('a')) != 0:
            whitepaper.append(td_list[9].find_elements_by_css_selector('a')[0].get_attribute('href'))
        else:
            whitepaper.append('')

## scrape data page by page
### when current page is not the last one
while 'paginate_button next disabled' not in [li.get_attribute('class')                                              for li in driver.find_elements_by_css_selector('ul[class="pagination"] li')]:
    scraper()
    # click to the next page 
    next_button = driver.find_elements_by_css_selector('ul[class="pagination"] li[class="paginate_button next"] a')
    next_button[0].click()
### when current page is the last one
else: 
    scraper()

driver.quit()


# In[16]:


# save results into dataframe
data = [homepage, name, blurb, symbol, status, usd_raised, duration, month, sale_price, current_price, current_return, whitepaper]
header = ['homepage', 'name', 'blurb', 'symbol', 'status', 'usd_raised', 'duration',
          'month', 'sale_price', 'current_price', 'current_return', 'whitepaper']
df = pd.DataFrame(data).T.replace({'': None})
df.columns = header
df.describe()

# dataframe shape with/without missing value
print('dataframe shape with missing value:', df.shape)
df.head(3)
print('dataframe shape without missing value:', df.dropna().shape)
df.dropna().head(3)

# save to csv
#df.to_csv('C:/Users/Administrator/Desktop/SIT/ICO/tokendata.io.csv', index = False)

