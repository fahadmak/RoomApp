import sys
import os
import sqlite3
from contextlib import closing

from objects import Category
from objects import Person

conn = None

def connect():
    global conn
    if not conn:
        if sys.platform == "win32":
            DB_FILE = "/Dojo/_db/dojo.sqlite"
        else:
            HOME = os.environ["HOME"]
            DB_FILE = HOME + "/_db/dojo.sqlite"
        
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row

def close():
    if conn:
        conn.close()

def make_category(row):
    return Category(row["categoryID"], row["categoryName"])

def make_person(row):
    return Person(row["personID"], row["name"], row["year"], row["minutes"],
            make_category(row))

def get_categories():
    query = '''SELECT categoryID, name as categoryName
               FROM Category'''
    with closing(conn.cursor()) as c:
        c.execute(query)
        results = c.fetchall()

    categories = []
    for row in results:
        categories.append(make_category(row))
    return categories

def get_category(category_id):
    query = '''SELECT categoryID, name AS categoryName
               FROM Category WHERE categoryID = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (category_id,))
        row = c.fetchone()
        if row:
            return make_category(row)
        else:
            return None

def get_people_by_category(category_id):
    query = '''SELECT personID, Person.name, year, minutes,
                      Person.categoryID as categoryID,
                      Category.name as categoryName
               FROM Person JOIN Category
                      ON Person.categoryID = Category.categoryID
               WHERE Person.categoryID = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (category_id,))
        results = c.fetchall()

    people = []
    for row in results:
        people.append(make_person(row))
    return people

def get_people_by_year(year):
    query = '''SELECT personID, Person.name, year, minutes,
                      Person.categoryID as categoryID,
                      Category.name as categoryName
               FROM Person JOIN Category
                      ON Person.categoryID = Category.categoryID
               WHERE year = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (year,))
        results = c.fetchall()

    people = []
    for row in results:
        people.append(make_person(row))
    return people

def add_person(person):
    sql = '''INSERT INTO Person (categoryID, name, year, minutes) 
             VALUES (?, ?, ?, ?)'''
    with closing(conn.cursor()) as c:
        c.execute(sql, (person.category.id, person.name, person.year,
                        person.minutes))
        conn.commit()

def delete_person(person_id):
    sql = '''DELETE FROM Person WHERE personID = ?'''
    with closing(conn.cursor()) as c:
        c.execute(sql, (person_id,))
        test = conn.commit()
        print("Test", test)
