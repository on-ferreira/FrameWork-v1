import requests
import time
from django.db import connection


def harvester_init(retry_interval=5, synthesis_url="http://localhost:8000/harvester_init"):
    retries = 0
    while True:
        try:
            response = requests.get(synthesis_url)
            response.raise_for_status()  # Levanta uma exceção para códigos de erro HTTP
            json_data = response.json()

            print("Projects retrived:", json_data)
            return json_data  # Sai do loop se a solicitação for bem-sucedida
        except requests.exceptions.RequestException as e:
            print(f"Error to stablish connection with synthesys: {e}")
            retries += 1
            # Developments is faster without retrying multiplyer
            # print(f"Tentando novamente em {retry_interval * retries} segundos...")
            # time.sleep(retry_interval * retries)
            print(f"Trying again in {retry_interval} seconds...")
            time.sleep(retry_interval)

def comunication_harvester_synthesis(project_list, sleep_interval=15,
                                     synthesis_url="http://localhost:8000/comunication_harverster_synthesis/"):
    while True:
        # Consulta (Coletor) solicita as informações dos últimos dados recebidos ao Síntese. GET
        # TODO: Adicionar um for project in project_list:
        # print("project_list:", project_list.get('1')['name'])
        
            
        response = requests.get(synthesis_url)
        json_data = response.json()

        # TODO: Fazer a lógica de como receber os últimos dados, para buscar por eles.

        # Consulta (Coletor) busca por dados novos na base externa e os recebe caso existam.
        harvested_data = {}
        for projeto_data in json_data.values():
            data_response = requests.get(projeto_data['link'])
            harvested_data[projeto_data['id']] = data_response.json()

        headers = {'Content-Type': 'application/json'}  # Adicione quaisquer outros headers necessários

        # Consulta (Coletor) envia dados coletados, se houver, para o Síntese. POST
        if harvested_data:
            post_response = requests.post(synthesis_url, json=harvested_data, headers=headers)
            print(f"Status Code: {post_response.status_code}")
            # print("Response Content:", post_response.text)

        # A comunicação é repetida rotineiramente de acordo com o tempo estipulado.
        time.sleep(sleep_interval)
