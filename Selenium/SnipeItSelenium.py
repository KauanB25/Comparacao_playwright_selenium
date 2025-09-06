from os import getenv
from dotenv import load_dotenv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep


load_dotenv(override=True)

class SnipeIT:

    def __init__(self,driver):

        self.driver=driver

        #Aguarda até 10 segundos um elemento
        self.wait = WebDriverWait(self.driver, 10)

    def login(self):

        self.driver.get(getenv('url_login'))

        self.driver.find_element(By.ID,"username").send_keys(getenv("user"))

        self.driver.find_element(By.ID,"password").send_keys(getenv("senha"))

        self.driver.find_element(By.ID,'submit').click()
        
    def cadastro(self,numero_serie):

        #Vai até o link de criação do ativo
        self.driver.get("https://demo.snipeitapp.com/hardware/create")
        
        self.driver.find_element(By.ID,'select2-company_select-container').click()

        #Aguarda uma quantidade minima de elementos
        self.wait.until(lambda driver: len(driver.find_elements(By.CSS_SELECTOR, '#select2-company_select-results > li')) >= 5)
        
        opcoes_companhia=self.driver.find_elements(By.CSS_SELECTOR,'#select2-company_select-results > li')

        try:

            opcoes_companhia[2].click()

        except IndexError:
            
            opcoes_companhia[0].click()
        
        self.driver.find_element(By.ID,'serials[1]').send_keys(numero_serie)

        self.driver.find_element(By.ID,'select2-model_select_id-container').click()

        # Aguarda pelo menos 5 opções de modelo
        self.wait.until(lambda driver: len(driver.find_elements(By.CSS_SELECTOR,'#select2-model_select_id-results > li')) >= 5)

        self.driver.find_element(By.XPATH, '//*[@id="select2-model_select_id-results"]/li[3]').click()

        self.driver.find_element(By.ID,'select2-status_select_id-container').click()

        opcoes_status = self.driver.find_elements(By.CLASS_NAME,'select2-results__option')

        opcoes_status[2].click()

        self.driver.find_element(By.ID,'submit_button').click()

    def excluir(self,numero_serie):

        self.driver.find_element(By.ID,'tagSearch').send_keys(numero_serie)

        self.driver.find_element(By.ID,'tagSearch').send_keys(Keys.ENTER)

        self.wait.until(lambda driver: len(self.driver.find_element(By.ID,'assetsListingTable').find_elements(By.TAG_NAME,'a')) >= 3)

        elementos_tag_a=self.driver.find_element(By.ID,'assetsListingTable').find_elements(By.TAG_NAME,'a')

        #analisa a propriedade de link das tags e se o link conter hardware, esse elemento é selecionado
        for elemento in elementos_tag_a:

            link=elemento.get_property('href')

            if 'hardware' in link:
                elemento.click()
                break
        
        self.wait.until(EC.presence_of_element_located((By.ID, 'details')))

        lista_botoes=self.driver.find_element(By.ID,'details').find_elements(By.TAG_NAME,'button')

        #Seleciona o último elemento
        lista_botoes[-1].click()
        
        #Aguarda o elemento ser clicavél
        self.wait.until(EC.element_to_be_clickable((By.ID, 'dataConfirmOK')))

        self.driver.find_element(By.ID,'dataConfirmOK').click()

      