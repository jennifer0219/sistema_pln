# Sistema PLN con Django

#Requisitos Previos 
-Tener Python 3.10 o superior 
-Tener Git instalado (para poder clonar el repositorio)
-Tener Pipenv instalado

En Terminal (cmd)
1. Clonar repositorio:
git clone https://github.com/jennifer0219/sistema_pln.git

2. Entrar al proyecto:
cd sistema_pln

3. Crear entorno virtual:
pipenv install
pipenv shell

4. Migrar base de datos:
python manage.py migrate

5. Crear superusuario:
python manage.py createsuperuser
Sigue las preguntas (usuario, email y contraseña).

6. Ejecutar servidor:
python manage.py runserver

Ingresa el link proporcionado en un navegador (ejemplo: http://127.0.0.1:8000/)

## Funcionalidades
- Subida de archivos `.txt`
- Lista de textos subidos
- Generación de histograma de palabras en tabla
- Visualización del archivo
- Administración desde panel Django
