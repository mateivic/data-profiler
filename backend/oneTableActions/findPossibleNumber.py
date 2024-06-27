import pandas as pd
from oneTableActions.findRowType import FindRowTypeAction
from oneTableActions.oneTableAction import OneTableAction
import datefinder


regex = "'^-?\d+(\.\d+)?$'"

class FindPossibleNumberAction(OneTableAction):
    def __init__(self, engine):
        self.engine = engine
        self.candidates = []
        self.possibleTypes = ["character varying", "text", "char", "character"]
        self.matchPercentage = 100
        
    def printResults(self):
        retValue = []
        if len(self.candidates) > 0:
            retValue.append({'label': f"Candidates for possible number column ({self.matchPercentage}% match):", 'value': ', '.join(self.candidates), 'valueIsArr': False})
        return retValue
        
    def act(self, table, columns):
        types = FindRowTypeAction(self.engine)
        types.act(table, columns)
        self.candidates = []
        for col in types.rowType:
            if types.rowType[col] in self.possibleTypes:
                query = f'select count({col}) * 1.0 / (select count({col}) from {table} where {col} is not null) * 100 {col} from {table} where {col} is not null and {col} ~ '
                query += regex
                result = pd.read_sql(query, self.engine)
                result = result[col][0]
                if result >= self.matchPercentage:
                    self.candidates.append(col)