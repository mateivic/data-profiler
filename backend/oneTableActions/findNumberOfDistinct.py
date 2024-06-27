import pandas as pd
from oneTableActions.oneTableAction import OneTableAction

class FindNumberOfDistinctAction(OneTableAction):
    def __init__(self, engine):
        self.engine = engine
        self.totalCount = 0
        self.countDistinct = {}
        
    def printResults(self):
        retValue = []
        if self.countDistinct and self.totalCount:
            distinctArr = []
            for col in self.countDistinct:
                distinctArr.append(f"{col} : {self.countDistinct[col]} distinct values ({round(self.countDistinct[col] * 1.0 / self.totalCount * 100, 2)}%)")
            retValue.append({'label': 'Distinct values:', 'value': distinctArr, 'valueIsArr': True})
        return retValue
    
    def act(self, table, columns):
        query  = "select "
        for idx, col in enumerate(columns):
            query += f'count(distinct {col}) {col}, '
        query += f"count(*) row_num from {table};"
        result = pd.read_sql(query, self.engine)
        self.countDistinct = {}
        self.totalCount = int(result['row_num'][0])
        for col in columns:
            self.countDistinct[col] = int(result[col][0])