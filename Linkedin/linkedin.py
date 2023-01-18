import time
from selenium import webdriver
# PROXY = "1.2.3.4:2000"
from sqlalchemy import create_engine
from  sqlalchemy.orm import scoped_session ,sessionmaker
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from fake_useragent import UserAgent
ua = UserAgent()
userAgent = ua.random
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument(f'user-agent={userAgent}')
# chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
# chrome_options.add_argument("disable-infobars")
# chrome_options.add_argument("user-agent = Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36")
# chrome_options.add_argument('--ignore-ssl-errors=yes')
# chrome_options.add_argument('--ignore-certificate-errors')
# chrome_options.add_argument('--proxy-server=%s' % PROXY)
chrome_path = 'chromedriver'
driver = webdriver.Chrome(chrome_path, options=chrome_options)
# driver = uc.Chrome(version_main=108)
# driver = webdriver.Chrome()
wait = WebDriverWait(driver, 20)
time.sleep(2)
driver.get('https://www.linkedin.com/checkpoint/rm/sign-in-another-account?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')
time.sleep(6)
email_box=wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='username']")))
driver.implicitly_wait(2)
email_box.send_keys('asadijaz989@gmail.com')
time.sleep(5)
pass_box=wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='password']")))
driver.implicitly_wait(2)
pass_box.send_keys('asdigolaar')
time.sleep(5)
driver.find_element(By.XPATH,"//button[@class='btn__primary--large from__button--floating']").click()
time.sleep(5)
# import pdb;pdb.set_trace()
ActionChains(driver).move_by_offset(50, 50).perform()
time.sleep(2)
KEY_WORD = 'google'
driver.get('https://www.linkedin.com/search/results/all/?keywords={}&origin=HISTORY&sid=MVg'.format(KEY_WORD))
time.sleep(6)
# try:
button = driver.find_element(By.XPATH,"//button[normalize-space()='Companies']")
driver.implicitly_wait(3)
ActionChains(driver).move_to_element(button).click(button).perform()
companies_list = []
companies_list.append(driver.find_element(By.XPATH,"//div[@class='entity-result__item']/div/div/div/div/span/span/a").get_attribute('href'))
time.sleep(6)
people_links = []
for url in companies_list:
    driver.get(url)
    time.sleep(2)
    name = driver.find_element(By.TAG_NAME,"h1").text
    # import pdb;pdb.set_trace()
    driver.find_element(By.XPATH,"//div[@class='display-flex mt2 mb1']/a").click()
    time.sleep(5)
    driver.implicitly_wait(3)
    engine = create_engine('mysql+pymysql://root@localhost/scraping')
    db = scoped_session(sessionmaker(bind=engine))
    list_url = []
    while True:
        employees = driver.find_elements(By.XPATH,"//div[@class='t-roman t-sans']/div/span/span/a")
        time.sleep(5)
        for em in employees:
            e = em.get_attribute('href')
            list_url.append(e)
        time.sleep(2)
        driver.execute_script("window.scrollBy(0, 1000)")
        time.sleep(2)
        try:
            driver.find_element(By.XPATH,"//button[@aria-label='Next']").click()
        except:
            pass
        time.sleep(2)
        if len(employees) < 10:
            break
    for employee in list_url:
        try:
            driver.get(employee)
            time.sleep(1)
            try:
                name = driver.find_element(By.XPATH,"//h1[@class='text-heading-xlarge inline t-24 v-align-middle break-words']").text
                first_name = name.split(" ")[0]
            except:
                first_name = 'Null'
            try:   
                middle_name = name.split(" ")[1]
            except:
                middle_name = 'Null'
            try:
                last_name = name.split(" ")[2]
            except:
                last_name = 'Null'
            experience = driver.find_element(By.XPATH,"//div[@class='text-body-medium break-words']").text
            time.sleep(1)
            try:
                skill = experience.split("|")[0]
            except:
                skill = 'Null'
            try:
                skill1 = experience.split("|")[1]
            except:
                skill1 = 'Null'
            try:
                skill2 = experience.split("|")[2]
            except:
                skill2 = 'Null'
            try:
                skill3 = experience.split("|")[3]
            except:
                skill3 = 'Null'
            try:
                skill4 = experience.split("|")[4]
            except:
                skill4 = 'Null'
            try:
                skill5 = experience.split("|")[5]
            except:
                skill5 = 'Null'
            try:
                skill6 = experience.split("|")[6]
            except:
                skill6 = 'Null'
            try:
                skill7 = experience.split("|")[7]
            except:
                skill7 = 'Null'
            try:
                skill8 = experience.split("|")[8]
            except:
                skill8 = 'Null'
            driver.find_element(By.XPATH,"//a[@id='top-card-text-details-contact-info']").click()
            time.sleep(1)
            try:
                profile_link = driver.find_element(By.XPATH,"//div[@class='pv-contact-info__ci-container t-14']/a").get_attribute('href')
            except:
                profile_link = 'Null'
            sql = "INSERT INTO `persons_record` (`first_name`,`middle_name`,`last_name`,`skill`,`skill1`,`skill2`,`skill3`,`skill4`,`skill5`,`skill6`,`skill7`,`skill8`,`profile_link`) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(first_name,middle_name,last_name,skill,skill1,skill2,skill3,skill4,skill5,skill6,skill7,skill8,profile_link)
            db.execute(sql)
            db.commit()
            print("inserted")
        except:
            pass
print('Done')