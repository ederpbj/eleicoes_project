import pandas as pd
import os
import django

# Definir a variável de ambiente DJANGO_SETTINGS_MODULE antes de inicializar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eleicoes.settings')

# Inicializar o Django
django.setup()

from core.models import LocalVotacao


def importar_dados(data_instalacao=None):
    # URL de exportação do Google Sheets em formato CSV
    url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQ_zsvB3KzJNeBpeQ36WgpYxXkjFswXZUfCR1hmXIZbWFIuNZoqRtEAXkg7MJWY_A/pub?output=csv'

    # Tentar carregar o arquivo CSV diretamente da URL
    try:
        df = pd.read_csv(url)
        print("Dados do Google Sheets carregados com sucesso!")
        print(df.head())  # Exibe as primeiras linhas do arquivo para verificar o conteúdo
    except Exception as e:
        print(f"Erro ao carregar o arquivo CSV do Google Sheets: {e}")
        return

    # Definir as colunas esperadas
    expected_columns = ['COD', 'ZONA', 'NOME DO LOCAL', 'ENDEREÇO', 'BAIRRO', 'CIA', 'SEÇÕES',
                        'INSTALAÇÃO', 'HORÁRIO', 'ELEITORES', 'PRIORIDADE', 'LOCAL DE VOTAÇÃO',
                        'LOCAL DE URNAS', 'FISCALIZAÇÃO']

    # Verificar se todas as colunas esperadas estão presentes no CSV
    if not all(col in df.columns for col in expected_columns):
        print("Erro: Colunas faltando no CSV.")
        print("Colunas encontradas:", df.columns)
        return

    print(f"Total de registros encontrados: {len(df)}")

    # Iterar pelas linhas do DataFrame e criar objetos LocalVotacao
    for index, row in df.iterrows():
        print(f"Processando o registro {index + 1} com o cod {row['COD']}...")  # Adiciona um log para cada linha processada

        # Verificar se o registro já existe no banco
        if LocalVotacao.objects.filter(cod=int(row['COD'])).exists():
            print(f"Registro com o cod {row['COD']} já existe, pulando...")
            continue

        # Criar um novo objeto LocalVotacao
        try:
            LocalVotacao.objects.create(
                cod=int(row['COD']) if pd.notna(row['COD']) else 0,
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
            print(f"Registro com o cod {row['COD']} criado com sucesso.")
        except Exception as e:
            print(f"Erro ao criar o registro com o cod {row['COD']}: {e}")

    print("Dados importados com sucesso!")
