import sqlite3
import mutex
#test

class SlaveNode:
    def __init__(self):
        self.node_dict = {'node_id': {"value": "0", "type": "TEXT", "property": "NOT NULL"},
                          'node_time': {"value": "0", "type": "TEXT", "property": "NOT NULL"},
                          'node_temp': {"value": 0, "type": "REAL", "property": "NOT NULL"},
                          'node_watertemp': {"value": 0, "type": "REAL", "property": "NOT NULL"},
                          'node_humi': {"value": 0, "type": "REAL", "property": "NOT NULL"},
                          'node_led': {"value": "ON", "type": "TEXT", "property": "NOT NULL"}
                          }
        #it is string
        self.column = []
        self.create_column()
        #it is string
        self.values = []
        self.create_values()
        self.template = ""
        self.create_template()

    def update(self, input_dict):
        for keys in input_dict:
            if not self.node_dict.has_key(keys):
                print("node_dict does not keep the " + keys)
                return 1
            self.node_dict[keys]["value"] = input_dict[keys]
        self.refresh()
        return 0

    #syn the modify of dict to the element
    def refresh(self):
        self.create_column()
        self.create_values()
        self.create_template()

    def create_template(self):
        # must do this to make sure the template is empty when we rebuild the template
        self.template = ""
        sql_str = "("
        for keys in self.node_dict:
            sql_str += keys + " " + str(self.node_dict[keys]["type"]) + str(self.node_dict[keys]["property"]) + ","
        sql_str = sql_str[0:(sql_str.__len__()-1)]
        sql_str += ")"
        self.template = sql_str

    def create_column(self):
        #just like the template
        self.column = []
        for keys in self.node_dict:
            self.column.append(keys)

    def create_values(self):
        #just like the template
        self.values = []
        for keys in self.node_dict:
            if self.node_dict[keys]["type"] == "REAL" or self.node_dict[keys]["type"] == "INTEGER":
                str_temp = str(self.node_dict[keys]["value"])
                self.values.append(str_temp)
            elif self.node_dict[keys]["type"] == "TEXT":
                str_temp = "'" + str(self.node_dict[keys]["value"]) + "'"
                self.values.append(str_temp)
            else:
                print("values error\n")


class RecordDb(SlaveNode):
    def __init__(self):
        try:
            self.patch = "RecordDB.db"
            self.table = "Record"
            SlaveNode.__init__(self)
            self.connect = sqlite3.connect(self.patch)
            self.cursor = self.connect.cursor()
            self.cursor.execute("select * from sqlite_master where tbl_name = '%s'" % self.table)
            self.data_row = self.cursor.fetchone()
            self.mutex = mutex.mutex()
            self.sync = 0
            if not self.data_row:
                self.cursor.execute("CREATE TABLE %s %s" % (self.table, self.template))
        except Exception, e:
            print("MoDb init failed\n")
            print(e)

    def do_close(self):
        try:
            self.connect.close()
            print("MoDb Closed\n")
        except Exception, e:
            print("MoDb Closed failed")
            print(Exception, e)

    def sql_insert(self):
        sql_str = "("
        for index in range(len(self.values)):
            sql_str += self.values[index] + ","
        sql_str = sql_str[0:(sql_str.__len__() - 1)]
        sql_str += ")"
        sql_str = "INSERT INTO" + " " + self.table + " " + "VALUES" + " " + sql_str
        return sql_str

    #write the whole node into Mo
    def data_write(self, input_dict):
        if not input_dict.__len__():
            print("error NULL input dict")
            return
        if self.update(input_dict):
            return
        # check if there is a node with node_id,if not ,create one
        sql_str = self.sql_insert()
        self.cursor.execute(sql_str)
        self.connect.commit()

    def do_write(self, input_dict):
        self.data_write(input_dict)

    def lock_action(self):
        if self.sync:
            print("lock error")
            return
        self.sync = 1

    def lock(self):
        self.mutex.lock(self.lock_action(), self)

    def unlock(self):
        self.sync = 0
        self.mutex.unlock()

"""
myMO = MoDb()
myNode = SlaveNode()
myNode.node_id =4
myNode.node_time = "1128.0"
myNode.node_temp = 27.0
myNode.update_dict()
myMO.do_write(myNode)
node = myMO.do_read(4)
myMO.do_close()
"""
