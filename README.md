# Avanzómetro

# Para instalar por primera vez:

-Clonar el repositorio

-Instalar Django en Python3: 

    pip3 install django
    
-Instalar psycopg2 en Python3 para conectar con la Base de Datos de PostgreSQL:

    pip3 install psycopg2
    
-Crear Base de Datos "avanzometro" con dueño "avanzometro" en PostgreSQL:

    -Entrar en psql con usuario postgres:
        psql -U postgres
    
        -Crear usuario "avanzometro":
            CREATE USER avanzometro;
        -Crear base de datos "avanzometro":
            CREATE DATABASE avanzometro;
        -Asignar usuario "avanzometro" a base de datos "avanzometro":
            ALTER DATABASE avanzometro OWNER TO avanzometro;
       
-Hacer migraciones de la aplicación:

    -Entrar en la carpeta de la aplicación y hacer migraciones:
        python3 manage.py makemigrations
    
    -Migrar las tablas:
        python3 manage.py migrate
        
-Correr el Servidor:

    python3 manage.py runserver
    
    
# Para actualizar versión:

-Clonar o hacer "pull" del repositorio
    
-Borrar y volver a crear Base de Datos "avanzometro" con dueño "avanzometro" en PostgreSQL:

    -Entrar en psql con usuario postgres:
        psql -U postgres
    
        -Borrar base de datos "avanzometro":
            DROP DATABASE avanzometro;
        -Crear base de datos "avanzometro":
            CREATE DATABASE avanzometro;
        -Asignar usuario "avanzometro" a base de datos "avanzometro":
            ALTER DATABASE avanzometro OWNER TO avanzometro;
       
-Hacer migraciones de la aplicación:
    
    -Entrar en la carpeta grafico/migrations de la aplicacion:
        Borrar todos los archivos, excepto "__init__.py"
    
    -Entrar en la carpeta de la aplicación y hacer migraciones:
        python3 manage.py makemigrations
    
    -Migrar las tablas:
        python3 manage.py migrate
        
-Correr el Servidor:

    python3 manage.py runserver
