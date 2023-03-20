from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import re
from bs4 import BeautifulSoup
import requests
from datetime import datetime as dt
from math import ceil


class AlepiLibrary:

    ### Variaveis estáticas ###
    mesesLabel = {"JANEIRO":1,"FEVEREIRO":2,"MARCO":3,"ABRIL":4,"MAIO":5,"JUNHO":6,"JULHO":7,"AGOSTO":8,"SETEMBRO":9,"OUTUBRO":10,"NOVEMBRO":11,"DEZEMBRO":12,"DECIMO":13}
    mesesNum = {1:"JANEIRO",2:"FEVEREIRO",3:"MARCO",4:"ABRIL",5:"MAIO",6:"JUNHO",7:"JULHO",8:"AGOSTO",9:"SETEMBRO",10:"OUTUBRO",11:"NOVEMBRO",12:"DEZEMBRO",13:"DECIMO"}

    url = "https://alepi.com.br/transparencia/grid_transp_publico_remuneracao"
    s=Service(ChromeDriverManager().install())
    op = webdriver.ChromeOptions()
    
    op.add_argument("headless") #não abre o navegador

    driver = webdriver.Chrome(service=s,options=op)
    
    

    def __init__(self) -> None:
        pass

    def getFolhaPagamento(self, ano:int = 2020, mes:int = 1 ,page:int = 1):
    
        AlepiLibrary.driver.get(AlepiLibrary.url)

        flagExisteMes = False
        for option in AlepiLibrary.driver.find_element(By.ID,"SC_fp_regfolha").find_elements(By.TAG_NAME,"option"):
            if (option.text == f"{AlepiLibrary.mesesNum[mes]}/{ano}" or 
            (mes == 13 and ano == 2018 and option.text == "DECIMO 13 SALARIO/2018") or 
            (mes == 13 and ano == 2017 and option.text == "DECIMO 13 SALARIO/2017")):
                option.click()#clica no mes e ano que foi passado
                AlepiLibrary.driver.find_element(By.XPATH,"//span[contains(text(),'Pesquisa')]").click()
                flagExisteMes=True
                break

        if not flagExisteMes: #se o mes passado não estiver disponivel para download...
            AlepiLibrary.driver.close()
            return "Erro",0
        
        matriz = []

        WebDriverWait(AlepiLibrary.driver, 1).until(EC.frame_to_be_available_and_switch_to_it((By.ID,"nmsc_iframe_grid_transp_publico_remuneracao")))


        while True:
            try:
                if int(AlepiLibrary.driver.find_element(By.CLASS_NAME,"scGridToolbarNavOpen").text)==1: #verifica se a pagina foi carregada
                    AlepiLibrary.driver.execute_script("window.scrollTo(document.body.scrollHeight,0);")
                    break
            except:
                pass

        AlepiLibrary.driver.find_element(By.ID,"rec_f0_bot").clear()
        AlepiLibrary.driver.find_element(By.ID,"rec_f0_bot").send_keys(page)
        AlepiLibrary.driver.find_element(By.ID,"brec_bot").click()

        while True:
            try:
                if int(AlepiLibrary.driver.find_element(By.CLASS_NAME,"scGridToolbarNavOpen").text)==page: #verifica se a pagina foi carregada
                    AlepiLibrary.driver.execute_script("window.scrollTo(document.body.scrollHeight,0);")
                    break
            except:
                pass


        while True:
            try:
                for i in AlepiLibrary.driver.find_elements(By.XPATH,"//img[contains(@id,'b_open_emb_grid_transp_publico_remuneracao_linha_')]") : i.click() #expande a informação de cada servidor
                break
            except:
                AlepiLibrary.driver.execute_script("window.scrollTo(document.body.scrollHeight,0);")
                pass

        
        
        aux = [(re.sub(r"[()]","",re.search(r"\(\d+\)", i.text).group()),re.sub(r"[\d()]","",i.text)) for i in AlepiLibrary.driver.find_elements(By.XPATH,"//span[contains(@id,'id_sc_field_fp_servidor_')]")] 

        id,nome = zip(*aux)
        cargo = [i.text for i in AlepiLibrary.driver.find_elements(By.XPATH,"//span[contains(@id,'id_sc_field_fp_cargo_')]")]
        regime = [i.text for i in AlepiLibrary.driver.find_elements(By.XPATH,"//span[contains(@id,'id_sc_field_fp_regime_')]")]

        descricao = [i.text for i in AlepiLibrary.driver.find_elements(By.XPATH,"//span[contains(@id,'id_sc_field_mv_grupo_')]")]
        valor = [float(i.text.replace(".","").replace(",",".")) for i in AlepiLibrary.driver.find_elements(By.XPATH,"//span[contains(@id,'id_sc_field_mv_valor_')]")]

        corValor = ['C' if i.get_attribute("style") == 'color: rgb(0, 140, 0);' else 'D' for i in AlepiLibrary.driver.find_elements(By.XPATH,"//span[contains(@id,'id_sc_field_mv_valor_')]")] #Verifica se o valor é credito ou debito

        descricaoValor = list(zip(descricao,valor)) #todas descricoes e valores juntos

        quantElementosPorServidor = [int(len(i.find_elements(By.TAG_NAME,"span"))/2) for i in AlepiLibrary.driver.find_elements(By.ID,"sc-ui-grid-body-345a1876")]

        descricaoValorServidor = []

        for quant in quantElementosPorServidor:
            descricaoValorServidor.append(dict(descricaoValor[:quant]))
            del(descricaoValor[:quant])

        matriz.extend(list(zip(id,nome,cargo,regime,descricaoValorServidor)))

        matrizFinal = []

        contCorValor = 0

        for x in matriz:
            totalLiquido = 0
            dicio = {'Id':x[0], 'Nome':x[1], 'Cargo':x[2], 'Regime':x[3],'Referencia':f"{AlepiLibrary.mesesNum[mes]}/{ano}",'DatadeAcesso':dt.now().strftime("%d/%m/%Y %H:%M:%S")}      
            
            rubrica = x[4]

            for i in rubrica:
                if (corValor[contCorValor] == 'C'):
                    
                    totalLiquido += rubrica[i]
                else:
                    totalLiquido = totalLiquido - rubrica[i]
                contCorValor+=1
            dicio.update(rubrica)
            dicio.update({'TotalLiquido':round(totalLiquido,2)})
            matrizFinal.append(dicio)

        numTotalPaginas = ceil(int(AlepiLibrary.driver.find_element(By.CLASS_NAME,"sm_counter").text.split('de ')[-1][:-1])/50)

        return matrizFinal, numTotalPaginas
    

    def referenciasDisponiveis(self) -> dict:

        url = "https://alepi.com.br/transparencia/grid_transp_publico_remuneracao"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        folhasSite = [i.getText().replace("DECIMO 13 SALARIO","DECIMO") for i in soup.find_all("option")]
        folhasSite = [{'ref':i,'mes':AlepiLibrary.mesesLabel[i.split('/')[0]],'ano':i.split('/')[-1]} for i in folhasSite ]
        return {'referencias':folhasSite}