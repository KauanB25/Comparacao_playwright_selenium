from playwright.sync_api import sync_playwright
from SnipeItPlaywright import SnipeIT
from time import sleep


with sync_playwright() as p:
    # Inicia o navegador (Chrome por padrão)
    browser = p.chromium.launch(headless=False,channel='chrome')
    
    page = browser.new_page()
    
    snipeIt = SnipeIT(page)
    
    numero_serie='PE0AR5T7'
    snipeIt.login()
    
    snipeIt.cadastro(numero_serie)
    
    snipeIt.excluir(numero_serie)

    browser.close()
