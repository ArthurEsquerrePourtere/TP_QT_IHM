import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Canvas import *
import resources


class MainWindow(QMainWindow):
    ##############
    def __init__(self,app):
        super().__init__()
        self.resize(640,480)
        self.createToolsBar()

        self.createPanel()
        
    def createPanel(self):
        mainContainer = QWidget()
        mainLayout = QHBoxLayout()
        
        #left
        self.textEdit = QTextEdit( self )
        mainLayout.addWidget(self.textEdit)
        
        #right
        rightLayout = QVBoxLayout()
        mainLayout.addLayout(rightLayout)
        
        clearButton = QPushButton( "Clear" )
        clearButton.clicked.connect(self.textEdit.clear)
        rightLayout.addWidget(clearButton )
        
        # progress
        self.progressBar = QProgressBar()
        self.progressBar.setRange(0,10)
        rightLayout.addWidget( self.progressBar)
        self.textEdit.textChanged.connect(self.updatePbar)
        
        # link
        mainContainer.setLayout(mainLayout)
        self.setCentralWidget( mainContainer )
        
    def updatePbar(self):
        self.progressBar.setValue(len(self.textEdit.toPlainText())%11)
    
    def createToolsBar(self):
        # Menu Bar
        bar = self.menuBar()
        fileMenu = bar.addMenu( "File" )
        # toolBar
        fileToolBar = self.addToolBar("File")
        
        # actions
        openAct = QAction(QIcon("open.png"), "Open..", self )
        openAct.setShortcut( QKeySequence("Ctrl+O" ) )
        openAct.setToolTip("OpenToolTip")
        openAct.setStatusTip("OpenStatus")
        openAct.triggered.connect(self.open)
        fileMenu.addAction(openAct)
        fileToolBar.addAction(openAct)
        
        saveAct = QAction(QIcon("save.png"), "Save..", self )
        fileMenu.addAction(saveAct)
        fileToolBar.addAction(saveAct)
        saveAct.triggered.connect(self.save)

        quitAct = QAction(QIcon("quit.png"), "Quit..", self )
        fileMenu.addAction(quitAct)
        fileToolBar.addAction(quitAct)
        quitAct.triggered.connect(self.quit)
      
        statusBar = self.statusBar()
        statusBar.showMessage("statusBar")

    ###############
    def open(self):
        print("Open...")
        fileName,_ = QFileDialog.getOpenFileName(self,"Open File")
        file = open(fileName,"r")
        self.textEdit.setHtml(file.read())
        print(fileName)
        file.close()
        
    ###############    
    def save(self):
        print("Save")		
        fileName,_ = QFileDialog.getSaveFileName(self,"Save File")
        text = self.textEdit.toHtml()
        file = open(fileName,"w")
        file.write(text)
        file.close()      
        print(fileName)
        
    ###############        
    def quit(self):
        print("Quit")		
        reply=QMessageBox.question(self, 'ATTENTION', "Do you want to close the application ?",QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
        if(reply==QMessageBox.Yes):
            QApplication.quit()
            
    def closeEvent(self,event):
        event.ignore()
        self.quit()


def main(args):
    app = QApplication(args)
    window = MainWindow(app)
    window.show()
    app.exec_()
	

if __name__ == "__main__":
	main(sys.argv) 