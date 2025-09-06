from os import getenv
from dotenv import load_dotenv
from playwright.sync_api import Page
from time import sleep

load_dotenv(override=True)

class SnipeIT:
    def __init__(self, page: Page):
        self.page = page

    def login(self):
        
        self.page.goto(getenv('url_login'))

        titulo_pagina = self.page.title()
        
        if 'maintenance' in titulo_pagina.lower():
            return False
        else:

            self.page.fill("#username", getenv("user"))

            self.page.fill("#password", getenv("senha"))

            self.page.click("#submit")

            return True
        
    def cadastro(self,numero_serie):

        # Vai até o link de criação do ativo
        self.page.goto("https://demo.snipeitapp.com/hardware/create")
        
        # Clica no seletor de empresa
        self.page.click("#select2-company_select-container")
        
        self.page.wait_for_selector("#select2-company_select-results > li", state="visible")
        
        # Aguarda uma quantidade mínima de elementos
        self.page.wait_for_function("""
            () => document.querySelectorAll('#select2-company_select-results > li').length >= 5
        """)
        
        opcoes_companhia = self.page.query_selector_all("#select2-company_select-results > li")
        
        try:
            opcoes_companhia[2].click()
        except IndexError:
            print(f"Opção selecionada: {opcoes_companhia[0].text_content()}")
            opcoes_companhia[0].click()
        
        self.page.fill("#serials\\[1\\]", numero_serie)
        
        self.page.click("#select2-model_select_id-container")
        
        self.page.wait_for_selector("#select2-model_select_id-results > li", state="visible")
        
        # Aguarda pelo menos 5 opções de modelo
        self.page.wait_for_function("""
            () => document.querySelectorAll('#select2-model_select_id-results > li').length >= 5
        """)
        
        self.page.click("#select2-model_select_id-results > li:nth-child(3)")
        
        self.page.click("#select2-status_select_id-container")
        
        opcoes_status = self.page.query_selector_all(".select2-results__option")
        
        opcoes_status[2].click()
        
        self.page.click("#submit_button")

    def excluir(self,numero_serie):
        self.page.fill('#tagSearch',numero_serie)

        self.page.press('#tagSearch', 'Enter')

        self.page.wait_for_function("""
            () => document.querySelectorAll('#assetsListingTable a').length >= 3
        """)

        elementos_tag_a = self.page.query_selector_all("#assetsListingTable a")

        #analisa a propriedade de link das tags e se o link conter hardware, esse elemento é selecionado
        for elemento in elementos_tag_a:
            link = elemento.get_attribute('href')
            if 'hardware' in link:
                elemento.click()
                break

        self.page.wait_for_selector("#details", state="visible")

        lista_botoes = self.page.query_selector_all("#details button")

        #Seleciona o último elemento
        lista_botoes[-1].click()

        #Aguarda o elemento ser clicavél
        self.page.wait_for_selector("#dataConfirmOK", state="visible")

        self.page.click("#dataConfirmOK")