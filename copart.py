import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import pandas as pd


url = ('https://www.copart.co.uk/lotSearchResults?free=false&searchCriteria=%7B%22query%22:%5B%22*%22%5D,'
       '%22sort%22:%5B%22lot_number%20desc%22,%22auction_date_utc%20asc%22%5D,%22watchListOnly%22:false,'
       '%22searchName%22:%22%22,%22freeFormSearch%22:false%7D&displayStr=Search%20vehicles&from=%2FvehicleFinder'
       '%3Fpage%3D4')


def click_next(button):
    try:
        button.click()
    except:
        time.sleep(2)
        click_next(button)


def find_ids(driver):
    try:
        page_ids = driver.find_elements('xpath', '//span[@class="search_result_lot_number p-bold blue-heading ng-star-inserted"]/a')
        page_ids = [x.text for x in page_ids]
        return page_ids
    except:
        time.sleep(3)
        return find_ids(driver)


def copart(url):
    id_list = []
    count = 0
    driver = uc.Chrome()
    wait = WebDriverWait(driver, 30)
    driver.get(url)
    driver.implicitly_wait(30)
    wait.until(EC.visibility_of_element_located(('xpath', '//button[@id="onetrust-accept-btn-handler"]')))
    accept = driver.find_element('xpath', '//button[@id="onetrust-reject-all-handler"]')
    driver.execute_script("arguments[0].scrollIntoView(true);", accept)
    time.sleep(2)
    accept.click()
    page_count = driver.find_element('xpath', '//div[@class="p-paginator-rpp-options p-dropdown p-component"]')
    driver.execute_script("arguments[0].scrollIntoView(true);", page_count)
    wait.until(EC.element_to_be_clickable(('xpath', '//span[@id="pr_id_5_label"]')))
    page_count.click()
    page_count_100 = driver.find_element('xpath', '//ul[@id="pr_id_5_list"]//li[@class="p-ripple p-element p-dropdown-item" and @aria-label="100"]')
    page_count_100.click()
    driver.implicitly_wait(30)
    time.sleep(7)
    while True:
        # wait.until(EC.presence_of_element_located(('xpath', '//table[@id="pr_id_1-table"]')))
        driver.implicitly_wait(30)
        page_ids = find_ids(driver)
        id_list.extend(page_ids)
        count += 1
        print(f'page:{count}----->{len(page_ids)}----{page_ids}')
        try:
            next_button = driver.find_element('xpath', '//button[@class="p-ripple p-element p-paginator-next p-paginator-element p-link"]')
        except:
            break
        driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
        wait.until(EC.presence_of_element_located(('xpath', '//button[@class="p-ripple p-element p-paginator-next p-paginator-element p-link"]')))
        wait.until(EC.visibility_of_element_located(('xpath', '//button[@class="p-ripple p-element p-paginator-next p-paginator-element p-link"]')))
        wait.until(EC.element_to_be_clickable(('xpath', '//button[@class="p-ripple p-element p-paginator-next p-paginator-element p-link"]')))
        click_next(next_button)
        time.sleep(1)
    driver.quit()
    id = pd.DataFrame(id_list, columns=['id'])
    id.to_csv('result_id.csv', index=False)

if __name__ == '__main__':
    copart(url)

