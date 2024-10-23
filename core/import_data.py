import pandas as pd

from core.models import LocalVotacao


def importar_dados(data_instalacao=None):
    # URL de exportação do Google Sheets
    url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTMcNDckORxHEEy_VKuFU8bHsYVNh-EPtVY35Nq7FL2SlEhNulj5PVMnDTtRijsvA/pub?output=csv'

    # Carregar o CSV diretamente da URL
    try:
        df = pd.read_csv(url)
    except Exception as e:
        print(f"Erro ao carregar CSV: {e}")
        return

    expected_columns = ['Cod', 'OPMs', 'ZONA', 'MUNICÍPIO', 'NOME DO LOCAL', 'ENDEREÇO', 'BAIRRO',
                        'QTDE_SECOES', 'DATA DA INSTALAÇÃO', 'HORÁRIO', 'QTDE_ELEITORES',
                        'NÍVEL DE PRIORIDADE', 'LOCAL DE VOTAÇÃO ', ' STATUS DAS URNAS',
                        ' STATUS FISCALIZAÇÃO', 'FALTA MILITAR']

    if not all(col in df.columns for col in expected_columns):
        print("Erro: Colunas faltando no CSV.")
        return
    
    # Mostrar os nomes das colunas para verificar se estão corretos
    print("Colunas encontradas no arquivo CSV:", df.columns)

    # Iterar pelas linhas do DataFrame e criar objetos LocalVotacao
    for _, row in df.iterrows():
        # Garantir que o código é único
        if LocalVotacao.objects.filter(cod=int(row['Cod'])).exists():
            print(f"Registro com o cod {row['Cod']} já existe, pulando...")
            continue

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
            status_fiscalizacao=row[' STATUS FISCALIZAÇÃO'] if pd.notna(row[' STATUS FISCALIZAÇÃO']) else '',
            falta_militar=int(row['FALTA MILITAR']) if pd.notna(row['FALTA MILITAR']) else 0,
        )
    print("Dados importados com sucesso!")
