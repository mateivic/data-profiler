import pandas as pd
from oneTableActions.oneTableAction import OneTableAction

class FindPrimaryKeyAction(OneTableAction):
    def __init__(self, engine):
        self.engine = engine
        self.candidates = []
        self.candidatesWithIndex = []
        
    def printResults(self):
        retValue = []
        if len(self.candidates) > 0:
            retValue.append({'label': ["Candidates for primary key (100% uniqueness):"], 'value': ', '.join(self.candidates), 'valueIsArr': False})
            if len(self.candidatesWithIndex) > 0:
                retValue.append({'label': "Candidates for primary key (100% uniqueness AND has unique index):", 'value': ', '.join(self.candidatesWithIndex), 'valueIsArr': False})
        else:
            retValue.append({'label': "Candidates for primary key (100% uniqueness):", 'value': "There are no candidates for primary key.", 'valueIsArr': False})
        return retValue
        
    def act(self, table, columns):
        query  = "select "
        for idx, col in enumerate(columns):
            query += f'count(distinct {col}) * 1.0 / count(*) as {col} '
            if idx != len(columns) - 1:
                query += ", "
        query += f"from {table};"
        result = pd.read_sql(query, self.engine).values[0]
        self.candidates = []
        self.candidatesWithIndex.clear()
        for idx, perc in enumerate(result):
            if perc == 1.0:
                self.candidates.append(columns[idx])
                
        if (len(self.candidates) > 0): 
            self.__checkForIndexes(table)
            
        
    def __checkForIndexes(self, table):
        query = f"select tablename, indexdef from pg_indexes where tablename = '{table}'"
        result = pd.read_sql(query, self.engine)
        candidatesWithIdxTemp = set()
        for index, row in result.iterrows():
            if "unique index" in row["indexdef"].lower():
                for candidate in self.candidates:
                    if candidate.lower() in row["indexdef"].lower():
                        candidatesWithIdxTemp.add(candidate)
        self.candidatesWithIndex = list(candidatesWithIdxTemp)