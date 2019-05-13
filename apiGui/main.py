from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QTableWidget, QTableWidgetItem, QTabWidget, QLineEdit, QLabel, QHeaderView, QTextEdit
import requests

host = 'http://localhost:5001/parts'
class apiGui:
    app = QApplication([])
    mainWindow = QMainWindow()
    window = QWidget()
    addwindow = QWidget()
    table = QTableWidget(0, 0)
    tabWidget = QTabWidget()
    heading = table.horizontalHeader()
    addlayout = QVBoxLayout()
    debugWindow = QTextEdit()
    debugWindow.setReadOnly(True)
    def show(self):
        self.mainWindow.setWindowTitle("MAIN")

        #main
        layout = QVBoxLayout()
        layout.addWidget(QLabel("URL"))
        mainURL = QLineEdit(host)
        layout.addWidget(mainURL)
        layout.addWidget(self.table)
        btnReload = QPushButton('reload')
        btnReload.clicked.connect(lambda:self.fillTable(mainURL.text()))
        layout.addWidget(btnReload)
        self.debugWindow.setText("show success")
        self.debugWindow.append("show success")
        self.debugWindow.show()
        layout.addWidget(self.debugWindow)

        self.window.setLayout(layout)

        #add
        self.addlayout.addWidget(QLabel("URL"))
        addURL = QLineEdit(host)
        self.addlayout.addWidget(addURL)
        btnSend = QPushButton('send')
        btnSend.clicked.connect(lambda:self.send(addURL.text()))
        self.addlayout.addWidget(btnSend)
        self.addwindow.setLayout(self.addlayout)

        self.tabWidget.addTab(self.window, "main")
        self.tabWidget.addTab(self.addwindow, "add")
        self.tabWidget.currentChanged.connect(lambda:self.reloadInputs(mainURL.text()))
        self.tabWidget.show()
        self.app.exec_()

    def log(self, text):
        self.debugWindow.append(text)
        self.debugWindow.show()

    def clearLayout(self, layout):
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)
        return layout

    def fillTable(self, url):
        self.table.setRowCount(0)
        self.table.setColumnCount(0)
        self.table.clear()
        print(url)
        data=0
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

        if data != 0:
            self.log("request ok")
            row = 0
            key = list(data.keys())[0]
            header = list(list(data.values())[0][0].keys())
            for d in data[key]:
                col = 0
                self.table.setRowCount(row + 1)
                for k in d.keys():
                    if row == 0:
                        self.table.setColumnCount(col + 1)
                        self.heading.setSectionResizeMode(col, QHeaderView.Stretch)
                        # or self.heading.setSectionResizeMode(col, QHeaderView.ResizeToContents)
                    self.table.setItem(row, col, QTableWidgetItem(d[k]))
                    col += 1
                row+=1
            self.table.setHorizontalHeaderLabels(header)


    def reloadInputs(self, url):
        #self.addlayout = QVBoxLayout()
        self.addlayout = self.clearLayout(self.addlayout)
        data = requests.get(url).json()
        row = 0
        key = list(data.keys())[0]
        header = list(list(data.values())[0][0].keys())
        for t in header:
            self.addlayout.addWidget(QLabel(t))
            self.addlayout.addWidget(QLineEdit())

        self.addwindow.setLayout(self.addlayout)

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
