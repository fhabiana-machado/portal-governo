from copy import deepcopy
from pathlib import Path

import json
import logging
import requests
import csv

# Define como faremos o log das ações
logging.basicConfig()
logger = logging.getLogger("portal.goveno.popula")
logger.setLevel(logging.INFO)

# Constantes utilizadas no script
PASTA_ATUAL = Path(__file__).parent.resolve()
PASTA_DADOS = PASTA_ATUAL / "dados"
PASTA_TEMPLATES = PASTA_ATUAL / "templates"
ARQUIVO_CSV = PASTA_ATUAL / "secretarias_rio_grande_do_sul_completo.csv"
BASE_URL="http://localhost:8080/Plone/++api++"
USUARIO="admin"
SENHA="admin"

# Cabeçalhos HTTP
headers = {
    "Accept": "application/json"
}

session = requests.Session()
session.headers.update(headers)

# Autenticar o usuário admin utilizando um Token JWT
login_url = f"{BASE_URL}/@login"
response = session.post(login_url, json={"login": USUARIO, "password": SENHA})
data = response.json()
token = data["token"]
session.headers.update(
    {"Authorization": f"Bearer {token}"}
)

def popula_templates() -> dict:
    suffix = ".json"
    templates = {}
    arquivos = PASTA_TEMPLATES.glob("*.json")
    for arquivo in arquivos:
        tipo = arquivo.name[:-len(suffix)]
        dados = json.loads(arquivo.read_text())
        templates[tipo] = dados
    return templates

# Popula os templates por tipo de conteúdo
templates = popula_templates()

CONTEUDO_RAIZ = {
    "/secretarias": {
        "id": "secretarias",
        "@type": "Document",
        "title": "Secretarias",
        "descricao": "Secretarias do Estado do Rio Grande do Sul"
    }
}

# Criar Pasta Raiz
path = "/secretarias"
data = CONTEUDO_RAIZ[path]

response = session.get(f"{BASE_URL}{path}")
if response.status_code != 404:
    logger.info(f"Ignorando {BASE_URL}{path}: Conteúdo já existe")
else:
    # Identificamos qual o tipo de conteúdo será criado
    tipo = data["@type"]
    # Criamos uma nova varíavel com a cópia dos dados originais
    payload = deepcopy(templates.get(tipo, {}))
    # Aplicamos os dados recebidos de CONTEUDO_RAIZ
    payload.update(data)
    response = session.post(f"{BASE_URL}/{path}", json=payload)
    if response.status_code > 300:
        logger.error(f"Erro ao criar pasta raiz '{path}': {response.status_code}")
    else:
        logger.info(f"Conteúdo criado: '{path}'")

# Popular dados de conteúdos
dados_csv = []
with open(ARQUIVO_CSV, "r") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        dados_csv.append(row)
        
# Parse de conteúdos
CONTEUDOS = {}
for item in dados_csv:
    path_parent = ""
    path = f"secretarias/{item['Id']}"
    CONTEUDOS[path] = {
        "id": "cultura",
        "@type": item['Id'],
        "title": item['Secretaria'],
        "description": "Secretaria do Governo do Estado do Rio Grande do Sul",
        "telefone": item['Telefone'],
        "email": item['E-mail'],
    }
    path_pessoa = f"{path}/{item['Responsável Id']}"
    CONTEUDOS[path_pessoa] = {
        "id": item['Responsável Id'],
        "@type": "Pessoa",
        "title": item['Responsável'],
        "cargo": item['Telefone'],
        "email": item['E-mail'],
    }

# Criar Conteúdos
for path in CONTEUDOS:
    logger.info(CONTEUDOS[path])
    data = CONTEUDOS[path]
    parent_path = "/".join(path.split("/")[:-1])[1:]

    response = session.get(f"{BASE_URL}/{path}")
    if response.status_code == 404:
        # Identificamos qual o tipo de conteúdo será criado
        tipo = data["@type"]
        # Criamos uma nova varíavel com a cópia dos dados originais
        payload = deepcopy(templates.get(tipo, {}))
        # Aplicamos os dados recebidos de CONTEUDOS
        payload.update(data)
        response = session.post(f"{BASE_URL}/{parent_path}", json=payload)
        if response.status_code > 300:
            logger.error(f"Erro ao criar '{path}': {response.status_code}")
            continue
        else:
            logger.info(f"Conteúdo criado: '{path}'")
    else:
        logger.info(f"Conteúdo existente: '{path}'")

    dados = response.json()
    if dados["review_state"] == "private":
        payload = {
            "comment": "Transição feita na importação"
        }
        response = session.post(f"{BASE_URL}/{path}/@workflow/publish", json=payload)
        if response.status_code > 200:
            logger.error(f"Erro ao transicionar '{path}' para publicado: {response.status_code}")
            continue
        else:
            logger.info(f"Conteúdo publicado: '{path}'")
    else:
        logger.info(f"Conteúdo já publicado: '{path}'")