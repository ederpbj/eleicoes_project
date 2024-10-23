import os
import django

# Configurar o DJANGO_SETTINGS_MODULE para apontar para o arquivo de configurações do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eleicoes.settings')

# Inicializar o Django
django.setup()

from core.models import LocalVotacao

def atualizar_status_urnas():
    try:
        # Atualiza os registros onde o status das urnas é 'Desmobilizado' para 'Instalada'
        registros_atualizados = LocalVotacao.objects.filter(status_urnas='Desmobilizado').update(status_urnas='Instalada')

        # Imprime a quantidade de registros que foram atualizados
        print(f"{registros_atualizados} registros atualizados com sucesso.")

    except Exception as e:
        print(f"Erro ao atualizar os registros: {e}")

if __name__ == "__main__":
    atualizar_status_urnas()
