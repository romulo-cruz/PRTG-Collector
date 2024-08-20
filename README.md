# PRTG Sensor Data Collector

Este script coleta dados de sensores de um servidor PRTG e os salva em um arquivo CSV. Ele permite a escolha de diferentes tipos de sensores e status para obter dados específicos ou todos os sensores disponíveis.

## Funcionalidades

- **Escolha de Sensores:** O script permite escolher entre diferentes tipos de sensores (Ping, Disco, Memória) ou coletar dados de todos os sensores.
- **Filtragem por Status:** O usuário pode escolher filtrar os sensores por status (disponíveis, indisponíveis, todos).
- **Armazenamento em CSV:** Os dados coletados são armazenados em um arquivo CSV no diretório especificado.

## Utilidades

- **Coleta de Dados:** Coleta dados de sensores do PRTG Network Monitor com base em status e tags definidos pelo usuário.
- **Geração de Relatórios:** Salva os dados coletados em um arquivo CSV, facilitando a análise posterior.
- **Atualização de Dashboards:** Pode ser utilizado para atualizar dashboards em tempo real.
- **Sincronização com Excel:** Os dados coletados podem ser sincronizados diretamente com o Excel para relatórios ou análise.
- **Transformação em Banco de Dados:** Os dados CSV podem ser transformados em um banco de dados atualizável, considerando que o arquivo pode ser gerado em intervalos curtos de tempo.

## Pré-requisitos

Antes de executar o script, certifique-se de ter instalado o Python 3.x e as seguintes bibliotecas:

```bash
pip install requests
```

## Estrutura de Arquivos

arquivo_de_credenciais.txt: Contém as credenciais e a URL do servidor PRTG. Este arquivo deve ser salvo no diretório C:\Users\youruser\desktop\softwares\PRTG Collector\Tags\ com o seguinte formato:

```
coreserver
username
passhash
```

arquivo_de_tags_ping.txt, arquivo_de_tags_disco.txt, arquivo_de_tags_memoria.txt: Arquivos de texto que contêm as tags dos sensores. Devem estar no mesmo diretório que o arquivo de credenciais.

Configuração

Credenciais:
Altere o arquivo chamado arquivo_de_credenciais.txt no diretório C:\Users\youruser\desktop\softwares\PRTG Collector\Tags\.
Preencha o arquivo com as informações do servidor PRTG, nome de usuário e passhash. Exemplo:

```
core.prtg.com
your.user
123456890
```

Tags de Sensores:

Altere o arquivo chamado arquivo_de_tags_ping.txt, arquivo_de_tags_disco.txt, arquivo_de_tags_memoria.txt no mesmo diretório do arquivo de credenciais.
Cada arquivo deve conter as tags relacionadas ao tipo de sensor correspondente. Exemplo de conteúdo de arquivo_de_tags_disco.txt:

```
diskfree
diskhealthsensor
```

## Como Usar

Execute o script Python. Será solicitado que você escolha um tipo de sensor:

Qual o tipo de sensor que você deseja obter?
(1) Ping
(2) Disco
(3) Memória
(9) Todos os sensores

Em seguida, será solicitado que você escolha o status dos sensores:

Qual o status dos sensores que você deseja obter?
(1) Disponíveis
(2) Indisponíveis
(3) Todos os status

O script irá coletar os dados dos sensores conforme a escolha e salvará as informações em um arquivo CSV no diretório a ser definido como por exemplo C:\Users\youruser\Desktop\ com o nome alertas.csv.

O script entrará em um loop, realizando a coleta de dados a cada 5 horas. (Caso queira o valor pode ser alterado):

Exemplo: 60 segundos
```
time.sleep(60)
```


## Contribuição

Contribuições são bem-vindas! Se você tiver sugestões de melhorias ou encontrar problemas, sinta-se à vontade para abrir uma issue ou enviar um pull request.

