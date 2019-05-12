from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QTableWidget, QTableWidgetItem, QTabWidget, QLineEdit, QLabel
import requests

host = 'http://localhost:5001/parts'
class apiGui:
    app = QApplication([])
    mainWindow = QMainWindow()
    window = QWidget()
    addwindow = QWidget()
    table = QTableWidget(0, 0)
    tabWidget = QTabWidget()
    text = QLineEdit(host)
    addlayout = QVBoxLayout()
    def show(self):
        self.mainWindow.setWindowTitle("MAIN")

        #main
        layout = QVBoxLayout()
        layout.addWidget(QLabel("URL"))
        layout.addWidget(self.text)
        layout.addWidget(self.table)
        btnReload = QPushButton('reload')
        btnReload.clicked.connect(lambda:self.fillTable(self.text.text()))
        layout.addWidget(self.btnReload)
        self.window.setLayout(layout)

        #add
        self.addlayout.addWidget(QLabel("URL"))
        self.addlayout.addWidget(self.text)
        btnSend = QPushButton('send')
        btnReload.clicked.connect(lambda:self.send(self.text.text()))
        self.addlayout.addWidget(btnSend)
        self.addwindow.setLayout(self.addlayout)

        self.tabWidget.addTab(self.window, "main")
        self.tabWidget.addTab(self.addwindow, "add")
        self.tabWidget.currentChanged.connect(lambda:self.reloadInputs(self.text.text()))
        self.tabWidget.show()
        self.app.exec_()

    def fillTable(self, url):
        self.table.setRowCount(0)
        self.table.setColumnCount(0)
        self.table.clear()

        data = requests.get(url).json()
        row = 0
        key = list(data.keys())[0]
        header = list(list(data.values())[0][0].keys())
        for d in data[key]:
            col = 0
            self.table.setRowCount(row + 1)
            for k in d.keys():
                if row == 0:
                    self.table.setColumnCount(col + 1)
                self.table.setItem(row, col, QTableWidgetItem(d[k]))
                col += 1
            row+=1

        self.table.setHorizontalHeaderLabels(header)
    def reloadInputs(self, url):
        #self.addlayout = QVBoxLayout()
        data = requests.get(url).json()
        row = 0
        key = list(data.keys())[0]
        header = list(list(data.values())[0][0].keys())
        for t in header:
            self.addlayout.addWidget(QLabel(t))
            self.addlayout.addWidget(QLineEdit())

        self.addwindow.setLayout(self.addlayout)

    def send(self, url):


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
