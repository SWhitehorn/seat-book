from selenium import webdriver
from selenium.webdriver.support.ui import Select
import datetime

firefoxOptions = webdriver.FirefoxOptions()
firefoxOptions.set_headless()
driver = webdriver.Firefox(firefox_options=firefoxOptions)

# Get user credentials
username = input('Username: ')
password = input('Password: ')

# Open browser
driver.get("https://roombookings.exeter.ac.uk/study-streathamcampusforum2020/Login.aspx?ReturnUrl=%2fstudy-streathamcampusforum2020%2f%3fqitq%3d07376081-e72e-4244-9dce-1517b6a4b0af%26qitp%3d05690489-9e9d-4f2b-99fa-9e9c4c9ddbba%26qitts%3d1601125061%26qitc%3dexeter%26qite%3dstudyforum2020%26qitrt%3dSafetynet%26qith%3da7213316847b7a4f52603d6b4e119a97")
assert 'Student Study Spaces Booking System' in driver.title

# Login
driver.find_element_by_css_selector('#ctl00_Main_UsernameBox').send_keys(username)
driver.find_element_by_css_selector('#ctl00_Main_PasswordBox').send_keys(password)
driver.find_element_by_css_selector('#ctl00_Main_LoginBtn').click()

# Choose room
select = Select(driver.find_element_by_css_selector('#ctl00_Main_Room1_ZoneList'))
select.select_by_visible_text('Forum')

# Get tomorrow's date
date = datetime.datetime.now() + datetime.timedelta(days=3)
element = driver.find_element_by_xpath(f"//*[text()='{date.day}']")

# Iterate through calender until next available day found
while True:
    element = driver.find_element_by_xpath(f"//*[text()='{date.day}']")
    if element.get_attribute('disabled') == 'true':
        date += datetime.timedelta(days=1)
    else:
        element.click()
        break

# Submit location and day preferences
driver.find_element_by_css_selector('#ctl00_Main_ShowOptionsBtn').click()

# Pick first room available and submit
driver.find_element_by_css_selector('#ctl00_Main_OptionSelector_OptionsGrid_ctl02_rdoSingle').click()
driver.find_element_by_css_selector('#ctl00_Main_SelectOptionButton').click()
driver.find_element_by_css_selector('#ctl00_Main_MakeBookingBtn').click()

driver.close()