import sys
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QTabWidget, QLineEdit, QLabel, QHeaderView, QTextEdit, QMenuBar, QAction
import requests

DEBUG = False
host = 'http://localhost:5001/parts'
SEPERATOR = '##########################################'

#text styles
bold = 1
class apiGui(QMainWindow):
    def __init__(self, parent = None):
        super(apiGui, self).__init__(parent)
        self.setWindowTitle("apiGui by LJ")
        #vars
        self.centralWidget = QWidget()
        self.tabWidget = QTabWidget()
        self.debug = QTextEdit()
        self.debug.setReadOnly(True)
        self.url = QLineEdit(host)
        self.headers = []
        #output
        self.oWindow = QWidget()
        self.oTable = QTableWidget(0, 0)
        #output table is readonly
        self.oTable.setEditTriggers(QTableWidget.NoEditTriggers)
        #no row labels
        self.oTable.verticalHeader().setVisible(False)
        self.oLayout = QVBoxLayout()
        #input
        self.iWindow = QWidget()
        self.iLayout = QVBoxLayout()
        self.iTable = QTableWidget(0, 0)
        #no row labels
        self.iTable.verticalHeader().setVisible(False)
        
        #menu actions
        actionCsv = QAction("import csv", self)
        actionUrl = QAction("saved urls", self)
        actionQuit = QAction("quit", self)
        #create menu
        menuFile = self.menuBar().addMenu("FILE")
        menuFile.addAction(actionCsv)
        menuFile.addAction(actionUrl)
        menuFile.addAction(actionQuit)
        menuFile.triggered[QAction].connect(self.trigger)
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
        self.setCentralWidget(self.centralWidget)
        #add tabs
        self.tabWidget.addTab(self.oWindow, "main")
        self.tabWidget.addTab(self.iWindow, "add")
        self.tabWidget.currentChanged.connect(lambda:self.reload(self.url.text()))

        self.reload(self.url.text())

    #utility functions
    def log(self, text, option = 0):
        if option == bold:
            text = '<html><b>' + text + '</b></html>'
        self.debug.append(text)
        self.debug.show()

    def request(self, url, inputData = 0):
        #if there is inputData when its a put, otherwise a get
        data = 0
        try:
            if inputData == 0:
                r = requests.get(url)
            else:
                r = requests.put(url, inputData)
            r.raise_for_status()
            if inputData == 0:
                data = r.json()
            else:
                data = r
        except requests.exceptions.HTTPError as errh:
            self.log("Http Error:"+str(errh))
        except requests.exceptions.ConnectionError as errc:
            self.log("Error Connecting:"+str(errc))
        except requests.exceptions.Timeout as errt:
            self.log("Timeout Error:"+str(errt))
        except requests.exceptions.RequestException as err:
            self.log("OOps: Something Else"+str(err))
        return data
    
    def trigger(self, action):
        self.log(action.text())

    #gui functions
    def showOutput(self):
        #add Widgets to layout
        btnReload = QPushButton('load')
        btnReload.clicked.connect(lambda:self.fillOutputTable(self.oTable, self.url.text()))
        self.oLayout.addWidget(btnReload)
        self.oLayout.addWidget(self.oTable)
        #set layout
        self.oWindow.setLayout(self.oLayout)

    def showInput(self):
        #add Widgets to layout
        btnReload = QPushButton('load')
        btnReload.clicked.connect(lambda:self.fillInputTable(self.iTable, self.url.text()))
        self.iLayout.addWidget(btnReload)
        btnSend = QPushButton('send')
        btnSend.clicked.connect(lambda:self.send(self.url.text()))
        self.iLayout.addWidget(btnSend)
        self.iLayout.addWidget(self.iTable)
        #set layout
        self.iWindow.setLayout(self.iLayout)


    def reload(self, url):
        self.fillInputTable(self.iTable, url)
        self.fillOutputTable(self.oTable, url)

    def fillInputTable(self, table, url):
        # creates an table with columns based on the url and an empty row, ready for your inputs
        table.setRowCount(0)
        table.setColumnCount(0)
        table.clear()
        table.setRowCount(1)
        data = self.request(url)
        if data != 0:
            self.log("request ok")
            key = list(data.keys())[0]
            self.headers = list(list(data.values())[0][0].keys())
            col = 0
            for i in self.headers:
                table.setColumnCount(col + 1)
                table.horizontalHeader().setSectionResizeMode(col, QHeaderView.Stretch)
                cell = QTableWidgetItem("")
                #future
                cell.setCheckState(QtCore.Qt.Checked)
                table.setItem(0, col, cell)
                col += 1
            table.setHorizontalHeaderLabels(self.headers)

    def fillOutputTable(self, table, url):
        table.setRowCount(0)
        table.setColumnCount(0)
        table.clear()
        print(url)
        data = self.request(url)
        if data != 0:
            self.log("request ok")
            row = 0
            #get the key of first element because my api returns parts/[list]
            key = list(data.keys())[0]
            #get an array of the dict headers for naming the columns
            self.headers = list(list(data.values())[0][0].keys())
            for d in data[key]:
                col = 0
                table.setRowCount(row + 1)
                for k in d.keys():
                    if row == 0:
                        #only create the columns in first loop
                        table.setColumnCount(col + 1)
                        table.horizontalHeader().setSectionResizeMode(col, QHeaderView.Stretch)
                    if DEBUG:
                        self.log(str(d[k]) + str(type(d[k])))
                    table.setItem(row, col, QTableWidgetItem(str(d[k])))
                    col += 1
                row+=1
            table.setHorizontalHeaderLabels(self.headers)

    def send(self, url):
        self.log(SEPERATOR)
        self.log(SEPERATOR)
        self.log("send message:", bold)

        data = {}
        #fill data dict
        for i, val in enumerate(self.headers):
            #only add if checked
            self.log(str(self.iTable.item(0,i).checkState()))
            if self.iTable.item(0, i).checkState() == QtCore.Qt.Checked:
                data[val] = self.iTable.item(0, i).text()
        #print data dict, but with newlines
        self.log(str(data).replace(',',',\n').replace('{','{\n').replace('}','\n}'))
        #put request
        r = self.request(url, data)
        if r != 0:
            self.log(SEPERATOR)
            self.log("return message:", bold)
            self.log(r.text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = apiGui()
    ex.show()
    sys.exit(app.exec_())
