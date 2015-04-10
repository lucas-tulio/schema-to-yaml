import sys
import pymysql
from db import Database

def get_field_name(table_desc):
  field_name = table_desc[0]
  return field_name

def get_field_type(column_desc):
  field_type = column_desc[1]
  if "varchar" in field_type:
    return "string"
  elif "tinyint" in field_type or "boolean" in field_type:
    return "boolean"
  elif "int" in field_type:
    return "int"
  elif "text" in field_type:
    return "text"
  elif "date_time" in field_type:
    return "date_time"
  elif "date" in field_type:
    return "date"
  elif "timestamp" in field_type:
    return "timestamp"

def get_field_length(column_desc):
  field_type = column_desc[1]
  if "(" not in field_type: return 0
  else:
    field_length = field_type.split("(")[1].split(")")[0]
    return int(field_length)

def is_field_not_null(column_desc):
  not_null = column_desc[2]
  return not_null == "NO"

def is_field_unique(column_desc):
  field_is_unique = column_desc[3] == "UNI"
  return field_is_unique

def get_field_default_value(column_desc):
  default_value = column_desc[4]
  if default_value != "":
    return default_value
  return None

# Args check
if len(sys.argv) != 2:
  print("Usage: python3 schema-to-yaml.py schema_name")
  sys.exit()

# Connect to database
db = Database(sys.argv[1])

# Get table list
with open("schema.yaml", "w") as out:
  for table in db.get_table_list():

    table_name = table[0]

    # Table name
    out.write(table_name.split("_")[1] + ":\n")
    out.write("  lock_attributes: true\n")

    # Attributes
    out.write("  attributes:\n")
    table_desc = db.get_table_definition(table_name)

    for column_desc in table_desc:

      # Skip "_id"
      field_name = get_field_name(column_desc)
      if field_name == "_id":
        continue

      # Field name and type
      field_type = get_field_type(column_desc)
      out.write("    - name: " + field_name + "\n")
      out.write("      type: " + field_type + "\n")

      # Length
      field_length = get_field_length(column_desc)
      if field_length > 0:
        out.write("      length: " + str(field_length) + "\n")

      # Not Null?
      field_not_null = is_field_not_null(column_desc)
      if field_not_null:
        out.write("      required: true\n")

      # Unique?
      field_unique = is_field_unique(column_desc)
      if field_unique:
        out.write("      unique: true\n")

      # Default value?
      default_value = get_field_default_value(column_desc)
      if default_value != None:
        out.write("      default: " + str(default_value) + "\n")

      out.write("\n")
