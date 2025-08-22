# Sistema PLN con Django

## Instalación

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

6. Ejecutar servidor:
python manage.py runserver


## Funcionalidades
- Subida de archivos `.txt`
- Lista de textos subidos
- Generación de histograma de palabras en tabla
- Visualización del archivo
- Administración desde panel Django
