import psycopg2 as pg
from psycopg2.extras import DictCursor
from getpass import getpass

##############
# Connecting #
##############

cx = pg.connect(
  host='localhost',  database='abq',
  user=input('Username: '),
  password=getpass('Password: '),
  cursor_factory=DictCursor
)

cur = cx.cursor()

#####################
# Executing Queries #
#####################

cur.execute("""
  CREATE TABLE test
  (id SERIAL PRIMARY KEY, val TEXT)
""")
cur.execute("""
  INSERT INTO test (val)
  VALUES ('Banana'), ('Orange'), ('Apple');
""")

###################
# Retrieving Data #
###################

cur.execute("SELECT * FROM test")
num_rows = cur.rowcount
data = cur.fetchall()

print(f'Got {num_rows} rows from database:')
#print(data)
for row in data:
    # DictCursor rows can use string indexes
    print(row['val'])

#########################
# Parameterized Queries #
#########################

new_item = input('Enter new item: ')

#Never do this:
#cur.execute(f"INSERT INTO test (val) VALUES ('{new_item}')")
cur.execute("INSERT INTO test (val) VALUES (%s)", (new_item,))
# or:
# cur.execute("INSERT INTO test (val) VALUES (%(item)s)", {'item': new_item})
cur.execute('SELECT * FROM test')
print(cur.fetchall())

###############
# Cleaning Up #
###############

# Call this to actually save the data before leaving
# cx.commit()

# This is usually not necessary, but you can do it if you wish.
#cx.close()
