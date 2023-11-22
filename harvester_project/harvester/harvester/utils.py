import requests
import time


def harvester_init(retry_interval=5, synthesis_url="http://localhost:5500/get_active_projects"):
    retries = 0
    while True:
        try:
            response = requests.get(synthesis_url)
            response.raise_for_status()  # Levanta uma exceção para códigos de erro HTTP
            json_data = response.json()

            print("Projects retrieved:", json_data)
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
                                     synthesis_url="http://localhost:5500/comunication_harverster_synthesis/"):
    tags_urls = {"1": "https://api.chucknorris.io/jokes/random", "2": "https://meowfacts.herokuapp.com/",
                 "3": "https://opentdb.com/api.php?amount=1"}
    while True:
        # Consulta (Coletor) solicita as informações dos últimos dados recebidos ao Síntese. GET

        response = requests.get(synthesis_url)
        json_data = response.json()
        print(f"json_data {json_data}")
        """
        Formato dos dados que irão chegar:
        json_data = {1: { "tags" : { 1 { tag_lastime: timestamp1}, 
                                     2 { tag_lasttime: timestamp2} }
                          "link" : project.link}
        """

        # Consulta (Coletor) busca por dados novos na base externa e os recebe caso existam.
        harvested_data = {}
        for projeto in json_data:
            # data_response = requests.get(projeto['link'])
            data_response = {}
            for tag in json_data[projeto]["tags"]:
                # Essa parte do código está sendo feita dessa forma pra emular mais rapidamente
                # o funcionamento da comunicação
                tag_response = requests.get(tags_urls[tag]).json()
                data_response[tag] = tag_response
            harvested_data[projeto] = data_response

        headers = {'Content-Type': 'application/json'}  # Adicione quaisquer outros headers necessários

        # Consulta (Coletor) envia dados coletados, se houver, para o Síntese. POST
        if harvested_data:
            post_response = requests.post(synthesis_url, json=harvested_data, headers=headers)
            print(f"Status Code: {post_response.status_code}")
            # print("Response Content:", post_response.text)

        # A comunicação é repetida rotineiramente de acordo com o tempo estipulado.
        time.sleep(sleep_interval)
