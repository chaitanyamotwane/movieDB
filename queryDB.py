"""
queryDB.py

Copyright (c) 2025 Swarthmore College Computer Science Department
Swarthmore PA, Professors Tia Newhall, Ameet Soni

Names: George Ackall, Neil Zhu 
Date: April 7th, 2025
Description: Create runs 8 sql query searches   
"""
import sqlite3
import os
import sys
import time

############### main program ###########################
def main():

  # make sure it is run with correct num command line args
  if(len(sys.argv) != 2):
      print("Error: Incorrect arguments")
      print("Usage: python3 queryDB.py databaseName")
      return(1)

  # check if database file exists
  if(not os.path.exists(sys.argv[1])):
      print("Error: file does not exist")
      exit(1)

  conn = sqlite3.connect(sys.argv[1])  # open connection
  conn.text_factory = str              # deals with string issues
  db = conn.cursor()                   # a cursor takes in the sql commands

  print
  print("Welcome to the Movie Database!")

  #  Repeatedly call printMenu and execute the chosen query until the user
  #  Selects to Exit
  while True: 
    # this handles the exception of an invalid input
    try:
      option = printMenu()  # This may raise ValueError if user typed a non-integer
    except ValueError:
      print()
      print("Invalid Input! Please enter an integer from 0 to 8.\n")
      continue  # go back to top of while-loop to re-prompt


    # if the user choses option 0, exit the program 
    if option == 0:
      print("Exiting ...\n")
      break
    # if the user choses option 1-8, execute query X (1-8)
    elif option == 1:
      query1(db)
    elif option == 2:
      query2(db)
    elif option == 3:
      query3(db)
    elif option == 4:
      query4(db)
    elif option == 5:
      query5(db)
    elif option == 6:
      query6(db)
    elif option == 7:
      query7(db)
    elif option == 8:
      testquery(db)

  print()
  print("Thank you for using the Movie Database!")
  return

############PLACE QUERY FUNCTIONS HERE############
def testquery(db):
  """
  This is a test query for you to use to test
  out some simple queries before writing the
  required ones.
  """
  print("in testquery")
  title =  "The Mexican"
  query = """SELECT DISTINCT A.fname, A.lname 
          FROM Actor AS A
          JOIN Casts AS C ON A.id = C.actorID
          JOIN Movie AS M ON C.movieID = M.id
          WHERE M.title = ?
          ORDER BY A.fname, A.lname 
          """ 

  explainable_query = f"""
      SELECT DISTINCT A.fname, A.lname 
        FROM Actor AS A
        JOIN Casts AS C ON A.id = C.actorID
        JOIN Movie AS M ON C.movieID = M.id
        WHERE M.title = '{title}'
        ORDER BY A.fname, A.lname 
    """
  executeQuery(db, query, params=(title,), explain_query=explainable_query)
  return 


def query1(db):
  """
  Query 1: Cast of the Princess Bride
  List the names of all distinct actors in 
  the movie "The Princess Bride  
  """
  title =  "The Princess Bride"
  query = """SELECT DISTINCT A.fname, A.lname 
          FROM Actor AS A
          JOIN Casts AS C ON A.id = C.actorID
          JOIN Movie AS M ON C.movieID = M.id
          WHERE M.title = ?
          ORDER BY A.fname, A.lname 
          """ 
  
  # build parameter-free version of the query for EXPLAIN
  explainable_query = f"""
        SELECT DISTINCT A.fname, A.lname 
        FROM Actor AS A
        JOIN Casts AS C ON A.id = C.actorID
        JOIN Movie AS M ON C.movieID = M.id
        WHERE M.title = '{title}'
        ORDER BY A.fname, A.lname 
    """
  executeQuery(db, query, params=(title,), explain_query=explainable_query)
  return 


def query2(db):
  """
  Query 2: Actor Filmography
 	Ask the user for the name of an actor, and print 
  all the movies starring an actor with that name 
  (only print each title once).  
  """
  #promts the user to enter name of an actor
  fname = input("Enter Actor's first name: ")
  lname = input("Enter Actor's last name: ")

  query = """
      SELECT DISTINCT M.title
      FROM Actor AS A
      JOIN Casts AS C ON A.id = C.actorID
      JOIN Movie AS M ON C.movieID = M.id
      WHERE A.fname = ?
        AND A.lname = ?
      ORDER BY M.title
      """

  # build parameter-free version of the query for EXPLAIN
  explainable_query = f"""
      SELECT DISTINCT M.title
      FROM Actor AS A
      JOIN Casts AS C ON A.id = C.actorID
      JOIN Movie AS M ON C.movieID = M.id
      WHERE A.fname = '{fname}'
        AND A.lname = '{lname}'
      ORDER BY M.title
    """
  executeQuery(db, query, params=(fname,lname,), explain_query=explainable_query)
  return 

