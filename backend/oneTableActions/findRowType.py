import pandas as pd
from oneTableActions.oneTableAction import OneTableAction

class FindRowTypeAction(OneTableAction):
    def __init__(self, engine):
        self.engine = engine
        self.rowType = {}
        
    def printResults(self):
        returnValue = []
        if self.rowType:
            returnArr = []
            for col in self.rowType:
                returnArr.append(f"{col} : {self.rowType[col]}")
            returnValue.append({'label': 'Column types:', 'value': returnArr, 'valueIsArr': True})
        return returnValue
        
    def act(self, table, columns):
        query  = "select "
        for idx, col in enumerate(columns):
            query += f'pg_typeof({col}) as {col} '
            if idx != len(columns) - 1:
                query += ", "
        query += f"from {table};"
        result = pd.read_sql(query, self.engine)
        self.rowType = {}
        for col in columns:
            self.rowType[col] = result[col][0]