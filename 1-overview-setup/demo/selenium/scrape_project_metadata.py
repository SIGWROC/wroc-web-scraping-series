from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
# Exceptions
from selenium.common.exceptions import NoSuchElementException
import csv
from time import sleep
import chromedriver_autoinstaller

#######################################

#_______SETUP SELENIUM DRIVER_________#

#######################################

chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists
                                      # and if it doesn't exist, download it automatically,
                                      # then add chromedriver to path

#__________DRIVER OPTIONS___________#

options = Options()
options.binary_location = "/Applications/GoogleChrome.app/Contents/MacOS/GoogleChrome"
options = Options()
# options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("window-size=200,200")

driver = webdriver.Chrome(options=options)
driver.set_window_size(800, 800)

# Search the "Code" page with "Machine Learning" keyword sorted by most votes in descending order
driver.get('https://www.kaggle.com/code?sortBy=voteCount&searchQuery=%22Machine+Learning%22&language=Python&types=datasets')

wait = WebDriverWait(driver, 20)
actions = ActionChains(driver)

csv_file = open('./kaggle_covid_competitions_project_data.csv', 'w', encoding='utf-8')
writer = csv.writer(csv_file)

proj_rows = ['kernel_name','kernel_path','vote_count','medal','comment_count']

writer.writerow(proj_rows)

user_url_list = []

#######################################

#__________PROJECT SCRAPING___________#

#######################################


#__________START NEW PAGE___________#

results_page = 0
while results_page < 50:

  print('\n\nPAGE:',(results_page+1),'\n\n')

  sleep(4)

  # parent div for all profiles; returns full list
  # classes are dyncamically changed everyday
  proj_profiles_list = driver.find_elements(By.XPATH, ("//div[contains(@class, 'sc-iNWwEs') and contains(@class, 'hBdoQq')]"))

  #__________START NEW SET OF PROJECTS___________#

  for pp in proj_profiles_list:

    projs_index = proj_profiles_list.index(pp)

    print('\n',('-' * 50))
    print('PROJECT:', (projs_index+1))

    # find profile image and values to check for a link
    proj_profile_img = pp.find_element(By.XPATH, (".//div[contains(@class, 'sc-olbas') and contains(@class, 'MnCfV')]"))

    try:

      # enter
      sleep(2)

      check_proj_profile_anchor = proj_profile_img.find_element(By.XPATH, (".//a"))
      # proj_values_row = get_proj_row(pp)

      print("-" * 50)
      # enter
      sleep(2)

      kaggle_kernels = {}
      
      #### KERNEL NAMES ####
      kernel_name = pp.find_element(By.XPATH, (".//a/child::div/child::div[contains(@class, 'sc-iBkjds') and contains(@class, 'sc-fLlhyt')]")).text
      print('kernel_name:', kernel_name)

      #### KERNEL PATH ####
      kernel_path = pp.find_element(By.XPATH, (".//child::a[contains(@class, 'sc-gFGZVQ') and contains(@class, 'NUNdY')]")).get_attribute('href')[28:]
      print('kernel_path:', kernel_path)
      
      #### VOTES ####
      vote_count = pp.find_element(By.XPATH, (".//child::div[contains(@class, 'sc-ckMVTt') and contains(@class, 'jfwJWs')]/child::div/child::span")).text
      print("vote_count:", vote_count)
      
      #### MEDAL ####
      medal = pp.find_element(By.XPATH, (".//div[contains(@class, 'sc-ckMVTt') and contains(@class, 'jfwJWs')]/child::span/child::span")).text
      print('medal: ', medal)

      #### NUMBER OF COMMENTS ###
      comment_count = pp.find_element(By.XPATH, (".//a[contains(@class, 'sc-dPyBCJ') and contains(@class, 'sc-bBXxYQ')]")).text[:-9]
      print('comment_count:',comment_count)
      
      #### ASSIGN VARS ####
      kaggle_kernels['kernel_name'] = kernel_name
      kaggle_kernels['kernel_path'] = kernel_path
      kaggle_kernels['vote_count'] = vote_count
      kaggle_kernels['medal'] = medal
      kaggle_kernels['comment_count'] = comment_count

      # Append row
      writer.writerow(kaggle_kernels.values())

      sleep(2)
      
    except NoSuchElementException:

      print("-" * 50)
      print('\n\nSKIPPED: MULTIPLE USERS\n',NoSuchElementException,'\n\n')
      sleep(2)

  # CLICK NEW PAGE
  results_page += 1

  # driver.execute_script("window.scrollTo(0,800)") #you can make an adjust 800 or 1000
  nextButton = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//p[@data-testid="selectedPage"]/following-sibling::p')))

  sleep(2)
  
  driver.execute_script("arguments[0].click();", nextButton)

  sleep(4)

driver.close()
csv_file.close()
