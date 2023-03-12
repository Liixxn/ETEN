<h1 align="center"><b>🍝ETEN🍹</b></h1>
<h2 align="center"><i>ETEN para tu sartén🍳</i></h2>


<p>ETEN es una aplicación de escritorio enfocada en la clasificación de recetas de texto en diversas categorías. Haciendo uso de inteligencia artificial, se 
entrena y se testea un modelo que es el encargado de la clasificación. Además, la aplicación puede obtener los ingredientes de una receta.</p>

<p>ETEN cuenta con unas 7 categorías con las que trabaja, sin embargo se ofrece la posibilidad de añadir las categorías que se quieran.<p>

<ul>
  <li>Arroz y Pasta🍚🍝</li>
  <li>Bebidas☕</li>
  <li>Carnes🍖</li>
  <li>Vegetales🥬</li>
  <li>Dulces🎂</li>
  <li>Pescados🐟</li>
  <li>Variados🍳</li>
</ul>



<p>ETEN es un proyecto desarrollado para la asignatura de "Proyecto de Computación I" de la carrera de Ingeniería Informática de 3º año. Creada en python y diseñada 
con PyQT5, ofrece una interfaz agradable y familiar al usuario, que informa en todo momento del estado de sus procesos.</p>

<div align="center">
  <img src="https://github.com/Liixxn/ETEN/blob/main/ETEN_png.png" width=150 height=150>
</div>
<hr>

<h3>Lenguajes y herramientas usadas</h3>
<a href="https://www.python.org" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> </a>
<a href="https://pandas.pydata.org/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/2ae2a900d2f041da66e950e4d48052658d850630/icons/pandas/pandas-original.svg" alt="pandas" width="40" height="40"/></a>
<a href="https://scikit-learn.org/" target="_blank" rel="noreferrer"><a href="https://scikit-learn.org/" target="_blank" rel="noreferrer"> <img src="https://upload.wikimedia.org/wikipedia/commons/0/05/Scikit_learn_logo_small.svg" alt="scikit_learn" width="40" height="40"/> </a>
<a href="https://numpy.org" target="_blank" rel="noreferrer"><img src="https://upload.wikimedia.org/wikipedia/commons/3/31/NumPy_logo_2020.svg" alt="Numpy" width="40" height="40"/> </a>
<a href="https://riverbankcomputing.com/software/pyqt/intro" target="_blank" rel="noreferrer"><img src="https://upload.wikimedia.org/wikipedia/commons/e/e6/Python_and_Qt.svg" alt="PyQt" width="40" height="40"/> </a>
<a href="https://jupyter.org" target="_blank" rel="noreferrer"><img src="https://upload.wikimedia.org/wikipedia/commons/3/38/Jupyter_logo.svg" alt="Jupyter Notebook" width="40" height="40"/> </a>
<a href="https://www.jetbrains.com/es-es/pycharm/" target="_blank" rel="noreferrer"><img src="https://upload.wikimedia.org/wikipedia/commons/1/1d/PyCharm_Icon.svg" alt="PyCharm" width="40" height="40"/> </a>

<hr>

<h3>Instalación</h3>

<p>ETEN hace uso de difernetes librerías para su correcto funcionamiento, por lo que debe tener instalado 'pip' para descargar todos los componentes. Si no tiene pip
puede instalárselo con el siguiente comando en una terminal.</p>

```
pyhton get-pip.py
```

<p>A continuación, navege desde la terminal hasta la ruta en la que se encuentre el proyecto descomprimido. Uno de los ficheros que se encuentran denominado, 
<i>requirements.txt</i> contiene todas las librerías que ETEN necesita. Instálelas con el siguiente comando:</p>

```
pip install -r requirements.txt
```

<p>Tras la finalización de las diversas instalaciones, solo tiene que ejecutar el fichero principal <b>ETEN.py</b> y ya podrá disfrutar de todas las 
funcionalidades que ofrece la aplicación.</p>

<hr>

<h3>Ficheros de interés</h3>
<p>Se van a explicar de una forma breve, los diferentes ficheros, carpetas etc. que conforman el proyecto, para un mayor entendimiento del funcionamiento y desarrollo
de ETEN.</p>


<h4 align="center">📑Ficheros📑</h4>

<ul>
  <li><b><i>ETEN.py</i></b>: el fichero principal de la aplicación, dónde se inicializan todas las ventanas y gestiona las diferentes funcionalidades.</li>
  <li><b><i>[nombre].ui</i></b>: archivos que representan los diseños para la interfaz de ETEN, estos ficheros son generados por la aplicación de diseño QT Designer.</li>
  <li><b><i>resource.qrc</i></b>: fichero generado por la aplicación de diseño QT Designer, que guarda las imágenes o iconos utilizados en el diseño.</li>
  <li><b><i>index.qss</i></b>: archivo igual a una hoja de estilos, pero para elementos PYQT.</li>
  <li><b><i>descargarVideos.py, word_Segmentation.py y check_lenght_audio.py</i></b>: fichero que gestione la descarga de vídeos o listas de reproducción, 
  además de transformar el vídeo a audio y pasar su contenido a texto.</li>
  <li><b><i>pln.py</i></b>: archivo que comprueba las categorías añadidas para el entrenamiento del modelo.</li>
  <li><b><i>text_processing.py</i></b>: fichero dónde se realizan todo el procesamiento de lenguaje natural sobre los textos de las recetas, además de entrenar
  y testear los diferentes modelos.</li>
  <li><b><i>pandas_table.py</i></b>: fichero que hace posible la visualización de los datos en un formato tabla.</li>
</ul>

<h4 align="center">🗂Carpetas🗂</h4>

<ul>
  <li><b><i>unlabeled</i></b>: carpeta que guarda las recetas utilizadas para la fase de test, que el modelo debe clasificar.</li>
  <li>icons<b><i></i></b>: carpetas que guardan los iconos que usa la aplicación.</li>
  <li><b><i>ingredientes</i></b>: carpeta dónde se encuentra un fichero de texto, que almacena diferentes ingredientes. Éste fichero se utiliza para obtenr los
  ingredientes de las recetas.</li>
  <li><b><i>stopwords</i></b>: carpeta que almacena el fichero de palabras vacías, usado para el proceso de lenguaje natural.</li>
  <li><b><i>recetas</i></b>: en esta carpeta se van a encontrar diferentes carpetas y ficheros:
    <ul>
      <li>transcripciones: guarda todas las recetas dividias en sus diferentes categorías para el entrenamiento del modelo.</li>
      <li>[nombre].mp4: dentro de esta carpeta se almacenan las diferentes recetas que se descarguen.</li>
    </ul>
  </li>
</ul>

<hr>

<h3 align="center">Ventana Principal de ETEN</h3>
<div align="center">
  <img src="https://github.com/Liixxn/ETEN/blob/main/imgs/VentanaPrincipal.png" alt="Ventana Principal de ETEN" width="60%" height="60%">
</div>
