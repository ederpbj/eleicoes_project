import os
import sys
import django
import pandas as pd
import datetime

# Adicionar o diretório raiz do projeto ao PYTHONPATH
sys.path.append('/Users/user/dev/Python/Django/eleicoes_project')

# Configurar o Django no script
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eleicoes.settings')
django.setup()

# Agora é possível importar o modelo
from core.models import LocalVotacao

def importar_dados():
    url = 'https://docs.google.com/spreadsheets/d/1lzAXDWS4gkCrDW6uPqfPRFWsBmzNEbaZ/edit?usp=sharing&ouid=111178866198443903759&rtpof=true&sd=true'
    df = pd.read_excel(url, engine='openpyxl')

    # Carregar a planilha Excel
    #df = pd.read_excel('core/Dados_eleições_2024.1.xlsx', engine='openpyxl')


    # Mostrar os nomes das colunas para verificar se estão corretos
    print("Colunas encontradas no arquivo Excel:", df.columns)

    # Iterar pelas linhas do DataFrame e criar objetos LocalVotacao
    for _, row in df.iterrows():
        # Garantir que `data_instalacao` nunca seja nulo
        data_instalacao = pd.to_datetime(row['DATA DA INSTALAÇÃO'], errors='coerce').date() if pd.notna(row['DATA DA INSTALAÇÃO']) else None

        LocalVotacao.objects.create(
            cod=int(row['Cod']) if pd.notna(row['Cod']) else 0,
            opm=row['OPMs'] if pd.notna(row['OPMs']) else '',
            zona=int(row['ZONA']) if pd.notna(row['ZONA']) else 0,
            municipio=row['MUNICÍPIO'] if pd.notna(row['MUNICÍPIO']) else '',
            nome_local=row['NOME DO LOCAL'] if pd.notna(row['NOME DO LOCAL']) else '',
            endereco=row['ENDEREÇO'] if pd.notna(row['ENDEREÇO']) else '',
            bairro=row['BAIRRO'] if pd.notna(row['BAIRRO']) else '',
            qtde_secoes=int(row['QTDE_SECOES']) if pd.notna(row['QTDE_SECOES']) else 0,
            data_instalacao=data_instalacao,  # Garantir que não seja nulo
            horario=row['HORÁRIO'] if pd.notna(row['HORÁRIO']) else '',
            qtde_eleitores=int(row['QTDE_ELEITORES']) if pd.notna(row['QTDE_ELEITORES']) else 0,
            nivel_prioridade=row['NÍVEL DE PRIORIDADE'] if pd.notna(row['NÍVEL DE PRIORIDADE']) else '',
            local_votacao=row['LOCAL DE VOTAÇÃO '] if pd.notna(row['LOCAL DE VOTAÇÃO ']) else '',
            status_urnas=row[' STATUS DAS URNAS'] if pd.notna(row[' STATUS DAS URNAS']) else '',
            status_fiscalizacao=row[' STATUS FISCALIZAÇÃO'] if pd.notna(row[' STATUS DAS URNAS']) else '',
            falta_militar=int(row['FALTA MILITAR']) if pd.notna(row['FALTA MILITAR']) else 0,
        )
    print("Dados importados com sucesso!")

# Executar a importação ao rodar o script
if __name__ == "__main__":
    importar_dados()
