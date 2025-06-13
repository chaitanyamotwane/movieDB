"""
createDB.py

Copyright (c) 2025 Swarthmore College Computer Science Department
Swarthmore PA, Professors Tia Newhall, Ameet Soni

Name: Chaitanya Motwane
Date: April 9th, 2025
Description: Creates the database tables, inserts all the data into the database,
and creates indexes that are useful
"""

import sqlite3
import os
import sys

def createTables(db):
  """Creates the database schema

  Creates 6 tables according to the following schema:
        Actor (id, fname, lname, gender)
        Movie (id, title, year)
        Director (id, fname, lname)
        Cast (actorID, movieID, role)
        DirectsMovie (directorID, movieID)
        Genre (movieID, genre)
  @param db - a Cursor object for the database connection
  @return None.  The 6 tables are added to the database
  """

  #Example for executing a SQL command.  This enforces foreign key constraints
  db.execute("PRAGMA foreign_keys=ON")

  print("...Creating Tables ...")

  db.execute("""CREATE TABLE Actor (
    id INTEGER PRIMARY KEY,
    fname VARCHAR(30),
    lname VARCHAR(30),
    gender CHAR(1)
    )""")
  
  db.execute("""CREATE TABLE Movie (
    id INTEGER PRIMARY KEY,
    title VARCHAR(30),
    year INTEGER
  )""")

  db.execute("""CREATE TABLE Director (
    id INTEGER PRIMARY KEY,
    fname VARCHAR(30),
    lname VARCHAR(30)
  )""")

  db.execute("""CREATE TABLE Casts (
    actorID INTEGER,
    movieID INTEGER,
    role VARCHAR(50),
    PRIMARY KEY (actorID, movieID, role),
    FOREIGN KEY (actorID) REFERENCES Actor(id),
    FOREIGN KEY (movieID) REFERENCES Movie(id)
  )""")

  db.execute(""" CREATE TABLE DirectsMovie (
    directorID INTEGER,
    movieID INTEGER,
    PRIMARY KEY (directorID, movieID),
    FOREIGN KEY (directorID) REFERENCES Director(id)
    FOREIGN KEY (movieID) REFERENCES Movie(id)
  )""")

  db.execute(""" CREATE TABLE Genre (
    movieID INTEGER,
    type VARCHAR(50),
    PRIMARY KEY (movieID, type)
  )""")



  pass

def insertAll(db):
  """
  Inserts all tuples from source files into the database
  The data is located in /scratch/newhall/public/cs44/swatDB/RelationName.txt.
  Each field is separated by a horizontal bar |
  @param db - a Cursor object for the database connection
  """
  print("...Inserting Records...")

  # Insert Actor
  with open('/scratch/newhall/public/cs44/movieDB/Actor.txt', 'r', errors='backslashreplace') as f:
      actors = [line.strip().split('|') for line in f]
  db.executemany("INSERT INTO Actor VALUES (?, ?, ?, ?)", actors)

  # Insert Movie
  with open('/scratch/newhall/public/cs44/movieDB/Movie.txt', 'r', errors='backslashreplace') as f:
      movies = [line.strip().split('|') for line in f]
  db.executemany("INSERT INTO Movie VALUES (?, ?, ?)", movies)

  # Insert Director
  with open('/scratch/newhall/public/cs44/movieDB/Director.txt', 'r', errors='backslashreplace') as f:
      directors = [line.strip().split('|') for line in f]
  db.executemany("INSERT INTO Director VALUES (?, ?, ?)", directors)

  # Insert Casts
  with open('/scratch/newhall/public/cs44/movieDB/Casts.txt', 'r', errors='backslashreplace') as f:
      casts = [line.strip().split('|') for line in f]
  db.executemany("INSERT INTO Casts VALUES (?, ?, ?)", casts)

  # Insert DirectsMovie
  with open('/scratch/newhall/public/cs44/movieDB/DirectsMovie.txt', 'r', errors='backslashreplace') as f:
      directs = [line.strip().split('|') for line in f]
  db.executemany("INSERT INTO DirectsMovie VALUES (?, ?)", directs) 

  # Insert Genre (no foreign key!)
  with open('/scratch/newhall/public/cs44/movieDB/Genre.txt', 'r', errors='backslashreplace') as f:
      genres = [line.strip().split('|') for line in f]
  db.executemany("INSERT INTO Genre VALUES (?, ?)", genres)



