# RoomApp


A system to allocate offices and living spaces to staff and Fellows at the Andela Kenya Dojo.

### Features
        
        - Create Rooms
        - Add People
        - Allocate persons to rooms
        - Reallocate person
        - Save session to database
        - Load session from database
        - Check occupants of a room
        - Printing room allocations to a file

### Why the project is useful
    This project helps to eradicate the current paper system used by most hostels in room allocation.

### How to setup the project/Installation/Configuration

* Go to Github, look for repository called the Room System using Python from fahadmak github account

* Clone the repo
```git clone or download from https://github.com/fahadmak/RoomApp.git``` and navigate to the project directory

* Install dependencies
```pip install -r requirements.txt```

* Run the program 
```python ui.py ``` shows a list of available commands
```python ui.py -i ``` takes you into an interactive loop
```python ui.py -h ``` displays the help section of the app
    
### Usage:
```
    create_room <room_type> <room_name>...
    add_person <person_fname> <person_lname> <FELLOW/STAFF> [<wants_accommodation>]
    print_allocations [--o=filename]
    print_unallocated [--o=filename]
    get_person_id <person_fname> <person_lname>
    print_room <room_name>
    reallocate_person <person_identifier> <room_name>
    load_people <file_name>
    save_state [--db=sqlite_database]
    load_state <sqlite_database>
    purge
    quit
```



