import pandas as pd
from multipleTableActions.multipleTableAction import MultipleTableAction
from oneTableActions.findPrimaryKey import FindPrimaryKeyAction

#foreign key candidates = [aimedTable, aimedColumn, candidateTable, candidateColumn, posibitityPercentage, overlapPercentage]

class FindForeignKeyAction(MultipleTableAction):
    def __init__(self, engine, tablesWithColumns):
        self.engine = engine
        self.tablesWithColumns = tablesWithColumns
        self.candidates = []
        self.possibitityMargin = 0.98
        self.overlapMargin = 0.4
        
    def printResults(self):
        retValue = []
        valueRows = []
        if len(self.candidates) > 0:
            for candidate in self.candidates:
                valueRows.append(f"{candidate[0]}({candidate[1]}) --->  {candidate[2]}({candidate[3]}) with posibility of {round(candidate[4] * 100, 2)}% and overlap of {round(candidate[5] * 100, 2)}%")
            retValue.append({'label': "Foreign keys predictions [Referenced table(column) ---> Referencing table(column)]", 'value': valueRows, 'valueIsArr': True})
        else:
            retValue.append({'label': "Foreign keys predictions [Referenced table(column) ---> Referencing table(column)]", 'value': valueRows, 'There are no candiates for foreign key.': False})
        return retValue
        
    def act(self):
        primaryKeyFinder = FindPrimaryKeyAction(self.engine)
        self.candidates = []
        for table in self.tablesWithColumns:
            primaryKeyFinder.act(table, self.tablesWithColumns[table])
            for primaryKey in primaryKeyFinder.candidates:
                primaryKeyElements = pd.read_sql("select " + primaryKey + " from " + table, self.engine).iloc[:, 0].astype(str).to_list()
                for otherTable in self.tablesWithColumns:
                    if otherTable != table:
                        self.__findPossibleForeignKey(table, primaryKey, primaryKeyElements, otherTable, self.tablesWithColumns[otherTable])

                            
    def __findPossibleForeignKey(self, aimedTable, aimedColumn, columnPattern, candidateTable, candidateColumns):
        columnElementsWithNullsNum = pd.read_sql("select count(*) num from " + candidateTable, self.engine).values[0][0]
        for column in candidateColumns:
            columnElementsWithoutNullsNum = pd.read_sql("select count(*) num from " + candidateTable + " where " + column + " is not null", self.engine).values[0][0]
            columnElements = pd.read_sql("select distinct(" + column + ") from " + candidateTable + " where " + column + " is not null", self.engine).iloc[:, 0].astype(str).to_list()
            numOfOverlaying = 0
            
            for idx, columnElement in enumerate(columnElements):
                if columnElement in columnPattern:
                    numOfOverlaying += 1
                if (idx > len(columnElements) / 20) and (numOfOverlaying / idx < 0.5):
                    break
                    
            if (numOfOverlaying / len(columnElements)) > self.possibitityMargin:
                notNullPercentage = columnElementsWithoutNullsNum / columnElementsWithNullsNum
                possibility = numOfOverlaying / len(columnElements)
                overlap = (len(columnElements) / len(columnPattern)) * notNullPercentage
                if overlap > self.overlapMargin:
                    self.candidates.append([aimedTable, aimedColumn, candidateTable, column, possibility, overlap])