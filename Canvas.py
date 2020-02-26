from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import copy


class Canvas(QWidget):
    
    action=pyqtSignal(str)

    def __init__(self, parent = None):
        super().__init__()
        print("class Canvas")
        self.setMinimumSize(300,500)
        self.pStart=QPoint()
        self.pEnd=QPoint()
        self.backgroundColor=QColor(Qt.gray)
        self.shape="rect"
        self.contourColor=QPen(Qt.black)
        self.contourThickness=5
        self.shapes=[]
        self.mode="draw"
        self.selectedShape=[]
        self.scale=1
        self.lassoPoints=[]
        self.menuDisplayed=None

    def reset(self):
        self.pStart=QPoint()
        self.pEnd=QPoint()
        self.selectedShape=[]
        self.lassoPoints=[]
        self.update()
        self.action.emit("updateChart")

    def add_object(self):
        print("add object")

    def set_color(self, color ):
        print("set color")

    def updateCoordinates(self):
        for shape in self.shapes:
            shape[1].setX(shape[1].x()+(self.pEnd.x()-self.pStart.x())/self.scale)
            shape[1].setY(shape[1].y()+(self.pEnd.y()-self.pStart.y())/self.scale)
            shape[2].setX(shape[2].x()+(self.pEnd.x()-self.pStart.x())/self.scale)
            shape[2].setY(shape[2].y()+(self.pEnd.y()-self.pStart.y())/self.scale)

    def selectShape(self,event):
        for i in range(-1,-len(self.shapes)-1,-1):
            shape=self.shapes[i]
            if(shape[0]=="rect"):
                Qshape=QRect(shape[1].x()*self.scale,shape[1].y()*self.scale,shape[2].x()*self.scale-shape[1].x()*self.scale,shape[2].y()*self.scale-shape[1].y()*self.scale)
            elif(shape[0]=="circle"):
                Qshape=QRegion(QRect(shape[1].x()*self.scale,shape[1].y()*self.scale,shape[2].x()*self.scale-shape[1].x()*self.scale,shape[2].y()*self.scale-shape[1].y()*self.scale), QRegion.Ellipse) 
            if (Qshape.contains(event.pos())):
                self.shapes.append(self.shapes.pop(i+len(self.shapes)))          
                self.selectedShape=[len(self.shapes)-1]
                break
            

    def mousePressEvent(self, event): # evenement mousePress
        self.action.emit("Press : "+str(event.pos().x())+" , "+str(event.pos().y()))
        self.pStart = event.pos()
        self.pEnd = event.pos()
        if (self.mode=="select"):
            self.selectShape(event)
            self.update()
        elif (self.mode=="lasso"):
            if(self.lassoPoints==[]):
                self.selectedShape=[]
                self.lassoPoints.append(event.pos())
            else:
                self.lassoPoints.append(event.pos())
            self.update()
            

    def mouseReleaseEvent(self, event): # evenement mouseRelease
        self.action.emit("Release : "+str(event.pos().x())+" , "+str(event.pos().y()))
        self.pEnd = event.pos()
        if (self.mode=="lasso"):
            polygon=QPolygon(self.lassoPoints+[self.lassoPoints[0]])
            for i in range(-1,-len(self.shapes)-1,-1):
                shape=self.shapes[i]
                rectShape=QRect(shape[1].x()*self.scale,shape[1].y()*self.scale,shape[2].x()*self.scale-shape[1].x()*self.scale,shape[2].y()*self.scale-shape[1].y()*self.scale)
                if(polygon.containsPoint(rectShape.center(),Qt.OddEvenFill)):
                    self.shapes.append(self.shapes.pop(i+len(self.shapes))) 
                    for i in range(len(self.selectedShape)):                        
                        self.selectedShape[i]-=1
                    self.selectedShape.append(len(self.shapes)-1)
            self.hideLoopMenu()
            self.lassoPoints=[]
        if (self.mode=="draw"):
            self.shapes.append([self.shape,self.pStart/self.scale,self.pEnd/self.scale,self.backgroundColor,self.contourColor,self.contourThickness])
            self.action.emit("updateChart")
        self.update()
        if (self.mode=="move"):
            self.updateCoordinates()
        self.pStart = event.pos()
        self.pEnd = event.pos()

    def mouseMoveEvent(self, event): # evenement mouseMove
        self.action.emit("Move : "+str(event.pos().x())+" , "+str(event.pos().y()))
        self.pEnd = event.pos() # on stocke la position du curseur
        if (self.mode=="lasso"):
            if(self.menuDisplayed==None):
                self.detectLoop(event)
            self.lassoPoints.append(event.pos())
        self.update()
        
    def detectLoop(self,event):
        isLoop=False
        if(len(self.lassoPoints)>15):
