# Eleicoes

```Python
# 0. gitignore
git rm -r --cached .
git add .
git commit -m "Remover arquivos do controle de versão e atualizar .gitignore"
git push origin master

# 1. Instalar pacotes 
pip install django whitenoise gunicorn django-bootstrap4 PyMySQL django-stdimage

pip freeze > requirements.txt

# 2. Criar projeto
django-admin startproject djangoDocsRegulador .

# 3.1 Criar aplicação
django-admin startapp core

# 3.2. Criar ambiente virtual
python3 -m venv .venv # criar
source .venv/bin/activate # ativar


# 3.3 instalar pacotes

pip install psycopg2-binary # instalar pacote
pip install --upgrade pip # atualizar pip
pip install dj_database_url 
pip install python-dotenv
pip install django-imagekit
pip install psycopg2
pip install psycopg
pip install django-crispy-forms
pip install django-bootstrap4


pip freeze > requirements.txt

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

ls -l /home/ubuntu/DocsReguladores/venv # listar

# gunicorn
sudo nano /etc/systemd/system/gunicorn.service

# colar conteudo

sudo systemctl daemon-reload
sudo systemctl restart gunicorn
sudo systemctl status gunicorn


sudo systemctl restart gunicorn
sudo systemctl restart nginx

# configurar nginx
sudo nano /etc/nginx/sites-available/docsreguladores

# excluir da raiz
sudo rm -rf /home/ubuntu/DocsReguladores/staticfiles

# screen rodar em segundo plano
screen -list
screen -S django
screen -r 28353.django # entrar na screen

# Redirecionar a porta 80 para a porta 8080
sudo /sbin/iptables -t nat -I PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8000

# rodando em
http://44.205.47.59/
http://52.54.188.232/

# atualizando com gihub
git pull origin main

# listar portas, e parar
sudo lsof -i :8000
sudo kill -9 27411 27412 27413 27414

# restartar serviços aws
source venv/bin/activate
pip freeze > requirements.txt
pip install -r requirements.txt
python manage.py makemigrations core
python manage.py migrate

rm -rf staticfiles
python manage.py collectstatic --noinput

sudo systemctl daemon-reload


sudo systemctl restart gunicorn
sudo systemctl restart nginx
sudo systemctl status gunicorn
sudo systemctl status nginx
python manage.py runserver 0.0.0.0:8000

# gihub
git pull origin main  # puxar as últimas atualizações do repositório remoto

# chave publica local
openssl req -new -key server.key -out server.csr\n


Atualizar python

# Remover o ambiente virtual antigo
deactivate  # caso esteja ativado
rm -rf venv

# Criar um novo ambiente virtual com Python 3.10 ou superior
python3.10 -m venv venv

# Ativar o ambiente virtual
source venv/bin/activate

# Instalar os pacotes novamente
pip install -r requirements.txt

# eleicoes
psql 'postgresql://postgres:NyAsxKMgCLggdwE9@wrongfully-scrupulous-gelding.data-1.use1.tembo.io:5432/postgres'
CREATE DATABASE eleicoes;



```
[docs bootstrap](https://getbootstrap.com/docs/5.3/content/tables/)
[Appliku hospedagem](https://app.appliku.com/auth/sign-up)
[Sua aplicação DJANGO NO AR](https://www.youtube.com/watch?v=ZBstiRvHX7w)