def query3(db):
  """
  Query 3: Co-stars
  Ask the user for the name of two actors. Print the names
  of all distinct movies in which those two actors co-starred.
  """
  #prompts the user to enter the name of actor 1 
  fname1 = input("Enter first actor's first name: ")
  lname1 = input("Enter first actor's last name: ")
  
  #prompts the user to enter the name of actor 1 
  fname2 = input("Enter second actor's first name: ")
  lname2 = input("Enter second actor's last name: ")

  query = """
      SELECT DISTINCT M.id, M.title
      FROM Actor AS A
      JOIN Casts AS C ON A.id = C.actorID
      JOIN Movie AS M ON C.movieID = M.id
      WHERE A.fname = ?
        AND A.lname = ?

      INTERSECT

      SELECT DISTINCT M.id, M.title
      FROM Actor AS A
      JOIN Casts AS C ON A.id = C.actorID
      JOIN Movie AS M ON C.movieID = M.id
      WHERE A.fname = ?
        AND A.lname = ?

      """

  # Build parameter-free version of the query for EXPLAIN
  explainable_query = f"""
      SELECT DISTINCT M.title
      FROM Actor AS A
      JOIN Casts AS C ON A.id = C.actorID
      JOIN Movie AS M ON C.movieID = M.id
      WHERE A.fname = '{fname1}'
        AND A.lname = '{lname1}'

      INTERSECT

      SELECT DISTINCT M.title
      FROM Actor AS A
      JOIN Casts AS C ON A.id = C.actorID
      JOIN Movie AS M ON C.movieID = M.id
      WHERE A.fname = '{fname2}'
        AND A.lname = '{lname2}'
      """
  executeQuery(db, query, params=(fname1, lname1, fname2, lname2,), explain_query=explainable_query)
  return 


def query4(db):
  """
  Query 4: Prolific Directors
  List all directors who directed 500 movies or more, in descending
  order of the number of movies they directed. Include the director's 
  name and the number of movies they directed.
  """
  query = """
      SELECT DISTINCT D.fname, D.lname, COUNT(M.id) AS FilmCount
      FROM Director AS D
      JOIN DirectsMovie AS DM ON DM.directorID = D.id
      JOIN Movie AS M ON DM.movieID = M.id
      GROUP BY DM.directorID
      HAVING COUNT(M.id) >= 500
      ORDER BY COUNT(M.id) DESC;
      """

  # build parameter-free version of the query for EXPLAIN
  explainable_query = f"""
      SELECT DISTINCT D.fname, D.lname, COUNT(M.id) AS FilmCount
      FROM Director AS D
      JOIN DirectsMovie AS DM ON DM.directorID = D.id
      JOIN Movie AS M ON DM.movieID = M.id
      GROUP BY DM.directorID
      HAVING COUNT(M.id) >= 500
      ORDER BY COUNT(M.id) DESC;
      """
  executeQuery(db, query, params=None, explain_query=explainable_query)
  return 

def query5(db):
  """
  Query 5: Bacon's Favorites
  Find Kevin Bacon's favorite co-stars. Print all actors that co-starred
  with Kevin Bacon in 8 or more movies, as well as the number of movies
  they co-starred in. Be sure that Kevin Bacon isn't in your results! 
  Only count each movie once per actor.
  """
  query = """
    SELECT A.fname, A.lname, COUNT(DISTINCT C.movieID) as 'NumFilms'
    FROM Actor AS A
    JOIN Casts AS C ON A.id = C.actorID
    WHERE  C.movieID IN
      (SELECT cB.movieID
      FROM Actor AS B
      JOIN Casts AS cB ON B.id = cB.actorID
      WHERE  B.fname = 'Kevin'
        AND B.lname = 'Bacon')
      AND A.id != 
        (SELECT B.id
        FROM   Actor AS B
        WHERE  B.fname = 'Kevin'
          AND  B.lname = 'Bacon')
    GROUP BY A.id
      HAVING COUNT(DISTINCT C.movieID) >= 8
      ORDER BY NumFilms DESC;
    """

  # build parameter-free version of the query for EXPLAIN
  explainable_query = f"""
    SELECT A.fname, A.lname, COUNT(DISTINCT C.movieID) as 'NumFilms'
    FROM Actor AS A
    JOIN Casts AS C ON A.id = C.actorID
    WHERE  C.movieID IN
      (SELECT cB.movieID
      FROM Actor AS B
      JOIN Casts AS cB ON B.id = cB.actorID
      WHERE  B.fname = 'Kevin'
        AND B.lname = 'Bacon')
      AND A.id != 
        (SELECT B.id
        FROM   Actor AS B
        WHERE  B.fname = 'Kevin'
          AND  B.lname = 'Bacon')
    GROUP BY A.id
      HAVING COUNT(DISTINCT C.movieID) >= 8
      ORDER BY NumFilms DESC;
    """

  executeQuery(db, query, params= None, explain_query=explainable_query)
  return 