#            line=QLineF(self.lassoPoints[-1],event.pos())
#            for polyPoint in range(len(self.lassoPoints)-15):
#                otherLine=QLineF(self.lassoPoints[polyPoint],self.lassoPoints[polyPoint+1])
#                intersection=QPoint(0,0)
#                print(otherLine.intersect(line,intersection))
#                print("coord : ",intersection.x())
#                if (otherLine.intersect(line,intersection)==0):
#                    isLoop=True
            for polyPoint in self.lassoPoints[:-10]:
                point = event.pos() - polyPoint
                if (point.manhattanLength() < 5):
                #if (event.pos().x()==polyPoint.x() and event.pos().y()==polyPoint.y()):
                    isLoop=True
        if(isLoop):
            self.displayLoopMenu(event)
            
    def displayLoopMenu(self,event):
        self.menuDisplayed=event.pos()
        print("affiche menu")
        
    def hideLoopMenu(self):
        self.menuDisplayed=None
        print("Cache menu")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.scale(self.scale,self.scale)
        if (self.mode=="move"):
            painter.translate(self.pEnd.x()/self.scale-self.pStart.x()/self.scale,self.pEnd.y()/self.scale-self.pStart.y()/self.scale)
        for i in range(len(self.shapes)):
            shape=self.shapes[i]
            if((self.mode=="select" or self.mode=="lasso") and i in self.selectedShape):
                pen = QPen(Qt.red)
            else:
                pen = shape[4]
            pen.setWidth(shape[5])
            painter.setPen(pen)
            painter.setBrush(shape[3])
            if (shape[0]=="rect"):    		
                	painter.drawRect(shape[1].x(),shape[1].y(),shape[2].x()-shape[1].x(),shape[2].y()-shape[1].y())
            elif(shape[0]=="circle"):
                painter.drawEllipse(shape[1].x(),shape[1].y(),shape[2].x()-shape[1].x(),shape[2].y()-shape[1].y())
        if (self.mode=="draw"):
            pen = self.contourColor
            pen.setWidth(self.contourThickness)
            painter.setPen(pen)
            painter.setBrush(self.backgroundColor)
            if (self.shape=="rect"):    		
                painter.drawRect(self.pStart.x()/self.scale,self.pStart.y()/self.scale,self.pEnd.x()/self.scale-self.pStart.x()/self.scale,self.pEnd.y()/self.scale-self.pStart.y()/self.scale)
            elif(self.shape=="circle"):
                painter.drawEllipse(self.pStart.x()/self.scale,self.pStart.y()/self.scale,self.pEnd.x()/self.scale-self.pStart.x()/self.scale,self.pEnd.y()/self.scale-self.pStart.y()/self.scale)
        if (self.mode=="lasso"):
            for i in range(len(self.lassoPoints)-1):
                pen = QPen(Qt.red)
                pen.setWidth(5/self.scale)
                painter.setPen(pen)
                painter.drawLine(self.lassoPoints[i]/self.scale,self.lassoPoints[i+1]/self.scale)
            if(self.menuDisplayed!=None):
                pen = QPen(Qt.black)
                pen.setWidth(3/self.scale)
                painter.setPen(pen)
                arrowSize=40
                painter.drawLine(self.menuDisplayed/self.scale,QPoint((self.menuDisplayed.x()+arrowSize)/self.scale,self.menuDisplayed.y()/self.scale))
                painter.drawLine(self.menuDisplayed/self.scale,QPoint((self.menuDisplayed.x()-arrowSize)/self.scale,self.menuDisplayed.y()/self.scale))
                painter.drawLine(self.menuDisplayed/self.scale,QPoint((self.menuDisplayed.x())/self.scale,(self.menuDisplayed.y()+arrowSize)/self.scale))
                painter.drawLine(self.menuDisplayed/self.scale,QPoint((self.menuDisplayed.x())/self.scale,(self.menuDisplayed.y()-arrowSize)/self.scale))
