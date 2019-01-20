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
        if args['name'] != None:
            sqlCommand = "INSERT INTO parts(name) VALUES('" + args['name'] + "')"
            #sqlCommand = "INSERT INTO parts(categoryId,name,description) VALUES(" + str(args['categoryId']) + ",'" + args['name'] + "','" + args['description']+"')"
            self.cursor.execute(sqlCommand)
            self.connection.commit()

            #get new id
            self.cursor.execute("SELECT id FROM parts ORDER BY id DESC LIMIT 1;")
            newestId = self.cursor.fetchone()[0]
            #set categoryId if set
            if args['categoryId'] != None:
                sqlCommand = "UPDATE parts SET categoryId=" + str(args['categoryId']) + " WHERE id ="+str(newestId)+";"
                self.cursor.execute(sqlCommand)
                self.connection.commit()

            #set description if set
            if args['description'] != None:
                sqlCommand = "UPDATE parts SET description='" + str(args['description']) + "' WHERE id ="+str(newestId)+";"
                self.cursor.execute(sqlCommand)
                self.connection.commit()

            #set amount if set
            if args['amount'] != None:
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
        self.connection.commit()
        return 200

    def patch(self):
        args = self.parser.parse_args()
        if args['id'] != None:
            if args['name'] != None:
                sqlCommand = "UPDATE parts SET name='" + str(args['name']) + "' WHERE id = " + str(args['id']) + ";"
                self.cursor.execute(sqlCommand)
                self.connection.commit()
            if args['description'] != None:
                sqlCommand = "UPDATE parts SET description='" + str(args['description']) + "' WHERE id = " + str(args['id']) + ";"
                self.cursor.execute(sqlCommand)
                self.connection.commit()
            if args['categoryId'] != None:
                sqlCommand = "UPDATE parts SET categoryId=" + str(args['categoryId']) + " WHERE id = " + str(args['id']) + ";"
                self.cursor.execute(sqlCommand)
                self.connection.commit()
            if args['amount'] != None:
                sqlCommand ="SELECT COUNT(*) FROM amounts WHERE partid="+str(args['id'])+";"
                self.cursor.execute(sqlCommand)
                count = self.cursor.fetchone()[0]
                if count == 0:
                    sqlCommand = "INSERT INTO amounts(partid,amount) VALUES(" + str(args['id']) + ","+str(args['amount']) + ");"
                else:
                    sqlCommand = "UPDATE amounts SET amount=" + str(args['amount']) + " WHERE partid = " + str(args['id']) + ";"
                self.cursor.execute(sqlCommand)
                self.connection.commit()

            #read new entry
            sqlCommand ='SELECT p.id, c.name,p.name, p.description, a.amount FROM parts as p LEFT JOIN amounts as a ON p.id=a.partid LEFT JOIN categories as c ON c.id = p.categoryId WHERE p.id =' + str(args['id']) + ';'
            self.cursor.execute(sqlCommand)
            output = self.cursor.fetchone()
            part = {'id': output[0],
                    'categoryId': output[1],
                    'name': output[2],
                    'description': output[3],
                    'amount': output[4]
                    }
            return part, 200
        else:
            return "no input",200

