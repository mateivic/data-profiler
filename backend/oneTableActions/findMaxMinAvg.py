import pandas as pd
from oneTableActions.findPossibleNumber import FindPossibleNumberAction
from oneTableActions.findRowType import FindRowTypeAction
from oneTableActions.oneTableAction import OneTableAction

class FindMaxMinAvgAction(OneTableAction):
    def __init__(self, engine):
        self.engine = engine
        self.maxMinAvg = {}
        self.relevantTypes = ["smallint", "integer", "decimal", "bigint", "numeric", "real", "double precision", "smallserial", "serial", "bigserial", "money"]
        
    def printResults(self):
        returnVal = []
        if self.maxMinAvg:
            maxMinAvg = []
            for col in self.maxMinAvg:
                if self.maxMinAvg[col]:
                    maxMinAvg.append(f"{col} : {', '.join('{}: {}'.format(k, v) for k, v in self.maxMinAvg[col].items())}")
            returnVal.append({'label': 'Max, min and average values in columns:', 'value': maxMinAvg, 'valueIsArr': True})
        return returnVal
        
    def act(self, table, columns):
        types = FindRowTypeAction(self.engine)
        types.act(table, columns)
        numbers = FindPossibleNumberAction(self.engine)
        numbers.act(table, columns)
        self.maxMinAvg = {}
        for idx, col in enumerate(columns):
            self.maxMinAvg[col] = {}
            if types.rowType[col] in self.relevantTypes:
                self.maxMinAvg[col]["Min"] =  self.__findMin(table, col)
                self.maxMinAvg[col]["Max"] =  self.__findMax(table, col)
                self.maxMinAvg[col]["Avg"] = self.__findAvg(table, col)
            elif col in numbers.candidates:
                colValues = pd.read_sql(f"select {col} from {table}", self.engine)
                colValues = pd.to_numeric(colValues.iloc[:, 0])
                self.maxMinAvg[col]["Min"] = colValues.min()
                self.maxMinAvg[col]["Max"] = colValues.max()
                self.maxMinAvg[col]["Avg"] = round(colValues.mean(), 2)


            
            
    def __findMax(self, table, column):
        query = f'select max({column}) {column} from {table};'
        result = pd.read_sql(query, self.engine)
        return result[column][0]
    
    def __findMin(self, table, column):
        query = f'select min({column}) {column} from {table};'
        result = pd.read_sql(query, self.engine)
        return result[column][0]
    
    def __findAvg(self, table, column):
        query = f'select avg({column}) {column} from {table};'
        result = pd.read_sql(query, self.engine)
        return round(result[column][0], 2)

        