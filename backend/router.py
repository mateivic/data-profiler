from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from oneTableActions.findTop10Distinct import FindTop10DistinctAction
from oneTableActions.findNotNullNumber import FindNotNullNumberAction
from multipleTableActions.findForeignKeyAction import FindForeignKeyAction
from oneTableActions.findColAndRowCount import FindColAndRowCountAction
from oneTableActions.findMaxMinAvg import FindMaxMinAvgAction
from oneTableActions.findNumberOfDistinct import FindNumberOfDistinctAction
from oneTableActions.findPossibleDate import FindPossibleDateAction
from oneTableActions.findPossibleNumber import FindPossibleNumberAction
from oneTableActions.findPossibleOIB import FindPossibleOIBAction
from oneTableActions.findPrimaryKey import FindPrimaryKeyAction
from oneTableActions.findRowType import FindRowTypeAction
from initialization import enterCredentialsAndConfig

Engine = None
TablesWithColumns = {}

app = Flask(__name__)
CORS(app)

@app.route('/getTableInfo/<table>', methods=['GET'])
def getTableInfo(table):
    global Engine
    global TablesAndColumns
    returnValue = []
    if table == 'relations':
        multipleTableAction = FindForeignKeyAction(Engine, TablesAndColumns)
        multipleTableAction.act()
        returnValue += multipleTableAction.printResults()
    else:
        oneTableActions = [FindPrimaryKeyAction(Engine), FindNumberOfDistinctAction(Engine), FindNotNullNumberAction(Engine), FindTop10DistinctAction(Engine), FindRowTypeAction(Engine), FindMaxMinAvgAction(Engine), FindPossibleOIBAction(Engine), FindPossibleDateAction(Engine), FindPossibleNumberAction(Engine), FindColAndRowCountAction(Engine)]
        for action in oneTableActions:
            action.act(table, TablesAndColumns[table])
            returnValue += action.printResults()
            
    response = jsonify({'result': returnValue})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/getDBTables', methods=['GET'])
def getDBTables():
    global Engine
    global TablesAndColumns
    if (len(TablesAndColumns.keys()) > 0):
        response = jsonify({'tables': list(TablesAndColumns.keys())})
    else:
        response = jsonify({'tables': []})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/sendCrentials', methods=['POST'])
def init():
    formData = json.loads(request.get_data())
    result = enterCredentialsAndConfig(formData)
    global Engine
    global TablesAndColumns

    if result.success:
        Engine = result.engine
        TablesAndColumns = result.tablesAndColumns
        response = jsonify({'error': ''})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    else:
        Engine = None
        TablesAndColumns = {}
        response = jsonify({'error': result.errorMsg})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
        

if __name__ == '__main__':
    app.run()