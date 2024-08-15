from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
import cv2

chrome_options= Options()

# chrome_options.add_argument('--headless')
X_OFFSET = 0
Y_OFFSET = 70

# Set up the WebDriver (this example uses Chrome)
driver = webdriver.Chrome()
action = ActionChains(driver)
driver.get(f"https://oa.cc.iitk.ac.in/Oa/Jsp/Main_Frameset.jsp")


driver.find_element(By.XPATH, '/html/body/table/tbody/tr[3]/td[1]/div/a[1]').click()
driver.find_element(By.XPATH, '/html/body/table/tbody/tr[3]/td[1]/div/div[1]/a[1]').click()
time.sleep(3)
div=driver.find_element(By.XPATH, '/html/body/table/tbody/tr[3]/td[2]')
action.move_to_element_with_offset(div, X_OFFSET, Y_OFFSET).click().perform()

time.sleep(3)
element = driver.find_element(By.XPATH, '//*[@id="mainframe"]')

# Extract the src attribute
src_link = element.get_attribute('src')

# Open the src link in the browser
driver.get(src_link)
checkbox = driver.find_element(By.XPATH, '/html/body/form/center[1]/table/tbody/tr[2]/td/input[1]')
checkbox.is_selected()
checkbox.click()


time.sleep(3)
Personal_details=[]
Other_details=[]
Image=[]


for i in range(1,1216):
    input=driver.find_element(By.XPATH, '//*[@id="rollno"]')
    # /html/body/form/div[1]/center/table/tbody/tr[3]/td[2]
    input.click()
    key=240000+i
    input.send_keys(key)
    try:
        input=driver.find_element(By.XPATH, '/html/body/form/div[1]/center/table/tbody/tr[3]/td[3]/input').click()
        name=driver.find_element(By.XPATH, '/html/body/form/div[2]/div/table/tbody/tr/td[3]').text
        Personal_details.append(name)
        print(name)
        other=driver.find_element(By.XPATH, '/html/body/form/div[2]/div/table/tbody/tr/td[4]').text
        Other_details.append(other)
        print(other)
        element = driver.find_element(By.XPATH, '/html/body/form/div[2]/div/table/tbody/tr/td[2]/img')
        # Extract the src attribute
        src_link = element.get_attribute('src')
        print(src_link)
        Image.append(src_link)
    except:
        continue

Data={"Personal Data": Personal_details, "Other details": Other_details}
df=pd.DataFrame(Data)
df.to_csv("Output2.csv", index=False)


