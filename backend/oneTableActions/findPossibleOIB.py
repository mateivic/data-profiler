import pandas as pd
from oneTableActions.findRowType import FindRowTypeAction
from oneTableActions.oneTableAction import OneTableAction

regex = "'^[0-9]{11}$'"

class FindPossibleOIBAction(OneTableAction):
    def __init__(self, engine):
        self.engine = engine
        self.candidates = []
        self.possibleTypes = ["character varying", "text", "char", "character"]
        self.matchPercentage = 95
        
    def printResults(self):
        retValue = []
        if len(self.candidates) > 0:
            retValue.append({'label': f"Candidates for possible OIB column (more than {self.matchPercentage}% match):", 'value': ', '.join(self.candidates), 'valueIsArr': False})
        return retValue
        
    def act(self, table, columns):
        types = FindRowTypeAction(self.engine)
        types.act(table, columns)
        self.candidates = []
        relevantColumns = []
        for col in types.rowType:
            if types.rowType[col] in self.possibleTypes:
                relevantColumns.append(col)
        for col in relevantColumns:
            query = f'select count({col}) * 1.0 / (select count(*) from {table}) * 100 {col} from {table} where {col} ~ '
            query += regex
            percentage = pd.read_sql(query, self.engine)
            if percentage[col][0] > self.matchPercentage: 
                values = pd.read_sql(f'select {col} from {table} where {col} ~ {regex}', self.engine).iloc[:, 0].to_list()
                candidate = True
                for value in values: 
                    if int(value[-1]) != self.__calculateControlNumber(value[:-1]):
                        candidate = False
                        break
                                    
                if candidate:
                    self.candidates.append(col)
                
    def __calculateControlNumber(self, oib):
        a = 10
        for i in range(10):
            a = (a + int(oib[i])) % 10
            if a == 0:
                a = 10
            a = (2 * a) % 11

        controlNum = 11 - a
        if controlNum == 10:
            controlNum = 0
        elif controlNum == 11:
            controlNum = 1
        
        return controlNum
            
        