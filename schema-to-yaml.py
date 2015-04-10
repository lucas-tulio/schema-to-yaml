import sys
import pymysql
from db import Database

# Args check
if len(sys.argv) != 2:
  print("Usage: python3 schema-to-yaml.py schema_name")
  sys.exit()

# Connect to database
db = Database(sys.argv[1])

# Get table list
for table in db.get_table_list():
  print(db.get_table_definition(table[0]))
  break

