from selenium.common import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def test_check_search_city(driver):
    driver.get('https://openweathermap.org/')
    search_field = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Search city"]')
    search_field.send_keys('Moscow')
    try:
        driver.find_element(By.XPATH, '//button[text()="Search"]').click()
    except NoSuchElementException:
        raise NoSuchElementException('Поле поиска на найдено')
    driver.implicitly_wait(10)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, 'ul.search-dropdown-menu li:nth-child(1) span:nth-child(1)'))).click()
    WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element(
        (By.CSS_SELECTOR, '.grid-container.grid-4-5 h2'), "Moscow, RU"))
