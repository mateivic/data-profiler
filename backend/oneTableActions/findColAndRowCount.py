import pandas as pd
from oneTableActions.oneTableAction import OneTableAction

class FindColAndRowCountAction(OneTableAction):
    def __init__(self, engine):
        self.engine = engine
        self.colNum = 0
        self.rowNum = 0
        
    def printResults(self):
        returnVal = []
        if self.colNum > 0:
            returnVal.append({'label': 'ColNum', 'value': str(self.colNum), 'valueIsArr': False})
        if self.rowNum > 0:
            returnVal.append({'label': 'RowNum', 'value': str(self.rowNum), 'valueIsArr': False})
        return returnVal
        
    def act(self, table, columns):
        query = f"select count(*) from {table};"
        self.rowNum = pd.read_sql(query, self.engine).values[0][0]
        query2 = f"select count(column_name) from information_schema.columns where table_name = '{table}';"
        self.colNum = pd.read_sql(query2, self.engine).values[0][0]

        