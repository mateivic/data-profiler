import pandas as pd
from oneTableActions.oneTableAction import OneTableAction

class FindTop10DistinctAction(OneTableAction):
    def __init__(self, engine):
        self.engine = engine
        self.top10 = {}
        
    def printResults(self):
        retValue = []
        arr = []
        for row in self.top10:
            if(len(self.top10[row]) == 0):
                arr.append(f"{row} : All values ​​appear only once")
            else:
                arr2 = []
                for element in self.top10[row]:
                    arr2.append(f"{element['name']} -> {element['count']} appearances")
                arr.append({"label": row, "value": arr2})
        retValue.append({"label": "Most common values:", "value": arr, "valueIsArr": True})
        return retValue
    
    def act(self, table, columns):
        self.top10 = {}
        for idx, col in enumerate(columns):
            query  = f"select {col},  count(*) num from {table} where {col} is not null group by {col} having count(*) > 1 order by num desc limit 10;"
            result = pd.read_sql(query, self.engine)
            if len(result[col]) > 0:
                arr = []
                for index, row in result.iterrows():
                    arr.append({"name": row[col], "count": row["num"]})
                self.top10[col] = arr
            else:
                self.top10[col] = []