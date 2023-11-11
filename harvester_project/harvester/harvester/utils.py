import requests
import time
from .models import Projeto
from django.db import connection


def harvester_init(retry_interval=5, synthesis_url="http://localhost:5005/harvester_init"):
    retries = 0
    while True:
        try:
            response = requests.get(synthesis_url)
            response.raise_for_status()  # Levanta uma exceção para códigos de erro HTTP
            json_data = response.json()

            # Salvar dados localmente
            for projeto_data in json_data.values():
                projeto = Projeto(
                    name=projeto_data['name'],
                    poco=projeto_data['poco'],
                    um=projeto_data['um'],
                    link_dados_rto=projeto_data['link_dados_rto']
                )
                projeto.save()

            print("Resposta do Synthesis:", json_data)
            break  # Sai do loop se a solicitação for bem-sucedida
        except requests.exceptions.RequestException as e:
            print(f"Erro ao tentar estabelecer conexão com o Síntese: {e}")
            retries += 1
            print(f"Tentando novamente em {retry_interval * retries} segundos...")
            time.sleep(retry_interval * retries)


def clear_table(table_name):
    with connection.cursor() as cursor:
        cursor.execute(f"DELETE FROM {table_name};")


def comunication_harverster_synthesis(sleep_interval=15,
                                      synthesis_url="http://localhost:5005/comunication_harverster_synthesis"):
    while True:
        # Consulta (Coletor) solicita as informações dos últimos dados recebidos ao Síntese. GET
        response = requests.get(synthesis_url)
        # Consulta (Coletor) busca por dados novos na base externa e os recebe caso existam.

        # Consulta (Coletor) envia dados coletados, se houver, para o Síntese. POST

        # A comunicação é repetida rotineiramente de acordo com o tempo estipulado.
        time.sleep(sleep_interval)
