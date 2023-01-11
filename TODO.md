# TODO

## To be done

- [ ] HTML structure
    - [ ] Pages schemes
    - [ ] Link between pages

- [ ] Front
    - [ ] Banner or floating menu
    - [X] Create a sign up page
    - [ ] Visualizing a particular pattern in a sequence

- [ ] Database
    - [X] UML diagram
    - [X] Migrations
    - [X] Import data
    - [X] Authentification
    - [X] Pattern search
    - [ ] Forum

## Optional features

### Database optimization

- [ ] Use `update_conflicts = True` in bulk_create. Only works with Django > 4.1
- [X] Compress the sequences : 10 Mo can be free if we use the compression in [utils.py](source/bacterial_genome_annotation/utils.py)
- [X] Default group Reader
- [ ] Make a command to create a bunch of example users and new annotations
- [ ] Pattern search optimization
    - [ ] Use Burrows-Wheeler Transform : from scratch or via [this repos](https://github.com/Axl-Lvy/Index-structure-and-mapping)
    - [X] Complex pattern search (for exemple with regular expressions)
    - [ ] Autocompletion

