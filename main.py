import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

PATH = 'E:\chromedriver'
driver = webdriver.Chrome(PATH)

driver.get("https://web.reg.tu.ac.th/registrar/class_info.asp?lang=th")

facultysearch = driver.find_element_by_name("facultyid")

df = pd.DataFrame

df=pd.DataFrame(
    {
        'course_code' : [],
        'course_name' : [],
        'faculty' : [],
        'section' : [],
        'date' : [],
        'professor' : []
    }
)

for option in facultysearch.find_elements_by_tag_name('option'):
    if option.text == 'คณะศิลปกรรมศาสตร์':
        option.click()
        break;

year = driver.find_element_by_name("semester")
for option in year.find_elements_by_tag_name('option'):
    if option.text == '1':
        option.click()
        break;

driver.find_elements_by_xpath('/html/body/table/tbody/tr[1]/td[2]/table/tbody/tr[7]/td[2]/table/tbody/tr/td/font[3]/input')[0].click()

while(True):
    for i in range(4,30) :
        try:
            try:
                a = '/html/body/table/tbody/tr[1]/td[2]/font/font/font/table/tbody/tr['+ str(i) +']/td[5]/font/a/b'
                coursecode = driver.find_element(By.XPATH,a).text
            except:
                coursecode = '-'
            try:
                b = '/html/body/table/tbody/tr[1]/td[2]/font/font/font/table/tbody/tr['+ str(i) +']/td[6]/font'
                coursename = driver.find_element(By.XPATH,b).text
            except:
                coursename
            try:
                fac = '/html/body/table/tbody/tr[1]/td[2]/div[1]/font/b'
                faculty = driver.find_element(By.XPATH,fac).text
            except:
                faculty = '-'
            try:
                sec = '/html/body/table/tbody/tr[1]/td[2]/font/font/font/table/tbody/tr['+ str(i) +']/td[8]/font/b'
                section = driver.find_element(By.XPATH,sec).text
            except:
                section = '-'
            try:
                time = '/html/body/table/tbody/tr[1]/td[2]/font/font/font/table/tbody/tr['+ str(i) +']/td[9]/font'
                date = driver.find_element(By.XPATH, time).text
            except:
                date = '-'
            try:
                p = 'body > table > tbody > tr.ContentBody > td:nth-child(2) > font > font > font > table > tbody > tr:nth-child('+ str(i) +') > td:nth-child(6) > font > font > font > font > font'
                professor = driver.find_element(By.CSS_SELECTOR, p).text
            except:
                professor = '-'

            df = df.append(
                {
                    'course_code': coursecode,
                    'course_name': coursename,
                    'faculty': faculty,
                    'section': section,
                    'date': date,
                    'professor': professor
                }, ignore_index=True
            )

        except:
            break
    try:
        href = driver.find_element(By.PARTIAL_LINK_TEXT, "[หน้าต่อไป]")
        href.click()
    except:
        break


print(df)
df.to_csv('Course.csv', encoding='utf-8-sig')
driver.quit()
