#!/usr/bin/env/python3
"""
Usage:
    dojo create_room (Living|Office) <room_name>...
    dojo add_person <first_name> <last_name> (Fellow|Staff) [<wants_space>]
    dojo reallocate_person <employee_id> <new_room_name>
    dojo load_people <filename>
    dojo print_allocations [--o=filename.txt]
    dojo print_unallocated [--o=filename.txt]
    dojo print_room <room_name>
    dojo save_state [--db=sqlite_database]
    dojo load_state <sqlite_database>
    dojo (-i | --interactive)

Options:
    -h --help     Show this screen.
    -i --interactive  Interactive Mode
    -v --version
"""

import cmd
import os
import sys

from docopt import docopt
from docopt import DocoptExit
import random
from rooms import Office, Living
from people import Staff, Fellow
from database import Database

from models import my_dojo

my_database = Database(my_dojo)
spacer=" "


def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """

    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print('Invalid Command!')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


def intro():
    """ the content of the user's current terminal."""
    print("WELCOME TO THE DOJO ROOM SPACE ALLOCATOR")
    print('-'*100)
    print(spacer)
    print('-'*100)
    print(spacer)
    print("For Help --- Type- help and to quit program type quit")
    print(spacer)
    print('-'*100)
    print(spacer)
    print("1    create_room (Living|Office) <room_name>...")
    print("2    add_person <first_name> <last_name> (Fellow|Staff) [<wants_space>]")
    print("3    reallocate_person <employee_id> <new_room_name>")
    print("4    load_people <filename>")
    print("5    print_allocations [--o=filename.txt]")
    print("6    print_unallocated [--o=filename.txt]")
    print("7    save_state [--db=sqlite_database]")
    print("8    load_state <sqlite_database>")
    print("9    print_room <room_name>")
    pass
    """Print introductory message to users screen."""
    
    
    
    


