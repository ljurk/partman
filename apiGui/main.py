from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QTableWidget, QTableWidgetItem, QTabWidget, QLineEdit, QLabel, QHeaderView, QTextEdit
import requests

host = 'http://localhost:5001/parts'
class apiGui:
    app = QApplication([])
    mainWindow = QMainWindow()
    tabWidget = QTabWidget()
    #output
    oWindow = QWidget()
    oTable = QTableWidget(0, 0)
    heading = oTable.horizontalHeader()
    oDebug = QTextEdit()
    oDebug.setReadOnly(True)
    oUrl = QLineEdit(host)
    #input
    iWindow = QWidget()
    iLayout = QVBoxLayout()
    iDebug = QTextEdit()
    iDebug.setReadOnly(True)
    iTable = QTableWidget(0, 0)
    def show(self):
        self.mainWindow.setWindowTitle("MAIN")

        self.showOutput()
        self.showInput()

        self.tabWidget.addTab(self.oWindow, "main")
        self.tabWidget.addTab(self.iWindow, "add")
        #self.tabWidget.currentChanged.connect(lambda:self.reloadInputs(self.oUrl.text()))
        self.tabWidget.show()
        self.app.exec_()

    def showOutput(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("URL"))
        layout.addWidget(self.oUrl)
        layout.addWidget(self.oTable)
        btnReload = QPushButton('reload')
        btnReload.clicked.connect(lambda:self.fillTable(self.oUrl.text()))
        layout.addWidget(btnReload)
        layout.addWidget(self.oDebug)

        self.oWindow.setLayout(layout)
    def showInput(self):
        self.iLayout.addWidget(QLabel("URL"))
        addURL = QLineEdit(host)
        self.iLayout.addWidget(addURL)
        btnSend = QPushButton('send')
        btnSend.clicked.connect(lambda:self.send(addURL.text()))
        self.iLayout.addWidget(btnSend)
        self.iLayout.addWidget(self.iDebug)
        self.iWindow.setLayout(self.iLayout)

    def log(self, text):
        self.oDebug.append(text)
        self.oDebug.show()
        self.iDebug.append(text)
        self.iDebug.show()

    def request(self, url):
        data = 0
        try:
            #data = requests.get(url).json()
            r = requests.get(url)
            r.raise_for_status()
            data = r.json()
        except requests.exceptions.HTTPError as errh:
            self.log("Http Error:"+str(errh))
        except requests.exceptions.ConnectionError as errc:
            self.log("Error Connecting:"+str(errc))
        except requests.exceptions.Timeout as errt:
            self.log("Timeout Error:"+str(errt))
        except requests.exceptions.RequestException as err:
            self.log("OOps: Something Else"+str(err))
        return data

    def clearLayout(self, layout):
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)
        return layout

    def fillTable(self, url):
        self.oTable.setRowCount(0)
        self.oTable.setColumnCount(0)
        self.oTable.clear()
        print(url)
        data = self.request(url)
        if data != 0:
            self.log("request ok")
            row = 0
            key = list(data.keys())[0]
            header = list(list(data.values())[0][0].keys())
            for d in data[key]:
                col = 0
                self.oTable.setRowCount(row + 1)
                for k in d.keys():
                    if row == 0:
                        self.oTable.setColumnCount(col + 1)
                        self.heading.setSectionResizeMode(col, QHeaderView.Stretch)
                        # or self.heading.setSectionResizeMode(col, QHeaderView.ResizeToContents)
                    self.oTable.setItem(row, col, QTableWidgetItem(d[k]))
                    col += 1
                row+=1
            self.oTable.setHorizontalHeaderLabels(header)


    def reloadInputs(self, url):
        #self.iLayout = QVBoxLayout()
        self.iLayout = self.clearLayout(self.iLayout)
        data = requests.get(url).json()
        row = 0
        key = list(data.keys())[0]
        header = list(list(data.values())[0][0].keys())
        for t in header:
            self.iLayout.addWidget(QLabel(t))
            self.iLayout.addWidget(QLineEdit())

        self.iWindow.setLayout(self.iLayout)

    def send(self, url):
        print(url)

    def add(args):
        if args.path == 'category':
            if args.name != None:
                r = requests.put(host + '/categories', data = {'name':args.name})
                print(r.text)
            elif args.csv != None:
                list = []
                with open(args.csv,'r') as f:
                    rows = csv.DictReader(f, delimiter=';')
                    for row in rows:
                        list.append(row)
                for l in list:
                    r = requests.put(host + '/categories', data = {'name':l['name']})
                    print(r.text)
        elif args.path == 'part':
            if args.name != None and args.categoryId != None and args.description != None:
                r = requests.put(host + '/parts', data = {'name':args.name, 'categoryId': args.categoryId, 'description': args.description})
            elif args.csv != None:
                list = []
                with open(args.csv,'r') as f:
                    rows = csv.DictReader(f, delimiter=';')
                    for row in rows:
                        list.append(row)
                for l in list:
                    r = requests.put(host + '/parts', data = {'name':l['name'], 'categoryId': l['categoryId'], 'description': l['description'], 'amount': l['amount']})
                    print(r.text)

if __name__ == '__main__':
    ex = apiGui()
    ex.fillTable(host)
    ex.show() 
