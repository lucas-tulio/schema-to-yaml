import pymysql

class Database:

  def __init__(self, schema):

    self.cur = None
    self.conn = None

    # Read parameters
    f = open("db.conf", "r")
    self.db_host = f.readline().split("=")[1].rstrip("\n")
    self.db_port = f.readline().split("=")[1].rstrip("\n")
    self.db_user = f.readline().split("=")[1].rstrip("\n")
    self.db_password = f.readline().split("=")[1].rstrip("\n")
    self.db_schema = schema
    f.close()

  def __del__(self):
    self._disconnect()

  def _connect(self):
    self.conn = pymysql.connect(host=self.db_host, port=int(self.db_port), user=self.db_user, passwd=self.db_password, db=self.db_schema, charset='utf8')
    self.cur = self.conn.cursor()

  def _disconnect(self):
    if self.cur != None:
      self.cur.close()
    if self.conn != None:
      self.conn.close()

  def get_table_list(self):
    self._connect()
    try:
      self.cur.execute("show tables")
      result = self.cur.fetchall()
      return result
    except Exception as e:
      print("Error reading table list")
      print(e)

    return False

  def get_table_definition(self, table_name):
    self._connect()
    try:
      self.cur.execute("DESC " + table_name)
      result = self.cur.fetchall()
      return result
    except Exception as e:
      print("Error reading table definition")
      print(e)

    return False
