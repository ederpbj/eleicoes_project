# eleicoes_project
 
# 1.1 Criar ambiente virtual
python3 -m venv .venv # criar
source .venv/bin/activate # ativar

# 1.2 Instalar pacotes 
pip install django whitenoise gunicorn django-bootstrap4 PyMySQL django-stdimage

# 2 instalar pacotes

pip install psycopg2-binary # instalar pacote
pip install --upgrade pip # atualizar pip
pip install dj_database_url 
pip install python-dotenv
pip install django-imagekit
pip install psycopg2
pip install psycopg
pip install django-crispy-forms
pip install django-bootstrap4
pip install pandas openpyxl

# 3.1 Criar projeto
django-admin startproject eleicoes .

# 3.2 Criar aplicação
django-admin startapp core

pip freeze > requirements.txt

# 3.3 importar dados
python manage.py shell

from core.import_data import importar_dados
importar_dados()

# 4.1 Instalando Postgres
brew install postgresql
brew services list # lista os serviços ativos
brew services start postgresql@14 # iniciar pg
postgres --version

psql -U postgres # iniciar com usuario
brew services stop postgresql@14 # parar pg
brew services list # listar

postgres --single -D /usr/local/var/postgresql@14 postgres # modo usuario unico
CREATE ROLE postgres WITH SUPERUSER LOGIN PASSWORD 'sua_senha_aqui';
\q # ou control + D

brew services start postgresql@14 # reiniciar o servidor
psql -U postgres # testar

# 4.2 logar e criar db no pgadmin

# 5. Criar Views
# core/views

# 6. Criar templates
# index, contato e produto

# 7. Criar pasta statics
# pastas static: css, images, js

# 8. Definindo rotas urls
# django2/urls
    # path("/", include('core.urls')),
# criar core/urls.py
    # referenciar todas as views

# 9. Migrando para db    
python manage.py makemigrations core
python manage.py makemigrations # para atualizar o migrate
python manage.py migrate

@permission_required # apenas usuários com permissões apropriadas possam acessar determinadas funcionalidades
python manage.py create_groups # criar grupos de usuários
python manage.py shell # remove permissões duplicadas manualmente

# 10. Criar super usuário
python manage.py createsuperuser

# 11. Coletar arquivos estaticos
python manage.py collectstatic

python manage.py check # verificacões
python manage.py runserver # rodar para testar

# 12. Criar form
# criar core/forms.py
# usar o shell, para ver as funções do form
python manage.py shell
from django import forms
dir(forms) # mostra as funções disponíveis
dir(forms.Form) # mostra as funções disponíveis
help(forms.Form.is_valid) # mostra as funções disponíveis

help(forms.CharField) # mostra atributos 

# atualizar core/views com o form

# 13. usando bootstrap no contato.html
# 14. Criar core/forms.py
# 15 executar migration
python manage.py makemigrations
python manage.py migrate


# 16. Registrar o core/admin

# criar super usuário
python manage.py createsuperuser

# pacote para imagens
#pip install django-pictures # nao funcionou
pip install django-imagekit
pip list # lista pacotes instalados

# 17. publicando no heroku
pip install dj_database_url psycopg2-binary

pip freeze > requirements.txt

# 18. criar arquivos Procfile e runtime.txt, para heroko rodar

# 19. migrar db para heroku
heroku --help
heroku update # atualiza
heroku login 
heroku addons:plans heroku-postgresql # verifica a disponibilidade planos postgres
heroku addons:create heroku-postgresql:essential-0 --app django2-zu # instalar postgress no heroku
heroku addons:info postgresql-cubed-18354 # information
heroku addons:docs heroku-postgresql # document

# migrando db para heroku
heroku run python manage.py migrate --app django2-zu

# 20. Instalar postgresql no heroku
pip install dj-database-url
heroku addons:create heroku-postgresql --app django2-zu
heroku logs --tail --app django2-zu # verifica erros no heroku
heroku run python manage.py migrate --app django2-zu # migra db
heroku run python manage.py collectstatic --app django2-zu # arquivos estaticos
heroku config --app django2-zu # configuracao de ambiente
web: gunicorn django2.wsgi --log-file - # procfile
heroku run python manage.py dbshell --app django2-zu # verifica logs
heroku ps:scale web=1 --app django2-zu # redeploy usando dino
# coletar arquivos estaticos
heroku run python manage.py collectstatic --app django2-zu
heroku run python manage.py migrate --app django2-zu
heroku config:set SECRET_KEY='django-insecure-(p&4zusfz&p!a-)lw$tmzml(rvez7q&o#pjv0_m*_wl^j=yrve'
heroku ps --app django2-zu
heroku logs --tail --app django2-zu # erros no log
heroku config:set DEBUG=True --app django2-zu # ativar depuração em produção temporariamente
heroku run python manage.py showmigrations --app django2-zu # verificar as migrações

# ajuste do gitignore e aplicação do migrate
heroku run python manage.py makemigrations core --app django2-zu # migracoes do core
heroku run python manage.py migrate --app django2-zu # migrar
heroku run python manage.py migrate core --app django2-zu # aplicar
heroku run python manage.py showmigrations --app django2-zu # verificar
heroku pg:psql --app django2-zu # verificar db diretamente
\d # sair
heroku config:set DEBUG=False --app django2-zu
heroku run python manage.py createsuperuser --app django2-zu # criar superusuario

# Cloudinary no Heroku, outra alternativa para hospedar midia 

# 21. Tratar imagens no heroku
pip install dj-static
pip install -r requirements.txt # ver se não falta nada
pip uninstall whitenoise # remover
pip freeze > requirements.txt

heroku pg:reset DATABASE_URL --app django2-zu --confirm django2-zu # reseta o banco de dados
heroku run python manage.py migrate --app django2-zu # migrar
heroku run python manage.py createsuperuser --app django2-zu # criar superusuario
heroku logs --tail --app django2-zu # verificar erros

heroku run python manage.py collectstatic --app django2-zu # coletar estaticos

# migration do core
heroku run python manage.py makemigrations core --app django2-zu # migrar
heroku run python manage.py migrate core --app django2-zu # aplicar
heroku run python manage.py showmigrations core --app django2-zu # verificar
heroku run python manage.py collectstatic --app django2-zu # arquivos estaticos
heroku logs --tail --app django2-zu # verificar erros

# Ajustes
python manage.py flush # apaga todos os dados de todas as tabelas do banco 

psql -U postgres
DROP DATABASE docsreguladoresdb # deletar o banco

# deletar arquivos de migração
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete

# remove arquivos corrompidos
find . -name "*.pyc" -exec rm -f {} \;
find . -name "__pycache__" -exec rm -rf {} \;


# Erros
python manage.py shell

from core.models import LocalVotacao

# Atualizar todos os registros que têm `data_instalacao` igual a None para um valor padrão, como a data atual
LocalVotacao.objects.filter(data_instalacao__isnull=True).update(data_instalacao=None)

python manage.py makemigrations core
python manage.py migrate

# limpar o banco
python manage.py shell 

from django.apps import apps

# Iterar por todas as tabelas do projeto e excluir todos os registros
for model in apps.get_models():
    model.objects.all().delete()

# importar do excel
python core/import_data.py

# executar na rede local
python manage.py runserver 0.0.0.0:8000
python manage.py runserver 192.168.0.15:8000