def query6(db):
  """
  Query 6: Versatile Actors
  Find actors who played five or more roles in the same movie
  during the year 2010.
  """

  query = """
    SELECT A.fname, A.lname, M.title, COUNT(*) AS NumRoles
    FROM Actor A
    JOIN Casts C  ON A.id = C.actorID
    JOIN Movie M  ON C.movieID = M.id
    WHERE M.id IN 
      (SELECT id
      FROM Movie
      WHERE year = 2010)
    GROUP BY A.id, M.id
    HAVING COUNT(*) >= 5
    ORDER BY NumRoles DESC, M.title, A.fname, A.lname;
  """

  # build parameter-free version of the query for EXPLAIN
  explainable_query = f"""
    SELECT A.fname, A.lname, M.title, COUNT(*) AS NumRoles
    FROM Actor A
    JOIN Casts C  ON A.id = C.actorID
    JOIN Movie M  ON C.movieID = M.id
    WHERE M.id IN 
      (SELECT id
      FROM Movie
      WHERE year = 2010)
    GROUP BY A.id, M.id
    HAVING COUNT(*) >= 5
    ORDER BY NumRoles DESC, M.title, A.fname, A.lname;
  """
  executeQuery(db, query, params= None, explain_query=explainable_query)
  return 


def query7(db):
  """
  Query 7: Actors with Most Movies 
  Finds the top 10 actors with the most Filmography 
  """
  query = """
    SELECT A.fname, A.lname, COUNT(DISTINCT C.movieID) AS TotalMovie
    FROM Actor A
    JOIN Casts C ON A.id = C.actorID
    GROUP BY A.id
    ORDER BY TotalMovie DESC
    LIMIT 10;
  """

  # build parameter-free version of the query for EXPLAIN
  explainable_query = f"""
    SELECT A.fname, A.lname, COUNT(DISTINCT C.movieID) AS TotalMovie
    FROM Actor A
    JOIN Casts C ON A.id = C.actorID
    GROUP BY A.id
    ORDER BY TotalMovie DESC
    LIMIT 10;
  """
  executeQuery(db, query, params= None, explain_query=explainable_query)
  return 

############ HELPER FUNCTIONS ######

def executeQuery(db, query, params=None, explain_query=None):
  """
  This helper method executes the query, measures run-time
  and prints the results, runtime, and explains the query. 
  @param db - the database cursor
  @param query - the query to execute 
  @param params - the params passed in the query
  @param explain_query - parameter-free version of the query
  """
  # start timing
  start = time.time()

  # execute query
  if params is not None:
    db.execute(query, params)
  else:
    db.execute(query)

  # fetch all results
  results = db.fetchall()

  # 4) end timing
  end = time.time()

  # print the number of results and time that it took for the query 
  print("\n %s results; Completed in %.3f seconds\n " % (len(results), (end - start)))

  # calls printResults
  printResults(db, results)

  # calls explinQuery 
  if explain_query:
    explainQuery(db, explain_query)

  return results


############ PROVIDED METHODS - READ AND USE WHERE APPROPRIATE ######
def printResults(db, results):
    """
    Prints the formatted results of an already executed query.
    @param db - the database cursor
    @param results - the data returned by fetchall after the query was
    executed.
    """
    format = "%-20s " * len(db.description) #format template

    #print column headers
    colNames = [db.description[i][0] for i in range(len(db.description))]
    print(format % tuple(colNames))
    print("-"*20*len(colNames))

    #print tuples
    for row in results:
      print(format%row)

def explainQuery(db, query):
    """
    Prints the query plan for the given query
    @param db - the database cursor
    @param query - the query to explain
    """
    db.execute("EXPLAIN QUERY PLAN \n "+query)
    print("\nQuery Plan:")
    print("-----------")
    for row in db:
      print(row[3])


def printMenu():
  """Prompts the user with the query menu and returns the chosen query

  This function loops until the user enters a valid choice.  It is not
  safe against non-integer input
  Return: an integer from 1 to 8 corresponding to the query to execute
  """
  choice = -1
  while choice < 0 or choice > 8:
    print()
    print("Menu of options:")
    print("(0) Exit")
    print("(1) Query 1: Cast of the Princess Bride")
    print("(2) Query 2: Actor Filmography")
    print("(3) Query 3: Co-stars")
    print("(4) Query 4: Prolific Directors")
    print("(5) Query 5: Bacon's Favorites")
    print("(6) Query 6: Versatile Actors")
    print("(7) Query 7: Programmer's Choice")
    print("(8) test: test queries")
    choice = int(input("Enter your choice: "))
  print()
  return choice

if __name__ == "__main__":
  main()
