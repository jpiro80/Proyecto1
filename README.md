<!-- HEADINGS -->

# Cuadros y tablas
## Requisitos:
* Python 3.9
* Github
* Visual Studio Code
* DB Browser for Sqlite
### El trabajo que estoy realizando consiste en fabricar cuadros en Python (.py)
![Cuadro 01](Cuadro01.png)

### A estos cuadros estoy intentando insertarles tablas creadas con DB Browser Sqlite (.db)
![Cuadro 02](Cuadro02.png)
### Como puede verse, las tablas son simples. Con filas y columnas que contienen diferentes tipos de variables. En este caso, estoy probando cuadros organizativos de pagos de impuestos del mes y sus respectivos importes. De no más de dos columnas, en principio. Para ello, estoy siguiendo un tutorial, dentro del cual, la línea 57 indica el comando con el que la tabla debería insertarse en el cuadro
![Cuadro 03](Cuadro03.png)

![Cuadro 04](Cuadro04.png)

### El problema que surge, es que en el tutorial al parecer utilizan Linux y otro programa para ejecutar archivos .py, por lo cual al hacer la ejecución con el Python 3.9 en Windows, el resultado que obtengo es el siguiente:
![Cuadro 05](Cuadro05.png)
### La tabla no se inserta en el cuadro y me marca esos errores.

### El archivo principal es index.py y el archivo a de base de datos a insertar es database.db Ambos se encuentran en el repositorio.