from selenium import webdriver
from SnipeItSelenium import SnipeIT


driver = webdriver.Chrome()

snipeIt = SnipeIT(driver)

snipeIt.login()

numero_serie='PE0AR5T7'

snipeIt.cadastro(numero_serie)

snipeIt.excluir(numero_serie)

driver.quit()


