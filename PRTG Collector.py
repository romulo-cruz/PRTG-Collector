import requests
import csv
import urllib3
from datetime import datetime
import os
import time

# Desativar avisos de segurança temporariamente (evitar problemas em casos de certificação etc)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Função pra obter credenciais e URL do PRTG
def get_credentials(filepath):
    with open(filepath, 'r') as file:
        lines = file.readlines()
        coreserver = lines[0].strip()
        username = lines[1].strip()
        passhash = lines[2].strip()

        # Evitando necessidade de http:// em arquivo de credenciais.txt
        if not coreserver.startswith('http://') and not coreserver.startswith('https://'):
            coreserver = 'https://' + coreserver

    return coreserver, username, passhash

# Função para carregar as tags de um arquivo de texto
def load_tags(filepath):
    tags = []
    with open(filepath, 'r') as file:
        for line in file:
            tag = line.strip()
            if tag and not tag.startswith("#"):  # Ignorar linhas vazias e comentários
                tags.append(tag)
    return tags

# Função para escolher o tipo de sensor
def choose_sensor():
    print("Qual o tipo de sensor que você deseja obter?")
    print("(1) Ping")
    print("(2) Disco")
    print("(3) Memória")
    print("(9) Todos os sensores")

    choice = input("Escolha o sensor (1/2/3/9): ").strip()
#importante definir a localidade correta do arquivo 
#caso queira adicionar tags personalizadas, os arquivos de texto devem ser editados conforme necessário
    if choice == "1":
        return "C:\\Users\\youruser\\desktop\\PRTG Collector\\Data\\Tags\\arquivo_de_tags_ping.txt"
    elif choice == "2":
        return "C:\\Users\\youruser\\desktop\\PRTG Collector\\Data\\Tags\\arquivo_de_tags_disco.txt"
    elif choice == "3":
        return "C:\\Users\\youruser\\desktop\\PRTG Collector\\Data\\Tags\\arquivo_de_tags_memoria.txt"
    elif choice == "9":
        return ""  # Sem filtros de tags, trará todos os sensores
    else:
        print("Escolha inválida. Tente novamente.")
        return choose_sensor()

# Função para escolher o status dos sensores
def choose_status():
    print("Qual o status dos sensores que você deseja obter?")
    print("(1) Disponíveis")
    print("(2) Indisponíveis")
    print("(3) Todos os status")

    choice = input("Escolha o status (1/2/3): ").strip()

    if choice == "1":
        return [2, 3]  # Exemplo: Status 3 = Disponível
    elif choice == "2":
        return [5, 13]  # Exemplo: Status 5 e 13 = Indisponível
    elif choice == "3":
        return []  # Status vazio trará todos os sensores, independentemente do status
    else:
        print("Escolha inválida. Tente novamente.")
        return choose_status()

# Diretório e nome do arquivo de saída - IMPORTANTE ALTERAR PARA ONDE O ARQUIVO DEVE SAIR
OUTPUT_DIR = r"C:\Users\Youruser\Desktop"
OUTPUT_FILE = "nomedoarquivo.csv"

def get_sensors(prtg_url, username, passhash, tags, status):
    tag_filters = ''.join(f"&filter_tags=@tag({tag})" for tag in tags)
    status_filters = ''.join(f"&filter_status={status}" for status in status)
    
    url = f"{prtg_url}/api/table.json?content=sensors&columns=objid,probe,group,device,status,downtime,lastvalue,message{status_filters}{tag_filters}&username={username}&passhash={passhash}"
    
    response = requests.get(url, verify=False)
    
    if response.status_code == 200:
        data = response.json()
        return data['sensors']
    else:
        print(f"Erro ao buscar dados: {response.status_code}")
        return []

#Aqui você pode definir a ordem na qual vai escolher quais valores devem ser coletados
def save_to_csv(sensors, directory, filename):
    filepath = os.path.join(directory, filename)
    with open(filepath, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['objid', 'probe', 'group', 'device', 'status', 'downtime', 'lastvalue', 'message'])
        for sensor in sensors:
            writer.writerow([
                sensor['objid'],
                sensor['probe'],
                sensor['group'],
                sensor['device'],
                sensor['status'],
                sensor['downtime'],
                sensor['lastvalue'],
                sensor['message']
            ])
    print(f"Relatório salvo em {filepath}")

def main():
    # Caminho para o arquivo de credenciais #necessário edita-lo para funcionamento do programa
    cred_file = "C:\\Users\\youruser\\desktop\\PRTG Collector\\Data\\arquivo_de_credenciais.txt"
    
    coreserver, username, passhash = get_credentials(cred_file)
    
    # Escolher o tipo de sensor e carregar as tags correspondentes
    tags_file = choose_sensor()
    if tags_file:
        tags = load_tags(tags_file)
    else:
        tags = []  # Sem tags específicas para 'Todos os sensores'

    # Escolher o status dos sensores
    status = choose_status()

    while True:
        print("Iniciando coleta de dados de disponibilidade...")
        print(f"[+] {datetime.now()}")

        sensors = get_sensors(coreserver, username, passhash, tags, status)

        if sensors:
            save_to_csv(sensors, OUTPUT_DIR, OUTPUT_FILE)
        else:
            print("Nenhum sensor encontrado.")

        print("Coleta de dados finalizada.")
        print(f"[+] {datetime.now()}")


        # Aqui você pode definir a cada quantos segundos o seu arquivo vai ser gerado pra alimentar o que quer que seja
        # Exemplo: time.sleep(60) - Reiniciar a cada 60 segundos
        
                # Pausar a execução por 5 horas (5 * 60 * 60 segundos) 
        time.sleep(5 * 60 * 60)

if __name__ == "__main__":
    main()
