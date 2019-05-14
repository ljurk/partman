from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QTabWidget, QLineEdit, QLabel, QHeaderView, QTextEdit
import requests

host = 'http://localhost:5001/parts'
class apiGui:
    app = QApplication([])
    mainWindow = QMainWindow()
    centralWidget = QWidget()
    tabWidget = QTabWidget()
    debug = QTextEdit()
    debug.setReadOnly(True)
    url = QLineEdit(host)
    #output
    oWindow = QWidget()
    oTable = QTableWidget(0, 0)
    oLayout = QVBoxLayout()
    #input
    iWindow = QWidget()
    iLayout = QVBoxLayout()
    iTable = QTableWidget(0, 0)
    def show(self):
        self.mainWindow.setWindowTitle("MAIN")

        #generate layout of the tabs
        self.showOutput()
        self.showInput()
        #central
        hlayout = QHBoxLayout()
        hlayout.addWidget(QLabel("URL"))
        hlayout.addWidget(self.url)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(hlayout)
        mainLayout.addWidget(self.tabWidget)
        mainLayout.addWidget(self.debug)
        self.centralWidget.setLayout(mainLayout)
        self.mainWindow.setCentralWidget(self.centralWidget)
        #add tabs
        self.tabWidget.addTab(self.oWindow, "main")
        self.tabWidget.addTab(self.iWindow, "add")
        #self.tabWidget.currentChanged.connect(lambda:self.reloadInputs(self.url.text()))

        self.mainWindow.show()
        self.app.exec_()

    def showOutput(self):
        #add Widgets to layout
        btnReload = QPushButton('load')
        btnReload.clicked.connect(lambda:self.fillTable(self.oTable, self.url.text()))
        self.oLayout.addWidget(btnReload)
        self.oLayout.addWidget(self.oTable)
        #set layout
        self.oWindow.setLayout(self.oLayout)

    def showInput(self):
        #add Widgets to layout
        btnReload = QPushButton('load')
        btnReload.clicked.connect(lambda:self.fillTable(self.iTable, self.url.text()))
        self.iLayout.addWidget(btnReload)
        btnSend = QPushButton('send')
        btnSend.clicked.connect(lambda:self.send(addURL.text()))
        self.iLayout.addWidget(btnSend)
        self.iLayout.addWidget(self.iTable)
        #set layout
        self.iWindow.setLayout(self.iLayout)

    def log(self, text):
        self.debug.append(text)
        self.debug.show()

    def request(self, url):
        data = 0
        try:
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

    def fillTable(self, table, url):
        table.setRowCount(0)
        table.setColumnCount(0)
        table.clear()
        print(url)
        data = self.request(url)
        if data != 0:
            self.log("request ok")
            row = 0
            key = list(data.keys())[0]
            header = list(list(data.values())[0][0].keys())
            for d in data[key]:
                col = 0
                table.setRowCount(row + 1)
                for k in d.keys():
                    if row == 0:
                        table.setColumnCount(col + 1)
                        table.horizontalHeader().setSectionResizeMode(col, QHeaderView.Stretch)
                        # or self.heading.setSectionResizeMode(col, QHeaderView.ResizeToContents)
                    table.setItem(row, col, QTableWidgetItem(d[k]))
                    col += 1
                row+=1
            table.setHorizontalHeaderLabels(header)


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
    #ex.fillTable(.oTable, host)
    ex.show() 
