from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import re
from bs4 import BeautifulSoup
import requests
import json


def referenciasDisponiveis():

    mesesLabel = {"JANEIRO":1,"FEVEREIRO":2,"MARCO":3,"ABRIL":4,"MAIO":5,"JUNHO":6,"JULHO":7,"AGOSTO":8,"SETEMBRO":9,"OUTUBRO":10,"NOVEMBRO":11,"DEZEMBRO":12,"DECIMO":13}

    url = "https://alepi.com.br/transparencia/grid_transp_publico_remuneracao"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    folhasSite = [i.getText().replace("DECIMO 13 SALARIO","DECIMO") for i in soup.find_all("option")]
    folhasSite = [{'ref':i,'mes':mesesLabel[i.split('/')[0]],'ano':i.split('/')[-1]} for i in folhasSite ]
    return {'referencias':folhasSite}