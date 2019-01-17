from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
from sql import Sql

sql = Sql()

class Parts(Resource):
    cursor = None
    parser = None
    connection = None

    def __init__(self):
        sql.cursor = self.cursor
        sql.connection = self.connection

    def get(self):
        args = self.parser.parse_args()
        if 'id' in args :
            return(jsonify({'part':sql.getObjects('parts', args['id'])}))
        else:
            return(jsonify({'parts':sql.getObjects('parts',0)}))

    def put(self):
        args = self.parser.parse_args()
        cat = int(args['categoryId']) ;
        sqlCommand = "INSERT INTO parts(categoryId,name,description) VALUES(" + str(cat) + ",'" + args['name'] + "','" + args['description']+"')"
        self.cursor.execute(sqlCommand)
        self.connection.commit()

        #get new id
        self.cursor.execute("SELECT id FROM parts ORDER BY id DESC LIMIT 1;")
        newestId = self.cursor.fetchone()[0]
        #add amount
        sqlCommand = "INSERT INTO amounts(partid,amount) VALUES(" + str(newestId) + ","+str(args['amount']) + ");"

        self.cursor.execute(sqlCommand)
        self.connection.commit()
        #read new entry
        sqlCommand ='SELECT p.id, c.name,p.name, p.description, a.amount FROM parts as p LEFT JOIN amounts as a ON p.id=a.partid LEFT JOIN categories as c ON c.id = p.categoryId ORDER BY p.id DESC LIMIT 1;'
        self.cursor.execute(sqlCommand)
        output = self.cursor.fetchone()
        part = {'id': output[0],
                'categoryId': output[1],
                'name': output[2],
                'description': output[3],
                'amount': output[4]
                }
        return part, 201

    def delete(self):
        args = self.parser.parse_args()
        sqlCommand = "DELETE FROM parts WHERE id = " + str(args['id']) + ";"
        self.cursor.execute(sqlCommand)
        return 200

