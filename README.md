# projet_web
web project of 2022-2023 in master AMI2B

## Diagramme UML

Pour obtenir le diagramme UML, lancer ces deux lignes de commande :

```
python manage.py graph_models -a -g --dot -o uml_diagram.dot
dot -Tpng uml_diagram.dot -o uml_diagram.png
```