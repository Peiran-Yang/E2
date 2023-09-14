import sqlite3

def init_db():
    conn = sqlite3.connect('stephen_king_movies.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS movies
                (id TEXT, name TEXT, year INT, rating REAL)''')
    return conn, c

def insert_data(conn, c, lines):
    c.executemany("INSERT INTO movies VALUES (?, ?, ?, ?)", lines)
    conn.commit()

def search_db(c, query, param):
    c.execute(query, param)
    return c.fetchall() or "No matching records"

if __name__ == "__main__":
    conn, c = init_db()
    with open('stephen_king_adaptations.txt', 'r') as f:
        lines = [tuple(line.strip().split(',')) for line in f]
    insert_data(conn, c, lines)

    options = {'1': ('name', 'LIKE', 'Enter the movie name: ', lambda x: '%'+x+'%'),
               '2': ('year', '=', 'Enter the movie year: ', int),
               '3': ('rating', '>=', 'Enter the movie rating: ', float)}
    
    while True:
        choice = input("\n1. By name\n2. By year\n3. By rating\n4. STOP\nChoice: ")
        if choice == '4': break
        if choice in options:
            col, op, msg, conv = options[choice]
            param = conv(input(msg))
            for row in search_db(c, f"SELECT * FROM movies WHERE {col} {op} ?", (param,)):
                print(row)
