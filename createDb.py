import csv, sqlite3

conn = sqlite3.connect('wines.db') # creates a database
cursor = conn.cursor() # method that iterrates through our db

# create a table
cursor.execute("""CREATE TABLE wine_list (
    WineID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT,
    Producer TEXT,
    Origin TEXT,
    Vegan TEXT
)""")

with open('barnivore_new.csv', 'r') as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['Name'], i['Producer'], i['Origin'], i['Vegan']) for i in dr]

cursor.executemany('INSERT INTO wine_list (Name, Producer, Origin, Vegan) VALUES (?, ?, ?, ?);', to_db)

# # commit  our command
conn.commit()

# # close our connection
conn.close()