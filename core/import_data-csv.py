import pandas as pd
import os
import django

# Definir a variável de ambiente DJANGO_SETTINGS_MODULE antes de inicializar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eleicoes.settings')

# Inicializar o Django
django.setup()

from core.models import LocalVotacao


def importar_dados(data_instalacao=None):
    # Caminho do arquivo CSV local
    url = '/Users/user/Library/CloudStorage/GoogleDrive-ciccsesds@gmail.com/Meu Drive/CPRM/Dados_eleições_2024.2_Dj.csv'

    # Tentar carregar o CSV local
    try:
        df = pd.read_csv(url)
        print("CSV carregado com sucesso!")
        print(df.head())  # Exibe as primeiras linhas do arquivo para verificar o conteúdo
    except Exception as e:
        print(f"Erro ao carregar CSV: {e}")
        return

    # Definir as colunas esperadas
    expected_columns = ['Nº', 'CIA', 'ZONA', 'NOME DO LOCAL', 'ENDEREÇO', 'BAIRRO',
                        'SEÇÕES', 'INSTALAÇÃO', 'HORÁRIO', 'ELEITORES',
                        'PRIORIDADE', 'LOCAL DE VOTAÇÃO', 'LOCAL COM URNAS',
                        'FISCALIZAÇÃO']

    # Verificar se todas as colunas esperadas estão presentes no CSV
    if not all(col in df.columns for col in expected_columns):
        print("Erro: Colunas faltando no CSV.")
        print("Colunas encontradas:", df.columns)
        return

    # Mostrar os nomes das colunas para verificar se estão corretos
    print("Colunas encontradas no arquivo CSV:", df.columns)

    # Iterar pelas linhas do DataFrame e criar objetos LocalVotacao
    for _, row in df.iterrows():
        print(f"Processando o registro com o cod {row['Nº']}...")  # Adiciona um log para cada linha processada

        # Verificar se o registro já existe no banco
        if LocalVotacao.objects.filter(cod=int(row['Nº'])).exists():
            print(f"Registro com o cod {row['Nº']} já existe, pulando...")
            continue

        # Criar um novo objeto LocalVotacao
        try:
            LocalVotacao.objects.create(
                cod=int(row['Nº']) if pd.notna(row['Nº']) else 0,
                cia=row['CIA'] if pd.notna(row['CIA']) else '',
                zona=int(row['ZONA']) if pd.notna(row['ZONA']) else 0,
                nome_local=row['NOME DO LOCAL'] if pd.notna(row['NOME DO LOCAL']) else '',
                endereco=row['ENDEREÇO'] if pd.notna(row['ENDEREÇO']) else '',
                bairro=row['BAIRRO'] if pd.notna(row['BAIRRO']) else '',
                secoes=int(row['SEÇÕES']) if pd.notna(row['SEÇÕES']) else 0,
                data_instalacao=data_instalacao,
                horario=row['HORÁRIO'] if pd.notna(row['HORÁRIO']) else '',
                eleitores=int(row['ELEITORES']) if pd.notna(row['ELEITORES']) else 0,
                prioridade=row['PRIORIDADE'] if pd.notna(row['PRIORIDADE']) else '',
                local_votacao=row['LOCAL DE VOTAÇÃO'] if pd.notna(row['LOCAL DE VOTAÇÃO']) else '',
                local_urnas=row['LOCAL COM URNAS'] if pd.notna(row['LOCAL COM URNAS']) else '',
                fiscalizacao=row['FISCALIZAÇÃO'] if pd.notna(row['FISCALIZAÇÃO']) else '',
            )
            print(f"Registro com o cod {row['Nº']} criado com sucesso.")
        except Exception as e:
            print(f"Erro ao criar o registro com o cod {row['Nº']}: {e}")

    print("Dados importados com sucesso!")
