import pandas as pd
from oneTableActions.findRowType import FindRowTypeAction
from oneTableActions.oneTableAction import OneTableAction
import datefinder


class FindPossibleDateAction(OneTableAction):
    def __init__(self, engine):
        self.engine = engine
        self.candidates = []
        self.possibleTypes = ["character varying", "text", "char", "character"]
        self.matchPercentage = 95
        
    def printResults(self):
        retValue = []
        if len(self.candidates) > 0:
            retValue.append({ 'label': f"Candidates for possible date column (more than {self.matchPercentage}% match):", 'value': ', '.join(self.candidates), 'valueIsArr': False})
        return retValue
        
    def act(self, table, columns):
        types = FindRowTypeAction(self.engine)
        types.act(table, columns)
        self.candidates = []
        for col in types.rowType:
            if types.rowType[col] in self.possibleTypes:
                query = f'select {col} from {table} where {col} is not null;'
                colValues = pd.read_sql(query, self.engine).iloc[:, 0].to_list()
                numOfMatches = 0
                for idx, colValue in enumerate(colValues):
                    matches = datefinder.find_dates(colValue)
                    for match in matches:
                        numOfMatches += 1
                        break
                    if idx > (len(colValues) / 5) and (numOfMatches / idx) < 0.5:
                        break  

                if (numOfMatches / len(colValues) * 100 > self.matchPercentage): 
                    self.candidates.append(col)
            
        