def createIndexes(db):
    """
    Create indexes to optimize performance for specific queries.
    Usefulness of indexes is described in README.adoc
    """

    print("...Building Indexes...")

    # Speeds up selection of actors by name (queries 1, 2, 3, 5, 6, 7)
    db.execute("CREATE INDEX IF NOT EXISTS idx_actor_name ON Actor(fname, lname);")

    # Speeds up movie title selection (queries 2, 3, 6)
    db.execute("CREATE INDEX IF NOT EXISTS idx_movie_title ON Movie(title);")

    # Speeds up movie year filtering (query 6 and query 7: year 2000)
    db.execute("CREATE INDEX IF NOT EXISTS idx_movie_year ON Movie(year);")

    # Speeds up joins on actorID (queries 1, 2, 3, 5, 6, 7)
    db.execute("CREATE INDEX IF NOT EXISTS idx_casts_actor ON Casts(actorID);")

    # Speeds up joins on movieID (queries 1, 2, 3, 5, 6)
    db.execute("CREATE INDEX IF NOT EXISTS idx_casts_movie ON Casts(movieID);")

    # Speeds up grouping by director for prolific directors (query 4)
    db.execute("CREATE INDEX IF NOT EXISTS idx_directsmovie_director ON DirectsMovie(directorID);")

"""PROVIDED METHODS BELOW"""

def dropIndexes(db):
  """
  Removes all existing indexes in the database
  @param db - a Cursor object for the database connection
  """
  print("...Removing Indexes..")
  db.execute("""SELECT name
                FROM sqlite_master
                WHERE type == 'index' and name NOT LIKE 'sqlite%'""")
  results = db.fetchall()
  for row in results:
    db.execute("DROP INDEX "+row[0])

def checkDB(filename):
  """
  Checks to see if the database exists

  Determines if a database with the given filename already exists.
  If so, the user can exit the program, choose to rebuild the DB, or
  choose to rebuild only the indexes (and keep the data intact)

  @param filename - a str containing the name of the database file
  @return true if the entire DB should be built, false if only the indexes
    should be reconstructed, or exits the program
  """
  if os.path.exists(filename):
     choice = -1
     while(choice not in [0,1,2]):
         print("File already exists.  Would you like to:")
         print("  0) Exit the program")
         print("  1) Remove the file and rebuild the entire DB")
         print("  2) Keep the file and rebuild the indexes only")
         choice = int(input("Enter choice: "))
     if choice == 0:
         print("Exiting...")
         exit(1)
     elif choice == 1:
         os.remove(filename)
         return True
     else:
         return False
  return True


###########################################################
# main is complete: you can add functionality, but it is not required
def main():
  if(len(sys.argv) != 2):
      print("Error: Incorrect arguments")
      print("Usage: python3 createDB.py databaseName")
      return(1)
  filename = sys.argv[1] #uses command line argument
  fullbuild = checkDB(filename)


  #This is how we connect to a sqlite database
  #If the database doesn't exist, sqlite will create it
  conn = sqlite3.connect(filename)  #Open connection
  conn.text_factory = str           #Deals with string issues
  db = conn.cursor()                #A cursor takes in the sql commands

  if(fullbuild): #only create table and insert entries if building a new db
      print("Creating new movie database!\n")
      createTables(db)
      insertAll(db)
  else:
      dropIndexes(db)

  createIndexes(db)
  conn.commit()

if __name__ == "__main__":
  main()
