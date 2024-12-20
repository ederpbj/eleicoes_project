import pandas as pd
import os
import django
import sys

# Adicionar o diretório do projeto ao sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Definir a variável de ambiente DJANGO_SETTINGS_MODULE com o nome correto do projeto
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eleicoes.settings')

# Inicializar o Django
django.setup()

from core.models import LocalVotacao


def importar_dados(data_instalacao=None):
    # Caminho para o arquivo Excel dentro da pasta core
    caminho_arquivo = os.path.join(os.path.dirname(__file__), 'Dados_eleições_2024.2.xlsx')

    # Verifique se o arquivo existe
    if not os.path.exists(caminho_arquivo):
        print(f"Arquivo não encontrado: {caminho_arquivo}")
        return

    # Tentar carregar o arquivo Excel local
    try:
        print(f"Carregando o arquivo Excel em: {caminho_arquivo}")
        df = pd.read_excel(caminho_arquivo)
        print("Arquivo Excel carregado com sucesso!")
        print(f"Primeiras linhas do arquivo:\n{df.head()}")  # Exibe as primeiras linhas para verificar o conteúdo
    except Exception as e:
        print(f"Erro ao carregar o arquivo Excel: {e}")
        return

    # Verificar se o DataFrame está vazio
    if df.empty:
        print("Erro: O arquivo Excel está vazio.")
        return

    # Definir as colunas esperadas
    expected_columns = ['COD', 'ZONA', 'NOME DO LOCAL', 'ENDEREÇO', 'BAIRRO', 'CIA', 'SEÇÕES',
                        'INSTALAÇÃO', 'HORÁRIO', 'ELEITORES', 'PRIORIDADE', 'LOCAL DE VOTAÇÃO',
                        'LOCAL DE URNAS', 'FISCALIZAÇÃO']

    # Verificar se todas as colunas esperadas estão presentes no Excel
    print("Verificando as colunas do arquivo...")
    if not all(col in df.columns for col in expected_columns):
        print("Erro: Colunas faltando no Excel.")
        print("Colunas encontradas:", df.columns)
        return

    print(f"Total de registros encontrados: {len(df)}")

    # Iterar pelas linhas do DataFrame e criar objetos LocalVotacao
    for index, row in df.iterrows():
        try:
            cod = int(row['COD']) if pd.notna(row['COD']) else 0
            print(
                f"Processando o registro {index + 1} com o cod {cod}...")  # Adiciona um log para cada linha processada

            # Verificar se o registro já existe no banco
            if LocalVotacao.objects.filter(cod=cod).exists():
                print(f"Registro com o cod {cod} já existe, pulando...")
                continue

            # Criar um novo objeto LocalVotacao
            LocalVotacao.objects.create(
                cod=cod,
                zona=int(row['ZONA']) if pd.notna(row['ZONA']) else 0,
                nome_local=row['NOME DO LOCAL'] if pd.notna(row['NOME DO LOCAL']) else '',
                endereco=row['ENDEREÇO'] if pd.notna(row['ENDEREÇO']) else '',
                bairro=row['BAIRRO'] if pd.notna(row['BAIRRO']) else '',
                secoes=int(row['SEÇÕES']) if pd.notna(row['SEÇÕES']) else 0,
                data_instalacao=row['INSTALAÇÃO'] if pd.notna(row['INSTALAÇÃO']) else data_instalacao,
                horario=row['HORÁRIO'] if pd.notna(row['HORÁRIO']) else '',
                eleitores=int(row['ELEITORES']) if pd.notna(row['ELEITORES']) else 0,
                prioridade=row['PRIORIDADE'] if pd.notna(row['PRIORIDADE']) else '',
                local_votacao=row['LOCAL DE VOTAÇÃO'] if pd.notna(row['LOCAL DE VOTAÇÃO']) else '',
                local_urnas=row['LOCAL DE URNAS'] if pd.notna(row['LOCAL DE URNAS']) else '',
                fiscalizacao=row['FISCALIZAÇÃO'] if pd.notna(row['FISCALIZAÇÃO']) else '',
                cia=row['CIA'] if pd.notna(row['CIA']) else ''
            )
            print(f"Registro com o cod {cod} criado com sucesso.")
        except Exception as e:
            print(f"Erro ao processar o registro {index + 1}: {e}")

    print("Dados importados com sucesso!")
