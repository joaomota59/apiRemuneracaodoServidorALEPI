# API para o Acesso a Renumeração do Servidor da Assembleia Legislativa do Piauí (ALEPI)

## Instalação das libs
```pip install -r requirements.txt```

## Inicialização da API
```python -m uvicorn apiALEPI:app --reload```


## Rotas

### Referências
> Retorna as referências (ano/mês) que estão disponíveis no site da ALEPI

* Acesso 1: http://127.0.0.1:8000/referencias
* Acesso 2 / Acesso Alternativo - Via Swagger: http://127.0.0.1:8000/docs#/default/read_item_referencias_get

### Folha de Pagamento
> Retorna a folha de pagamento dos servidores da ALEPI, dado como entrada o ano, mês e a paginação.
* Acesso 1: http://127.0.0.1:8000/folha?ano=2023&mes=1&page=1
* Acesso 2 / Acesso Alternativo - Via Swagger: http://127.0.0.1:8000/docs#/default/read_item_folha_get

>Parâmetros de entrada da rota
ano = ano da folha de pagamento Ex: 2020, 2021, 2022, 2023...</br>
mes = mes da folha de pagamento Ex: 1,2,3,4...</br>
Obs: 1 corresponde a Janeiro, 2 a Fevereiro...</br>
page = responsavel pela paginação da folha de pagamento... Ex: 1,2,3,4...

