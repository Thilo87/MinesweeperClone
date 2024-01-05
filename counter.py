# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 08:45:17 2023

@author: AMD
"""

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import math

"""

Class for a display with graphical digits. You can set the number with Counter.number and the width with
Counter.width. Or you can start/stop a count-up with Counter.start/Counter.stop.

"""
class Counter(QGraphicsView):
    # height and width of the digit-images
    _IMG_HEIGHT = 23
    _IMG_WIDTH = 13
    
    _IMG_DIGIT_PATHS = ["img/counter_0.png",\
                          "img/counter_1.png",\
                          "img/counter_2.png",\
                          "img/counter_3.png",\
                          "img/counter_4.png",\
                          "img/counter_5.png",\
                          "img/counter_6.png",\
                          "img/counter_7.png",\
                          "img/counter_8.png",\
                          "img/counter_9.png"]
        
    _DEFAULT_WIDTH = 3
    _DEFAULT_NUMBER = 0
        
    def __init__(self, name, parent=None):
        super(QGraphicsView,self).__init__(parent)
        
        self._number = self._DEFAULT_NUMBER     # current number to display
        self._width = self._DEFAULT_WIDTH       # number of the digits to display, e.g. 4 for 1234, 3 for 123, ...
        
        self._timer = QTimer(self)              # timer for countdown/-up
        self._timer.timeout.connect(self._on_timer_timeout)
        
        self.setMaximumHeight(self._IMG_HEIGHT)
        self.setMinimumHeight(self._IMG_HEIGHT)
        self.setMaximumWidth(self._IMG_WIDTH * self._width)
        self.setMinimumWidth(self._IMG_WIDTH * self._width)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setFrameShape(QFrame.NoFrame)
        
        self.graphicsScene = QGraphicsScene(0, 0, self._IMG_WIDTH * self._width, self._IMG_HEIGHT)
        self.setScene(self.graphicsScene)
        
        self._update()
        
    def _on_timer_timeout(self):
        self._number += 1
        self._update()
        
    # update visual digits
    def _update(self):
        self.graphicsScene.clear()
        
        if self._number <= 0:
            num_digits = 0
        else:
            num_digits = int(math.floor(math.log10(self._number))+1) # e.g. 4 for 1234, 3 for 123, 3 for 999, ...
            
        if num_digits > self._width:
            num_digits = self._width
            
        if self._number < 0:
            number_cpy = 0
        else:
            number_cpy = self._number
            
        # display the digits of the number_cpy in the graphics view. Begin with the last digit, e.g. 4
        # of 1234. Then draw the 3, the 2, and then the 1.
        for i in range(0, num_digits):
            digit = number_cpy % 10 # get the last digit from number_cpy
            number_cpy = int(math.floor(number_cpy / 10)) # remove the last digit from number_cpy
            
            image = QGraphicsPixmapItem(QPixmap(self._IMG_DIGIT_PATHS[digit]))
            image.setPos(self._IMG_WIDTH * self._width - (i+1)*self._IMG_WIDTH, 0)
            self.graphicsScene.addItem(image)
            
        # if the number has fewer digits than the width of the display, fill the places to the left
        # with zeros
        if num_digits < self._width:
            for i in range(0, self._width - num_digits):
                image = QGraphicsPixmapItem(QPixmap(self._IMG_DIGIT_PATHS[0]))
                image.setPos(self._IMG_WIDTH * self._width - (i+1+num_digits)*self._IMG_WIDTH, 0)
                self.graphicsScene.addItem(image)
        
    # called when a user has changed the width
    def _update_width(self):
        self.setMaximumWidth(self._IMG_WIDTH * self._width)
        self.setMinimumWidth(self._IMG_WIDTH * self._width)
        
        self.graphicsScene = QGraphicsScene(0, 0, self._IMG_WIDTH * self._width, self._IMG_HEIGHT)
        self.setScene(self.graphicsScene)
        
        self._update()
        
    # starts the count-up
    def start(self):
        self._timer.start(1000)
    
    # stops the count-up
    def stop(self):
        self._timer.stop()
        
    @property
    def number(self):
        return self._number
    
    @number.setter
    def number(self, a):
        if type(a) != int:
            raise TypeError("Only integers allowed!")
            
        self._number = a
        self._update()
        
    @property
    def width(self):
        return self._width
    
    @width.setter
    def width(self, a):
        if type(a) != int:
            raise TypeError("Only integers allowed!")
            
        self._width = a
        self._update_width()