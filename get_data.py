from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time, os, json


options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')

#Barra de progreso sacada de https://stackoverflow.com/questions/3173320/text-progress-bar-in-terminal-with-block-characters
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    return f'\r{percent}% {suffix}\n|{bar}|'
    # Print New Line on Complete
    if iteration == total: 
        print()

def conseguirJson(path):
    with open(path, "r") as read_file:
        data = json.load(read_file)
    return data

def guardarCfes(list,port):
    with open(f"./outputs/data_{port}.json", "w") as write_file:
        json.dump(list, write_file)

def conseguirCFEs(driver,rut,passw,port):
    driver.get(f'https://cfe.rondanet.com:{port}/CFERondanetServerProd/login.xhtml')
    time.sleep(2)    
    actual = {}
    #Ingresar RUT
    driver.find_element(By.XPATH,'//*[@id="loginForm:empresa"]').click()
    elem = driver.find_element(By.XPATH,'//*[@id="loginForm:empresa"]')
    elem.send_keys(f'{rut}')
    #Ingresar admin
    driver.find_element(By.XPATH,'//*[@id="loginForm:empresa"]').click()
    elem = driver.find_element(By.XPATH,'//*[@id="loginForm:username"]')
    elem.send_keys("admin")
    #Ingresar pass
    driver.find_element(By.XPATH,'//*[@id="loginForm:empresa"]').click()
    elem = driver.find_element(By.XPATH,'//*[@id="loginForm:lblPassword"]')
    elem.send_keys(f'{passw}')
    #Click ingresar
    driver.find_element(By.XPATH,'//*[@id="loginForm:btnIngresar"]').click()
    
    get_url = driver.current_url
    while(len(get_url) <= 64):
        get_url = driver.current_url

    #Hover en CFE
    element_to_hover_over = driver.find_element(By.XPATH,'//*[@id="j_idt14:j_idt17_label"]')
    hover = ActionChains(driver).move_to_element(element_to_hover_over)
    hover.perform()
    time.sleep(0.75)

    #Click en Gestión CFE
    driver.find_element(By.XPATH,'//*[@id="j_idt14:j_idt18"]').click()
    time.sleep(0.75)
    #Click en filtros
    driver.find_element(By.XPATH,'//*[@id="cFESelections:j_idt77"]').click()
    time.sleep(0.75)
    #Click en Emision desde
    driver.find_element(By.XPATH,'//*[@id="cFESelections:calendarEDInputDate"]').click()
    time.sleep(0.75)
    #Click en mes menos
    driver.find_element(By.XPATH,'/html/body/div/div[2]/form[2]/div[8]/div[4]/div/div[4]/div[2]/table/tbody/tr[1]/td[2]/div/div/table/tbody/tr[1]/td/table/tbody/tr/td[2]/div').click()
    time.sleep(0.75)
    #Click en fecha 26
    driver.find_element(By.XPATH,'//*[text()="26"]').click()


    #Click en Emision Hasta
    driver.find_element(By.XPATH,'//*[@id="cFESelections:calendarEHPopupButton"]').click()
    time.sleep(0.75)
    #Click en Hoy
    driver.find_element(By.XPATH,'/html/body/div/div[2]/form[2]/div[8]/div[4]/div/div[4]/div[2]/table/tbody/tr[1]/td[4]/div/div/table/tbody/tr[9]/td/table/tbody/tr/td[5]/div').click()
    time.sleep(0.75)
    #Click en aplicar filtros
    driver.find_element(By.XPATH,'//*[@id="cFESelections:j_idt304"]').click()
    time.sleep(1)
    #Extraer cantidad de facturas
    cfeEQ = int(WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#cFESelections\:cfeDataTable\:cantidadRegistros"))).get_attribute("innerHTML"))
    time.sleep(0.75)

    #Click en filtros
    driver.find_element(By.XPATH,'//*[@id="cFESelections:j_idt77"]').click()
    time.sleep(0.75)
    #Click en recibidos
    driver.find_element(By.XPATH,'//*[@id="cFESelections:cfeRec:1"]').click()  
    time.sleep(0.75)
    #Click en aplicar filtros
    driver.find_element(By.XPATH,'//*[@id="cFESelections:j_idt304"]').click()
    time.sleep(1)
    #Extraer cantidad de facturas
    cfeRQ = int(WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#cFESelections\:cfeDataTable\:cantidadRegistros"))).get_attribute("innerHTML"))
    time.sleep(0.75)

  #Ver reportes
    #Hover en CFE
    element_to_hover_over = driver.find_element(By.XPATH,'//*[@id="j_idt14:j_idt28_label"]')
    hover = ActionChains(driver).move_to_element(element_to_hover_over)
    hover.perform()
    time.sleep(0.75)
    #Click en Gestion de reportes
    driver.find_element(By.XPATH,'//*[@id="j_idt14:j_idt29"]').click()
    time.sleep(1)
    #Click abrir calendario Emision desde
    driver.find_element(By.XPATH,'//*[@id="ReportesDiarios:repoDesdePopupButton"]').click()
    time.sleep(0.75)
    #Click en Hoy
    driver.find_element(By.XPATH,'/html/body/div/div[2]/form[1]/div/div[2]/div[1]/div/table/tbody/tr/td[2]/div/div/table/tbody/tr[9]/td/table/tbody/tr/td[5]/div').click()
    time.sleep(0.75)
    #Click abrir calendario Emision desde
    driver.find_element(By.XPATH,'//*[@id="ReportesDiarios:repoDesdePopupButton"]').click()
    time.sleep(0.75)
    #Click en mes menos
    driver.find_element(By.XPATH,'/html/body/div/div[2]/form[1]/div/div[2]/div[1]/div/table/tbody/tr/td[2]/div/div/table/tbody/tr[1]/td/table/tbody/tr/td[2]/div').click()
    time.sleep(0.75)
    #Click en fecha 26
    driver.find_element(By.XPATH,'//*[text()="26"]').click()
    #Click en Buscar
    driver.find_element(By.XPATH,'//*[@id="ReportesDiarios:j_idt108"]').click()
    time.sleep(1)
    #Extraer cantidad de facturas
    reportQ = int(WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div[2]/form[1]/div/div[2]/div[2]/div/div[2]/div/table[1]/tbody/tr/td[2]/label"))).get_attribute("innerHTML"))
    time.sleep(0.75)

    #Click en Salir
    driver.find_element(By.XPATH,'//*[@id="j_idt14:j_idt60"]').click()
    time.sleep(0.75)

    cantQTot = cfeEQ+cfeRQ+reportQ
    actual = {f"{rut}":f"{cantQTot}"}
    return actual

def main(port,rut,driver):
        time.sleep(2)
        cfes = {}

        driver_path = ".\chromedriver_win32\chromedriver.exe"

        os.system("clear||cls")
        cfes = conseguirJson(f"./outputs/data_{port}.json")
        for rut,passw in rut.items():
            if len(rut) == 12:
                cfe = conseguirCFEs(driver,rut,passw,port)
                cfes.update(cfe)
        guardarCfes(cfes,port) 