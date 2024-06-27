from getpass import getpass
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from helpers import to_lowercase
import json
import pandas as pd

class CredentialsAndConfig:
    def __init__(self, success, engine, tablesAndColumns, errorMsg):
        self.success = success
        self.engine = engine
        self.tablesAndColumns = tablesAndColumns
        self.errorMsg = errorMsg
        
class RelevantTablesAndColumns:
    def __init__(self, success, tablesAndColumns, errorMsg):
        self.success = success
        self.tablesAndColumns = tablesAndColumns
        self.errorMsg = errorMsg
        

def enterCredentialsAndConfig(formData):
    try: 
        engine = create_engine(f'postgresql+psycopg2://{formData["username"]}:{formData["password"]}@{formData["host"]}:{formData["port"]}/{formData["dbName"]}')
        # engine = create_engine(f'postgresql+psycopg2://postgres:bazepodataka@localhost:5432/DiplProjekt')
        engine.connect()
        if 'configFile' in formData:
            response = getRelevantTablesAndColumns(engine, formData["configFile"])
        else:
            response = getRelevantTablesAndColumns(engine, None)
        if response.success is True:
            return CredentialsAndConfig(success=True, engine=engine, tablesAndColumns=response.tablesAndColumns, errorMsg="")
        else:
            return CredentialsAndConfig(success=False, engine=None, tablesAndColumns=None, errorMsg=response.errorMsg)
    except SQLAlchemyError as ex:
        return CredentialsAndConfig(success=False, engine=None, tablesAndColumns=None, errorMsg=f"An error happend while trying to connect to the database. Please check your input. Stack trace: {ex.__cause__}")
        
def getRelevantTablesAndColumns(engine, configFile):
    if configFile:
        try:
            with open(f"../configs/{configFile}", 'r') as file:
                data = json.load(file)
                data_lowercase = to_lowercase(data)
                modified_data = data_lowercase
                verifyConfigFile(engine, modified_data)
                return RelevantTablesAndColumns(success=True, tablesAndColumns=modified_data, errorMsg="")
        except FileNotFoundError:
            return RelevantTablesAndColumns(success=False, tablesAndColumns=None, errorMsg=f"The file {configFile} does not exist.")
        except json.JSONDecodeError as err:
            return RelevantTablesAndColumns(success=False, tablesAndColumns=None, errorMsg=f"Error decoding JSON from the file {configFile}: {err.__cause__}.")
        except Exception as err:
            return RelevantTablesAndColumns(success=False, tablesAndColumns=None, errorMsg=f"Error decoding JSON from the file {configFile}: {err}.")
    else:
        tables = pd.read_sql("select table_name from information_schema.tables where table_schema = 'public'", engine)
        returnDict = {}
        for index, row in tables.iterrows():
            table = row['table_name'].lower()
            columns = pd.read_sql(f"select column_name from information_schema.columns where table_name = '{table}';", engine).iloc[:, 0].to_list()
            columns = [col.lower() for col in columns]
            returnDict[table] = columns
        return RelevantTablesAndColumns(success=True, tablesAndColumns=returnDict, errorMsg="")

def verifyConfigFile(engine, configFile):
    tables = pd.read_sql("select table_name from information_schema.tables where table_schema = 'public'", engine).iloc[:, 0].to_list()
    tables = [table.lower() for table in tables]
    for configFileTable in configFile:
        if configFileTable.lower() not in tables:
            raise Exception(f"Table {configFileTable} doesn't exist in database.")
        else:
            columns = pd.read_sql(f"select column_name from information_schema.columns where table_name = '{configFileTable}';", engine).iloc[:, 0].to_list()
            columns = [column.lower() for column in columns]
            if not (set(configFile[configFileTable]) <= set(columns)):
                raise Exception(f"Some columns of table {configFileTable} don't exist in database.")
    

    