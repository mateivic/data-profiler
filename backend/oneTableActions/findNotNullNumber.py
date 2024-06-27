import pandas as pd
from oneTableActions.oneTableAction import OneTableAction

class FindNotNullNumberAction(OneTableAction):
    def __init__(self, engine):
        self.engine = engine
        self.totalCount = 0
        self.notNullNum = {}
        
    def printResults(self):
        retValue = []
        if self.notNullNum and self.totalCount:
            notNullArr = []
            for col in self.notNullNum:
                if self.notNullNum[col] > 0:
                    notNullArr.append(f"{col} : {self.notNullNum[col]} NULL values ({round(self.notNullNum[col] * 1.0 / self.totalCount * 100, 2)}%)")
            if len(notNullArr) > 0:
                retValue.append({'label': 'NULL values:', 'value': notNullArr, 'valueIsArr': True})
            else:
                retValue.append({'label': 'NULL values:', 'value': "There are no NULL values in this table", 'valueIsArr': False})
        return retValue
    
    def act(self, table, columns):
        self.notNullNum = {}
        self.totalCount = int(pd.read_sql(f"select count(*) from {table};", self.engine).values[0])
        for idx, col in enumerate(columns):
            query  = f'select count(*) from {table} where {col} is null;'
            result = int(pd.read_sql(query, self.engine).values[0])
            self.notNullNum[col] = result