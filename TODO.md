# TODO

## To be done

- [ ] HTML structure
    - [ ] Pages schemes
        - [X] Annot
        - [ ] Parser
        - [X] Add
        - [X] Login
        - [X] Account
        - [X] Search 
    - [ ] Link between pages
        - [X] Annot
        - [ ] Parser
        - [X] Add
        - [X] Login
        - [X] Account
        - [X] Search
    - [ ] Forum page
    - [ ] Annotation comment

- [ ] Front
    - [ ] Banner or floating menu or sidebar
    - [X] Create a sign up page
    - [ ] Visualizing a particular pattern in a sequence
    - [ ] Bootstrap 5
    - [ ] front page: put a side-bar with a menu to access every feature
    - [ ] front page: separate into 4 different zones, each one explaining one feature (annotate, add, parse, search)
    - [ ] search genome: displays the genomes found and brightens the searched pattern
    - [ ] annotate: the annotator can search in a bank of unannotated sequences which one he wants to sequence.

- [ ] Database
    - [X] UML diagram
    - [X] Migrations
    - [X] Import data
    - [X] Authentification
    - [X] Pattern search
    - [ ] Comments
    - [ ] Scroll
- [ ] Other
    - [ ] Use blast API


## Report

- [ ] Justify why there can be multiple annotations for one sequence

## Optional features

- [ ] Chat(gpt) help

### Front

- [ ] Multi theme

### Database optimization

- [ ] Use `update_conflicts = True` in bulk_create. Only works with Django > 4.1
- [X] Compress the sequences : 10 Mo can be free if we use the compression in [utils.py](source/bacterial_genome_annotation/utils.py)
- [X] Default group Reader
- [ ] Make a command to create a bunch of example users and new annotations
- [ ] Pattern search optimization
    - [ ] Use Burrows-Wheeler Transform : from scratch or via [this repos](https://github.com/Axl-Lvy/Index-structure-and-mapping)
    - [X] Complex pattern search (for exemple with regular expressions)
    - [ ] Autocompletion
- [ ] Color the searched pattern

