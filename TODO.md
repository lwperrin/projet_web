# TODO

## To be done

- [X] HTML structure
    - [X] Pages schemes
        - [X] Annot
        - [X] Parser
        - [X] Add
        - [X] Login
        - [X] Account
        - [X] Search
            - [X] Blast
                - [X] Alignement
            - [X] Annotation  
        - [X] AboutUs
        - [X] contact
    - [X] Link between pages
        - [X] Annot
        - [X] Parser
        - [X] Add
        - [X] Login
        - [X] Account
        - [X] Search
            - [X] Blast
                - [X] Alignement
            - [X] Annotation  
        - [X] AboutUs
        - [X] contact
    - [ ] Forum page
    - [X] Annotation comment
        - [ ] display
    - [ ] Account page (different depending on the user group)
    - [X] Search in home

- [ ] Front
    - [X] Banner or floating menu or sidebar
    - [X] Create a sign up page
    - [X] Color
    - [X] Visualization of query Search 
    - [X] Visualization Sequence of Query
    - [X] Visualizing a particular pattern in a sequence
    - [X] Bootstrap 4
    - [X] front page: put a side-bar with a menu to access every feature
    - [X] front page: home/search
    - [X] search genome: displays the genomes found and brightens the searched pattern
    - [X] annotate: the annotator can search in a bank of unannotated sequences which one he wants to sequence.
    - [X] Help page

- [ ] Database
    - [X] UML diagram
    - [X] Migrations
    - [X] Import data
    - [X] Authentification
    - [X] Pattern search
    - [ ] Comments
    - [ ] Scroll
    - [ ] Django-RQ to build tasks queues
    - [X] Regex to contains then regex
    - [ ] Search by validate

- [ ] Other
    - [X] Use blast API
    - [X] Blast visualization


## Report

- [X] Justify why there can be multiple annotations for one sequence

## Optional features

- [ ] Chat help
- [X] FAQ

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
- [X] launch blast in background
- [X] Validate email and password in live (ajax)
- [ ] fix assignation of the annotations

## CheckList Error

- [ ] Permissions for Add genome Page (acces same no sign in)
- [ ] Copy of Annotations identic in Sequence Page
- [ ] Annotate link in Nav Bar it's incorect (connect with annotate account/link with sequence page it's okay)
- [ ] Assign a sequence for members (not visible ( no favorites) however i add members ( annotator) in favorities list).
- [ ] valid/delete Button for the new annotations visible (all users).
- [ ] 

## Verify Points

- [ ] IGV visualization (Annotation)
- [ ] 
