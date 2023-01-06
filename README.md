# Projet web

Web project of 2022-2023 in master AMI2B. The purpose is to build a web application with django to allow users to create and view annotations of bacterial genome.

## Environnement

We used for this project [python 3.9.12](https://www.python.org/downloads/release/python-3912/). The list of external modules, including [django 4.1.4](https://www.djangoproject.com), is available in [the requirements file](requirements.txt). To install them directly, just run : 
```
pip install -r "requirements.txt"
```
## Import data

You must put the data folder at the root of the project (where you find doc and source). Then, just run those two commands :
```
python source/manage.py migrate
python source/manage.py import_my_data
```
Note that it is also possible to compress the data using the functions in [utils.py](source/bacterial_genome_annotation/utils.py) to gain around 10 Mo.

## Classes

Here is the UML class diagram, obtained directly from [django-extensions](https://django-extensions.readthedocs.io/en/latest/graph_models.html?highlight=graph).

![diagram image](doc/uml/diagram.png "UML Class Diagram")

To recreate it, just run the two commands bellow:

```
python source/manage.py graph_models -g --dot -o doc/uml/diagram.dot bacterial_genome_annotation

dot -Tpng doc/uml/diagram.dot -o doc/uml/diagram.png
```