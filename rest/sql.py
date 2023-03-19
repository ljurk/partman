class Sql():
    connection = None
    cursor = None
    def getObjects(self, type, id):
        if type == 'parts':
            if id == 0:
                sqlCommand ='SELECT p.id,  c.name as category, p.name,  p.description, a.amount FROM parts as p LEFT JOIN amounts as a ON p.id=a.partid LEFT JOIN categories as c ON c.id = p.categoryId ORDER BY p.id DESC;'
            else:
                sqlCommand ='SELECT p.id,  c.name as category,p.name, p.description, a.amount FROM parts as p LEFT JOIN amounts as a ON p.id=a.partid LEFT JOIN categories as c ON c.id = p.categoryId WHERE p.id = ' + str(id) + 'ORDER BY p.id;'
        elif type == 'categories':
            sqlCommand= 'SELECT * FROM categories;'

        self.cursor.execute(sqlCommand)
        columns = [desc[0] for desc in self.cursor.description]
        output = self.cursor.fetchone()
        part={}
        parts=[]
        while output != None:
            for i in range(len(output)):
               part[columns[i]]= output[i]
            parts.append(part.copy())
            output = self.cursor.fetchone()
        return parts
