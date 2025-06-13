# MovieDB (SQL + Python)

This project implements a **relational movie database** using Python and SQLite3. The goal of the project is to demonstrate proficiency in **SQL query design, database schema creation, indexing for performance**, and Python integration with a relational database.

The dataset was derived from the IMDb dataset (up to 2015), and contains hundreds of thousands of records for movies, actors, directors, genres, and their interrelationships.

---

## Motivation

The primary goal of this project is to showcase **SQL and relational database skills**, including:

- Designing relational schemas  
- Writing efficient SQL queries with joins, grouping, and filtering  
- Building and justifying indices to optimize performence
- Using Python to interface with SQLite3  
- Analyzing query execution plans and timing performance  

---

## How the Program Works

### `createDB.py`: Building the Database

This script is responsible for **initializing and populating the database**:

- **User Prompt**: If the database file already exists, the user is prompted to choose between:
  - Rebuilding the database from scratch
  - Reusing the existing data but rebuilding indices
  - Exiting the program
- **Schema Creation**: Creates the relational tables with appropriate primary and foreign key constraints.
- **Data Ingestion**: Parses large `.txt` files line-by-line and inserts data into tables.
- **Index Creation**: Builds performance-enhancing indices to support efficient querying (see index list below).
- **Performance Note**: Creating the full database can take several minutes due to the large dataset and integrity checks.

### `queryDB.py`: Querying the Database

This script provides an **interactive command-line interface** to explore the database through predefined SQL queries.

- **Menu Interface**: Displays a menu of 8 queries for the user to select from.
- **User Input**: Some queries prompt for actor names or other parameters to customize the results.
- **Query Execution**:
  - SQL commands are executed via `sqlite3` using Python
  - Query results are displayed in a clean, formatted table
  - Query execution time is printed using Python’s `time` module
- **Query Optimization**:
  - The SQLite query planner (`EXPLAIN QUERY PLAN`) is used to display how each query runs
  - Temporary tables may be created for complex queries and dropped after execution

Together, these scripts demonstrate how to **combine procedural logic (Python)** with **declarative database logic (SQL)** in a clean and modular design.

---


## About SQLite

[SQLite](https://sqlite.org) is a self-contained, serverless, transactional SQL database engine.

- **Self-contained:** SQLite is "stand-alone" or "self-contained" in the sense that it has very few dependencies. It runs on any operating system, and uses no external libraries or interfaces (other than a few standard C-library calls)
- **Serverless:** Most SQL database engines are implemented as a separate server process. Programs that want to access the database communicate with the server using some kind of protocol (typically TCP/IP). With SQLite, the process that wants to access the database reads and writes directly from the database files on disk. No intermediary server process.
- **Transactional:** A transactional database is one in which all changes and queries appear to be Atomic, Consistent, Isolated, and Durable (ACID).

SQLite is the most widely deployed database in the world. It is ideal for applications where simplicity, portability, and reliability matter. Think of it not as a replacement for enterprise solutions like PostgreSQL or Oracle, but as a powerful and efficient alternative to using flat files — like a smarter, safer version of `fopen()`.

> “Make good and beautiful products that are fast, reliable, and simple to use — just as you have received SQLite for free, so also freely give.”

---


## Database Overview

The database schema consists of the following six tables:

| Table           | Description                                          |
|------------------|------------------------------------------------------|
| `Actor`          | Actor ID, first name, last name, and gender         |
| `Movie`          | Movie ID, title, and release year                   |
| `Director`       | Director ID, first name, and last name              |
| `Casts`          | Links actors to movies with a role field            |
| `DirectsMovie`   | Maps directors to movies                            |
| `Genre`          | Lists genres associated with movies                 |

---

## Description of Queries

| Query No. | Description |
|-----------|-------------|
| **1** | List all distinct actors who appeared in **"The Princess Bride"**. |
| **2** | Prompt for an actor’s name and display all movies they starred in. |
| **3** | Prompt for two actors’ names and list all movies they **co-starred** in. |
| **4** | List all directors who directed **≥ 500 movies**, sorted by number of movies directed (descending). |
| **5** | Find **Kevin Bacon’s favorite co-stars** — actors who appeared with him in **≥ 8 different movies**. |
| **6** | List actors who played **≥ 5 distinct roles in the same movie** during **2010**. |
| **7** | Programmer’s choice: A meaningful, original query created to highlight relational reasoning and multi-table joins. |
| **8** | A placeholder test query, useful for debugging and experimentation. |

Each query:

- Displays formatted query results  
- Reports query execution time  
- Shows the **SQLite query plan** for performance insight  

---

## Indices Used and Justification

| Index Name                 | Table         | Columns               | Purpose                                                    |
|----------------------------|---------------|------------------------|------------------------------------------------------------|
| `idx_actor_name`           | `Actor`       | `(fname, lname)`       | Speeds up queries 1, 2, 3, 5, and 6 (actor name lookups)   |
| `idx_movie_title`          | `Movie`       | `(title)`              | Speeds up movie searches in queries 1 and 2                |
| `idx_casts_actor_movie`    | `Casts`       | `(actorID, movieID)`   | Optimizes co-actor matching in queries 3, 5, and 6          |
| `idx_casts_movie_actor`    | `Casts`       | `(movieID, actorID)`   | Improves performance for queries involving movie-first joins |
| `idx_director_id`          | `Director`    | `(id)`                 | Supports fast join for query 4                             |
| `idx_directsmovie_director`| `DirectsMovie`| `(directorID)`         | Optimizes director lookup for query 4                      |
| `idx_movie_year`           | `Movie`       | `(year)`               | Used for filtering by year in query 6                      |

SQLite auto-indexes primary keys; no need to create separate indices on `id` fields unless using composite keys.

---

## How to Run

### 1. Prerequisites

Ensure you have **Python 3** and **SQLite3** installed:

```bash
python3 --version
sqlite3 --version
```

### 2. Clone the Repository

```bash
git clone https://github.com/chaitanyamotwane/movieDB.git
cd movie-database-sqlite
```

### 3. Create the Database

```bash
python3 createDB.py your_database.db
```

This script:

- Creates the six core tables  
- Parses and inserts records from text files (e.g., `Actor.txt`)  
- Applies `INSERT INTO` commands for all records  
- Constructs performance-boosting indices  

### 4. Query the Database

```bash
python3 queryDB.py your_database.db
```

This launches a command-line menu for interacting with the database and running queries.

---

## Learn More

- [SQLite Official Docs](https://www.sqlite.org/docs.html)  
- [Python `sqlite3` Module](https://docs.python.org/3/library/sqlite3.html)  
- [SQL Tutorial at SQLZoo](https://sqlzoo.net)  

---

## License

The data is derived from the IMDb dataset (pre-2015) and is used **strictly for educational purposes**.