class Interactive(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)

        self.rooms = []
        self.vacant_rooms = []
        self.offices = []
        self.vacant_offices = []
        self.livingspaces = []
        self.vacant_livingspaces = []
        self.people = []
        self.allocated_people = []
        self.unallocated_people = []
        self.fellows = []
        self.allocated_fellows = []
        self.staff = []
        self.allocated_staff = []
        self.prompt = 'DOJO>> '
    @docopt_cmd   
    def do_create_room(self, args):
        """Usage: create_room (Living|Office) <room_name>..."""
        print( spacer)
        new_rooms = []
        for room in args["<room_name>"]:
            if room.lower() in [r.name.lower() for r in self.rooms]:
                print ("One or more rooms you tried to create already exist! " \
                          "Please try again.")
                print (spacer)
                return
            if args["Office"]:
                new_room = Office(room)
                self.offices.append(new_room)
            elif args["Living"]:
                new_room = Living(room)
                self.livingspaces.append(new_room)
            self.check_vacant_rooms()
            self.rooms.append(new_room)
            new_rooms.append(new_room)
        print ("You have successfully added the following rooom(s):")
        for new_room_ in new_rooms:
            print( "Name: " + ''.join(new_room_.name) + " | Type: " \
                      + new_room_.room_type)
        print (spacer)   
        
    def check_vacant_rooms(self):
        """Usage:
        add_person <first_name> <last_name> (Fellow|Staff) [<wants_space>]"""
        for office in self.offices:
            if len(office.occupants) < office.capacity:
                if office not in self.vacant_offices:
                    self.vacant_offices.append(office)
                    self.vacant_rooms.append(office)
            elif len(office.occupants) >= office.capacity:
                if office in self.vacant_offices:
                    self.vacant_offices.remove(office)
                    self.vacant_rooms.remove(office)
        for livingspace in self.livingspaces:
            if len(livingspace.occupants) < livingspace.capacity:
                if livingspace not in self.vacant_livingspaces:
                    self.vacant_livingspaces.append(livingspace)
                    self.vacant_rooms.append(livingspace)
            elif len(livingspace.occupants) >= livingspace.capacity:
                if livingspace in self.vacant_livingspaces:
                    self.vacant_livingspaces.remove(livingspace)
                    self.vacant_rooms.remove(livingspace)  
                    
                    
    @docopt_cmd 
    def do_add_person(self, args):
        """Add new person"""
        print (spacer)
        name = args["<first_name>"] + " " + args["<last_name>"]
        wants_space = "Yes" if args.get("<wants_space>") is "Y" else "No"
        if wants_space == "No":
            if args["Staff"]:
                new_person = Staff(name)
                self.staff.append(new_person)
            elif args["Fellow"]:
                new_person = Fellow(name)
                self.fellows.append(new_person)
        else:
            if self.offices:
                self.check_vacant_rooms()
                if not self.vacant_offices:
                    print( "There are no vacant offices at this time.")
                    print ("Please try again later.")
                    print (spacer)
                    return
                if args["Staff"]:
                    office_choice = random.choice(self.vacant_offices)
                    new_person = Staff(name)
                    office_choice.occupants.append(new_person)
                    self.staff.append(new_person)
                    self.allocated_staff.append(new_person)
                    print ("You have successfully allocated " + name + \
                              " of Employee ID " + str(new_person.emp_id) + \
                            "\nthe following office: " + office_choice.name)
                    print(spacer)
                elif args["Fellow"]:
                    office_choice = random.choice(self.vacant_offices)
                    new_person = Fellow(name)
                    office_choice.occupants.append(new_person)
                    self.fellows.append(new_person)
                    self.allocated_fellows.append(new_person)
                    print ("You have successfully allocated " + name + \
                              " of Employee ID " + str(new_person.emp_id) + \
                            "\nthe following office: " + office_choice.name)
                    print(spacer)
                self.allocated_people.append(new_person)
            else:
                print( "There are no offices in the system.")
                print ("Add one using the create_room command " \
                          "and try again.")
                print(spacer)
                return
        self.people.append(new_person)
        self.success_added_person(new_person, wants_space)  
    def success_added_person(self, new_person, wants_space):
        """Success message when person has been successfully added"""
        print ("You have successfully added the following person:")
        print ("Name: " + new_person.name + " | Employee ID: " + \
                  str(new_person.emp_id) + \
                "\nJob Type: " + new_person.job_type + \
                " | Wants Space?: " + wants_space)
        print(spacer) 
    @docopt_cmd     
    def do_reallocate_person(self, args):
        """Usage: reallocate_person <employee_id> <new_room_name>"""
        print( spacer)
        emp_id = int(args["<employee_id>"])
        new_person = None

        """Check that employee ID entered exists"""
        for p in self.people:
            if p.emp_id == emp_id:
                new_person = p
        if new_person is None:
            print ("The employee ID you have entered does not exist.")
            print ("Please try again.")
            print (spacer)
            return

        new_room_name = args["<new_room_name>"]
        for r in self.rooms:
            if r.name == new_room_name:
                new_room = r

        """Check that room entered exists and is vacant"""
        if new_room_name not in [r.name for r in self.vacant_rooms]:
            print( "The room you entered, " + new_room_name + \
                "either does not exist or is not vacant.")
            print("Please try again.")
            print( spacer)
            return

        if new_person.job_type == "Staff":
            """Prevent staff from being allocated living spaces"""
            if new_room.room_type == "Living":
                print("Staff members cannot be allocated " \
                    "living spaces.")
                print(spacer)
                return

        """Check if person has already been allocated a room"""
        for room in self.vacant_rooms:
            if new_person.emp_id in \
                    [person.emp_id for person in room.occupants]:
                if new_room == room:
                    """
                    Prevent person from being allocated the same room
                    """
                    print(new_person.name + " is already an occupant" \
                        " of the room " + new_room.name + ".")
                    print (spacer)
                    return
                else:
                    """Remove person from current office"""
                    room.occupants.remove(new_person)

        """Add person to new room"""
        new_room.occupants.append(new_person)
        self.allocated_people.append(new_person)
        if new_person.job_type == "Fellow":
            self.allocated_fellows.append(new_person)
        else:
            self.allocated_staff.append(new_person)
        print("You have successfully allocated " + new_person.name + \
            " of Employee ID " + str(new_person.emp_id) + \
            "\nthe following room: " + new_room.name)
        if new_person in self.unallocated_people:
            self.unallocated_people.remove(new_person)
        print (spacer)
    @docopt_cmd    
    def do_load_people(self, args):
        """Usage: load_people <filename>"""
        filename = args["<filename>"]
        with open(filename, 'r') as my_file:
            people = my_file.readlines()
            for p in people:
                p = p.split()
                if p:
                    first_name = p[0]
                    last_name = p[1]
                    if p[2] == "FELLOW":
                        is_staff = False
                        is_fellow = True
                    else:
                        is_staff = True
                        is_fellow = False
                    if len(p) == 4:
                        wants_space = p[3]
                    else:
                        wants_space = None

                    self.add_person({
                            "<first_name>": first_name.title(),
                            "<last_name>": last_name.title(),
                            "<wants_space>": wants_space,
                            "Fellow": is_fellow,
                            "Staff": is_staff
                        })
                    
    @docopt_cmd                
    def doprint_unallocated(self, args):
        """Usage: print_unallocated [--o=filename.txt]"""
        print(spacer)
        output = ""
        output += "Unallocated People\n"
        output += "-" * 50 + "\n"
        for p in self.people:
            if p not in self.allocated_people:
                output += p.name + "\n"
                if p not in self.unallocated_people:
                    self.unallocated_people.append(p)
        if not self.people:
            output += "There are no people in the system.\n"
            output += "Add a person using the add_person command" \
                " and try again.\n"
        elif not self.unallocated_people:
            output += "There are no unallocated people in the system.\n"
        print(output)
        if args["--o"]:
            with open(args["--o"], 'wt') as f:
                f.write(output)
                print("The list of unallocated people has been saved " \
                    "to the following file: ")
                print(args["--o"])
                print(spacer)    
                
    @docopt_cmd            
    def print_allocations(self, args):
        """Usage: print_allocations [--o=filename.txt]"""
        print(spacer)
        output = ""
        for r in self.rooms:
            output += r.name + "\n"
            output += "-" * 50 + "\n"
            if r.occupants:
                output += ", ".join(p.name for p in r.occupants) + "\n"
                output += spacer + "\n"
            else:
                output += "This room has no occupants.\n"
                output += spacer + "\n"
        if not self.rooms:
            output += "There are no rooms in the system.\n"
            output += "Add a room using the create_room command" \
                " and try again.\n"
        print(output)
        if args["--o"]:
            with open(args["--o"], 'wt') as f:
                f.write(output)
                print("The list of allocations has been saved " \
                    "to the following file: ")
                print(args["--o"])
                print(spacer) 
                
    @docopt_cmd            
    def print_room(self, args):
        """Usage: print_room <room_name>"""
        print(spacer)
        room_name = args["<room_name>"]
        if room_name not in [r.name for r in self.rooms]:
            print("The room you have entered does not exist.")
            print("Please try again.")
            print(spacer)
            return
        for r in self.rooms:
            if r.name == room_name:
                room = r
                print(room.name)
                print("-" * 50)
                if room.occupants:
                    for p in room.occupants:
                        print(p.name)
                else:
                    print("This room has no occupants.")
                print(spacer)    
                
    @docopt_cmd
    def do_save_state(self, args):
        """Usage: save_state [--db=sqlite_database]"""
        my_database.save_state(args)
     
    @docopt_cmd
    def do_load_state(self, args):
        """Usage: load_state <sqlite_database>"""

        my_database.load_state(args)        
       
        
    
    
    def do_quit(self, arg):
        """Quits out of the interactive mode"""
        print(spacer)
        print("Goodbye!")
        print(spacer)
        exit()

opt = docopt(__doc__, sys.argv[1:])
                

    
if __name__ == "__main__":
    try:
        opt = docopt(__doc__, sys.argv[1:])

        if opt['--interactive'] or opt['-i']:
            
            intro()
            Interactive().cmdloop()

        print(opt)
    except KeyboardInterrupt:
        
        print('Application Exiting')






