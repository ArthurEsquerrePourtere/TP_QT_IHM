import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtChart import *
from Canvas import *
import resources


class MainWindow(QMainWindow):
    

    def __init__(self, parent = None ):
        super().__init__()
        print( "init mainwindow")
        self.resize(1000, 850)

        bar = self.menuBar()
        fileMenu = bar.addMenu("File")
        # actions
        openAct = QAction(QIcon("open.png"), "Open..", self )
        openAct.setShortcut( QKeySequence("Ctrl+O" ) )
        openAct.setToolTip("OpenToolTip")
        openAct.setStatusTip("OpenStatus")
        openAct.triggered.connect(self.open)
        fileMenu.addAction(openAct)
        
        saveAct = QAction(QIcon("save.png"), "Save..", self )
        fileMenu.addAction(saveAct)
        saveAct.triggered.connect(self.save)
        
        quitAct = QAction(QIcon("quit.png"), "Quit..", self )
        fileMenu.addAction(quitAct)
        quitAct.triggered.connect(self.quit)

        colorMenu = bar.addMenu("Color")
        actPen = colorMenu.addAction(QIcon(":/icons/pen.png"), "&Pen color", self.pen_color, QKeySequence("Ctrl+P"))
        actBrush = colorMenu.addAction(QIcon(":/icons/brush.png"), "&Brush color", self.brush_color, QKeySequence("Ctrl+B"))

        colorToolBar = QToolBar("Color")
        self.addToolBar( colorToolBar )
        colorToolBar.addAction( actPen )
        colorToolBar.addAction( actBrush )

        thicknessMenu = bar.addMenu("Thickness")
        actMoreThick = thicknessMenu.addAction(QIcon("plus.png"),"More thick", self.moreThick)
        actLessThick = thicknessMenu.addAction(QIcon("minus.png"),"Less thick", self.lessThick)
        
        thicknessToolBar = QToolBar("Thickness")
        self.addToolBar( thicknessToolBar )
        thicknessToolBar.addAction( actMoreThick )
        thicknessToolBar.addAction( actLessThick )

        shapeMenu = bar.addMenu("Shape")
        actRectangle = shapeMenu.addAction(QIcon(":/icons/rectangle.png"), "&Rectangle", self.rectangle )
        actEllipse = shapeMenu.addAction(QIcon(":/icons/ellipse.png"), "&Ellipse", self.ellipse)
        #actFree = shapeMenu.addAction(QIcon(":/icons/free.png"), "&Free drawing", self.free_drawing)

        shapeToolBar = QToolBar("Shape")
        self.addToolBar( shapeToolBar )
        shapeToolBar.addAction( actRectangle )
        shapeToolBar.addAction( actEllipse )
        #shapeToolBar.addAction( actFree )

        modeMenu = bar.addMenu("Mode")
        actMove = modeMenu.addAction(QIcon(":/icons/move.png"), "&Move", self.move)
        actDraw = modeMenu.addAction(QIcon(":/icons/draw.png"), "&Draw", self.draw)
        actSelect = modeMenu.addAction(QIcon(":/icons/select.png"), "&Select", self.select)
        actLasso = modeMenu.addAction(QIcon("lasso.png"),"&Lasso", self.lasso)

        modeToolBar = QToolBar("Navigation")
        self.addToolBar( modeToolBar )
        modeToolBar.addAction( actMove )
        modeToolBar.addAction( actDraw )
        modeToolBar.addAction( actSelect )
        modeToolBar.addAction( actLasso )

        zoomMenu = bar.addMenu("Zoom")
        actZoomIn = zoomMenu.addAction(QIcon(":/icons/zoom-in.png"),"Zoom in", self.zoomIn)
        actZoomOut = zoomMenu.addAction(QIcon(":/icons/zoom-out.png"),"Zoom out", self.zoomOut)
        
        zoomToolBar = QToolBar("Zoom")
        self.addToolBar( zoomToolBar )
        zoomToolBar.addAction( actZoomIn )
        zoomToolBar.addAction( actZoomOut )
        
        deleteMenu = bar.addMenu("Delete")
        actMove = deleteMenu.addAction(QIcon("undo.png"),"Delete last shape", self.delete)
        actDraw = deleteMenu.addAction(QIcon("trash.png"),"Delete all", self.deleteAll)

        mainContainer = QWidget()
        mainLayout = QHBoxLayout()
        
        #left
        leftLayout = QVBoxLayout()
        mainLayout.addLayout(leftLayout)
        
        #up
        self.textEdit = QTextEdit( self )
        leftLayout.addWidget(self.textEdit)

        #down
        self.canvas = Canvas()
        self.canvas.action.connect(self.get_action)
        leftLayout.addWidget(self.canvas)
        
        #right
        rightLayout = QVBoxLayout()
        
        self.shapesNb=[(0,0)]
        self.createShapeChart()
        rightLayout.addWidget(QChartView(self.charts[0]))
        
        self.buttonNumber=[0]*4
        self.createButtonChart()
        rightLayout.addWidget(QChartView(self.charts[1]))
        mainLayout.addLayout(rightLayout)

        # link
        mainContainer.setLayout(mainLayout)
        self.setCentralWidget( mainContainer )


    ##############
    def createShapeChart(self):
        self.charts = [QChart()]
        self.charts[0].setTitle("Number of each shape after each action")
        
        lineRect = QLineSeries()
        lineRect.setName("Rectangle")
        pen=QPen(QColor("#fdc086"))
        pen.setWidth(5)
        lineRect.setPen(pen)
        
        lineEllipse = QLineSeries()
        lineEllipse.setName("Ellipse")
        pen=QPen(QColor("#7fc97f"))
        pen.setWidth(5)
        lineEllipse.setPen(pen)
        
        lineTotal = QLineSeries()
        lineTotal.setName("Total")
        pen=QPen(Qt.black)
        pen.setWidth(5)
        lineTotal.setPen(pen)
        
        for i in range(len(self.shapesNb)):
            lineRect << QPoint(i,self.shapesNb[i][0])
            lineEllipse << QPoint(i,self.shapesNb[i][1])
            lineTotal << QPoint(i,self.shapesNb[i][0]+self.shapesNb[i][1])
        
        self.charts[0].legend().hide()
        self.charts[0].addSeries(lineRect)
        self.charts[0].addSeries(lineEllipse)
        self.charts[0].addSeries(lineTotal)
        self.charts[0].createDefaultAxes()
        self.charts[0].axisX().setRange(0,1)
        self.charts[0].axisY().setRange(0,1)
        self.charts[0].axisY().setTitleText("Number of each shape")
        self.charts[0].axisX().setTitleText("Action")
        self.charts[0].setAnimationOptions(QChart.SeriesAnimations)
        
        self.charts[0].legend().setVisible(True)
        self.charts[0].legend().setAlignment(Qt.AlignBottom)
        
    def createButtonChart(self):
        self.charts.append(QChart())
        self.charts[1].setTitle("Mode button use")
            
        setMove= QBarSet("Move")
        setDraw= QBarSet("Draw")
        setSelect= QBarSet("Select")
        setLasso= QBarSet("Lasso")
        
        setMove.append(self.buttonNumber[0])
        setDraw.append(self.buttonNumber[1])
        setSelect.append(self.buttonNumber[2])
        setLasso.append(self.buttonNumber[3])
        
        series = QBarSeries()
        
        series.append(setMove)
        series.append(setDraw)
        series.append(setSelect)
        series.append(setLasso)
        
        self.charts[1].legend().hide()
        self.charts[1].addSeries(series)
        self.charts[1].createDefaultAxes()
        self.charts[1].axisY().setRange(0,max(self.buttonNumber))
        self.charts[1].axisX().setVisible(False)
        self.charts[1].setAnimationOptions(QChart.SeriesAnimations)
        self.charts[1].axisY().setTitleText("Number of click")
        
        self.charts[1].legend().setVisible(True)
        self.charts[1].legend().setAlignment(Qt.AlignBottom)
        
    def updateShapeChart(self):
        self.charts[0].removeAllSeries()

        lineRect = QLineSeries()
        lineRect.setName("Rectangle")
        pen=QPen(QColor("#fdc086"))
        pen.setWidth(5)
        lineRect.setPen(pen)
        
        lineEllipse = QLineSeries()
        lineEllipse.setName("Ellipse")
        pen=QPen(QColor("#7fc97f"))
        pen.setWidth(5)
        lineEllipse.setPen(pen)
        
        lineTotal = QLineSeries()
        lineTotal.setName("Total")
        pen=QPen(Qt.black)
        pen.setWidth(5)
        lineTotal.setPen(pen)
        
        total=[]
        for i in range(len(self.shapesNb)):
            lineRect << QPoint(i,self.shapesNb[i][0])
            lineEllipse << QPoint(i,self.shapesNb[i][1])
            total.append(self.shapesNb[i][0]+self.shapesNb[i][1])
            lineTotal << QPoint(i,total[i])
    
        
        self.charts[0].addSeries(lineRect)
        self.charts[0].addSeries(lineEllipse)
        self.charts[0].addSeries(lineTotal)
        self.charts[0].createDefaultAxes()
        self.charts[0].axisX().setRange(0,i)
        self.charts[0].axisY().setRange(0,max(total))
        self.charts[0].axisY().setTitleText("Number of each shape")
        self.charts[0].axisX().setTitleText("Action")
        
        
    def updateNbShape(self):
        rect=0
        ellipse=0
        for shape in self.canvas.shapes:
            if(shape[0]=="rect"):
                rect+=1
            else:
                ellipse+=1
        self.shapesNb.append((rect,ellipse))
        self.updateShapeChart()
        
    def updateButtonChart(self):
        self.charts[1].removeAllSeries()
        
        setMove= QBarSet("Move")
        setDraw= QBarSet("Draw")
        setSelect= QBarSet("Select")
        setLasso= QBarSet("Lasso")
        
        setMove.append(self.buttonNumber[0])
        setDraw.append(self.buttonNumber[1])
        setSelect.append(self.buttonNumber[2])
        setLasso.append(self.buttonNumber[3])
        
        series = QBarSeries()
        
        series.append(setMove)
        series.append(setDraw)
        series.append(setSelect)
        series.append(setLasso)
        self.charts[1].addSeries(series)
        self.charts[1].axisY().setRange(0,max(self.buttonNumber))
    
    def pen_color(self):
        color = QColorDialog.getColor()
        if (color.isValid()):
            self.log_action("choose pen color : "+color.name())
            self.canvas.contourColor=QPen(color)
            for i in self.canvas.selectedShape:
                if (self.canvas.mode=="select" or self.canvas.mode=="lasso"):
                    self.canvas.shapes[i][4]=QPen(color)
                    self.canvas.update()

    def brush_color(self):
        color = QColorDialog.getColor()
        if (color.isValid()):
            self.log_action("choose brush color : "+color.name())
            self.canvas.backgroundColor=color
            for i in self.canvas.selectedShape:
                if (self.canvas.mode=="select" or self.canvas.mode=="lasso"):
                    self.canvas.shapes[i][3]=color
                    self.canvas.update()

    def moreThick(self):
        self.log_action("Thickness : More")
        self.canvas.contourThickness+=1
        for i in self.canvas.selectedShape:
            if (self.canvas.mode=="select" or self.canvas.mode=="lasso"):
                self.canvas.shapes[i][5]+=1
                self.canvas.update()

    def lessThick(self):
        self.log_action("Thickness : Less")
        self.canvas.contourThickness-=1
        for i in self.canvas.selectedShape:
            if (self.canvas.mode=="select" or self.canvas.mode=="lasso"):
                self.canvas.shapes[i][5]-=1
                self.canvas.update()

    def rectangle(self):
        self.log_action("Shape mode: rectangle")
        self.canvas.shape="rect"
        if (self.canvas.mode=="select" or self.canvas.mode=="lasso"):
            for i in self.canvas.selectedShape:
                self.canvas.shapes[i][0]="rect"
                self.canvas.update()
            self.updateNbShape()
        else:
            self.draw(True)

    def ellipse(self):
        self.log_action("Shape Mode: circle")
        self.canvas.shape="circle"
        if (self.canvas.mode=="select" or self.canvas.mode=="lasso"):
            for i in self.canvas.selectedShape:
                self.canvas.shapes[i][0]="circle"
                self.canvas.update()
            self.updateNbShape()
        else:
            self.draw(True)

    def free_drawing(self):
        self.log_action("Shape mode: free drawing")

    def move(self):
        self.log_action("Mode: move")
        self.buttonNumber[0]+=1
        self.updateButtonChart()
        self.canvas.selectedShape=[]
        self.canvas.lassoPoints=[]
        self.canvas.mode="move"
        self.canvas.update()

    def draw(self,auto=False):
        self.log_action("Mode: draw")
        if(auto==False):
            self.buttonNumber[1]+=1
            self.updateButtonChart()
        self.canvas.selectedShape=[]
        self.canvas.lassoPoints=[]
        self.canvas.mode="draw"
        self.canvas.update()

    def select(self):
        self.log_action("Mode: select")
        self.buttonNumber[2]+=1
        self.updateButtonChart()
        self.canvas.selectedShape=[]
        self.canvas.lassoPoints=[]
        self.canvas.mode="select"
        self.canvas.update()
        
    def lasso(self):
        self.log_action("Mode: lasso")
        self.buttonNumber[3]+=1
        self.updateButtonChart()
        self.canvas.selectedShape=[]
        self.canvas.lassoPoints=[]
        self.canvas.mode="lasso"
        self.canvas.update()
        
    def delete(self):
        self.log_action("Mode: delete last shape")
        self.canvas.shapes.pop()
        self.canvas.reset()
        
    def deleteAll(self):
        self.log_action("Mode: delete all")
        self.canvas.shapes=[]
        self.canvas.reset()

    def zoomIn(self):
        self.log_action("Zoom in")
        self.canvas.scale*=1.2
        self.canvas.update()

    def zoomOut(self):
        self.log_action("Zoom out")
        self.canvas.scale/=1.2
        self.canvas.update()
        
    def get_action(self, str):
        if(str!="updateChart"):
            self.log_action(str)
        else:
            self.updateNbShape()

    def log_action(self, str):
        content = self.textEdit.toPlainText()
        self.textEdit.setPlainText( content + "\n" + str)
       
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
