# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 10:03:44 2023

@author: AMD
"""


import random
import sys
from functools import partial

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *






"""

Data-class for a field in the minefield. Holds essential data for the field.

"""
class Field:
    def __init__(self, i, j, is_mine = False, is_flagged = False, is_open = False):
        self.is_mine = is_mine
        self.is_flagged = is_flagged
        self.is_open = is_open              # if the player has opened this field
        
        self.neighbors = []                 # list of neighbors of the field, including fields with mines
        self.num_neighbouring_mines = 0     # number of neighbors with mines
        
        self.coordinates = (i, j)









"""

Class for a minefield. Holds and alters the game state. Does not handle the GUI.

"""
class Gamefield:
    def __init__(self, width = 10, height = 10, num_mines = 10):
        self._field = [[]]              # 2-dimensional array with fields (instances of Field-class) in it
        self._num_mines = num_mines     # number of mines in the minefield
        self._num_flagged_fields = 0
        self._num_correct_flags = 0
        self._num_opened_fields = 0
        
        self._height = height
        self._width = width
        
        self.reset()
        
    # recursively opens all neighbors with zero mines and also adjacent fields to fields with zero mines
    def _rec_open_free_fields(self, field):
        if not field.is_open:
            self._num_opened_fields += 1
        field.is_open = True
        
        for neighbor in field.neighbors:
            if neighbor.num_neighbouring_mines > 0:
                if not neighbor.is_open:
                    self._num_opened_fields += 1
                neighbor.is_open = True
            elif not neighbor.is_open:
                self._rec_open_free_fields(neighbor)
        
    # opens a field. Returns False if field was a mine. Also, if the field has zero mines, opens
    # all neighbors of the field with zero mines and also adjacent fields to fields with zero mines
    def open_field(self, i, j):
        field = self._field[i][j]
        
        if field.is_mine:
            return False
        
        if not field.is_open:
            self._num_opened_fields += 1
        field.is_open = True
        
        # recursively open all fields with zero mines
        if field.num_neighbouring_mines == 0:
            self._rec_open_free_fields(field)
        
        return True
    
    def set_flag(self, i, j):
        if not self._field[i][j].is_flagged:
            self._num_flagged_fields += 1
            if self._field[i][j].is_mine:
                self._num_correct_flags += 1
            
        self._field[i][j].is_flagged = True
        
    def remove_flag(self, i, j):
        if self._field[i][j].is_flagged:
            self._num_flagged_fields -= 1
            if self._field[i][j].is_mine:
                self._num_correct_flags -= 1
            
        self._field[i][j].is_flagged = False
        
    def is_flagged(self, i, j):
        return self._field[i][j].is_flagged
    
    def is_open(self, i, j):
        return self._field[i][j].is_open
    
    def is_mine(self, i, j):
        return self._field[i][j].is_mine
    
    def get_num_neighbouring_mines(self, i, j):
        return self._field[i][j].num_neighbouring_mines
    
    def get_num_flagged_fields(self):
        return self._num_flagged_fields
    
    def get_num_correct_flags(self):
        return self._num_correct_flags
    
    def get_num_opened_fields(self):
        return self._num_opened_fields
    
    def get_field(self, i, j):
        return self._field[i][j]
    
    def is_game_won(self):
        return self._num_correct_flags + self._num_opened_fields == self._width * self._height

    # closes all fields, removes mines, redistributes mines randomly
    def reset(self):
        self._num_flagged_fields = 0
        self._num_correct_flags = 0
        self._num_opened_fields = 0
        
        self._field = [[Field(i, j) for j in range(self._width)] for i in range(self._height)]
        
        # distribute random mines. Make an array of all possible fields in the minefield,
        # then get one after another field from this array and place a mine there
        all_possible_fields = [(i,j) for j in range(self._width) for i in range(self._height)]
        for n in range(self._num_mines):
            rand_index = random.randint(0, len(all_possible_fields)-1)
            
            i = all_possible_fields[rand_index][0]
            j = all_possible_fields[rand_index][1]
            
            self._field[i][j].is_mine = True
            del all_possible_fields[rand_index]
            
        # get neighbors of each field and number of neighbouring mines
        for i in range(self._height):
            for j in range(self._width):
                neighbors = []
                if i < self._height - 1:
                    neighbors.append(self._field[i+1][j])
                if i > 0:
                    neighbors.append(self._field[i-1][j])
                if j < self._width - 1:
                    neighbors.append(self._field[i][j+1])
                if j > 0:
                    neighbors.append(self._field[i][j-1])
                if i < self._height - 1 and j < self._width - 1:
                    neighbors.append(self._field[i+1][j+1])
                if i > 0 and j < self._width - 1:
                    neighbors.append(self._field[i-1][j+1])
                if i > 0 and j > 0:
                    neighbors.append(self._field[i-1][j-1])
                if i < self._height - 1 and j > 0:
                    neighbors.append(self._field[i+1][j-1])
                    
                self._field[i][j].neighbors = neighbors
                
                # count neighbouring mines
                num_neighbouring_mines = 0
                for neighbor in self._field[i][j].neighbors:
                    if neighbor.is_mine:
                        num_neighbouring_mines += 1
                        
                self._field[i][j].num_neighbouring_mines = num_neighbouring_mines
                    
    @property
    def num_mines(self):
        return self._num_mines
    
    @num_mines.setter
    def num_mines(self, a):
        if type(a) != int:
            raise TypeError("The number of mines must be an integer.")
        if a >= self._height * self._width:
            raise ValueError("There cannot be more mines than fields.")
            
        self._num_mines = a
        self.reset()
        
    @property
    def height(self):
        return self._height
    
    @height.setter
    def height(self, a):
        if type(a) != int:
            raise TypeError("The height and width of the minefield must be an integer.")
            
        self._height = a
        self.reset()
        
    @property
    def width(self):
        return self._width
    
    @width.setter
    def width(self, a):
        if type(a) != int:
            raise TypeError("The height and width of the minefield must be an integer.")
            
        self._width = a
        self.reset()
        
        
        
    
        
    
    
    
        
"""

Class for constants

"""
class CONSTANTS:
    MINEFIELD_IMG_WIDTH = 16
    MINEFIELD_IMG_HEIGHT = 16
    
    IMG_CLOSED_PATH = "img/field_closed.png"
    IMG_MINE_PATH = "img/field_mine.png"
    IMG_MINE_RED_PATH = "img/field_mine_red.png"
    IMG_NUM_MINES = ["img/field_0.png",
                     "img/field_1.png",
                     "img/field_2.png",
                     "img/field_3.png",
                     "img/field_4.png",
                     "img/field_5.png",
                     "img/field_6.png",
                     "img/field_7.png",
                     "img/field_8.png"]
    IMG_FLAG_PATH = "img/field_flag.png"
    
    IMG_SMILEY_HAPPY_PATH = "img/smiley_happy.png"
    IMG_SMILEY_DEAD_PATH = "img/smiley_dead.png"
    IMG_SMILEY_TENSE_PATH = "img/smiley_tense.png"
    IMG_SMILEY_SUNGLASSES_PATH = "img/smiley_sunglasses.png"
    
    
    
    
    
    
    
    
    
"""

Class for a clickable QLabel. Used for fields in the minefield with an image on it.

"""
class QLabel_clickable(QLabel):
    clicked = pyqtSignal()
    rightClicked = pyqtSignal()
    mouseReleased = pyqtSignal()
    mouseDown = pyqtSignal()
    
    def mousePressEvent(self, ev):
        self.mouseDown.emit()
        
        if ev.button() == Qt.LeftButton:
            self.clicked.emit()
        elif ev.button() == Qt.RightButton:
            self.rightClicked.emit()
            
    def mouseReleaseEvent(self, ev):
        self.mouseReleased.emit()
        
    
    
    
    
    
    
    
"""

Gamefield-size dialog

"""
class GamefieldsizeDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.ui = uic.loadUi("GamefieldsizeDialog.ui", self)
    
        self.cancelButton.clicked.connect(self.close)
        self.applyButton.clicked.connect(self._on_applyButton_clicked)
        self.widthSpinBox.valueChanged.connect(self._on_widthSpinBox_valueChanged)
        self.heightSpinBox.valueChanged.connect(self._on_heightSpinBox_valueChanged)
        
        self.minesSpinBox.setMaximum(self.widthSpinBox.value() * self.heightSpinBox.value() - 1)
        
        self.widthSpinBox.setValue(parent._gamefield.width)
        self.heightSpinBox.setValue(parent._gamefield.height)
        self.minesSpinBox.setValue(parent._gamefield.num_mines)
        
        
    def _on_widthSpinBox_valueChanged(self, val):
        self.minesSpinBox.setMaximum(self.widthSpinBox.value() * self.heightSpinBox.value() - 1)
        
    def _on_heightSpinBox_valueChanged(self, val):
        self.minesSpinBox.setMaximum(self.widthSpinBox.value() * self.heightSpinBox.value() - 1)
        
    def _on_applyButton_clicked(self):
        self.parent()._gamefield._width = self.widthSpinBox.value()
        self.parent()._gamefield._height = self.heightSpinBox.value()
        self.parent()._gamefield._num_mines = self.minesSpinBox.value()
        self.parent()._gamefield.reset()
        
        self.parent().reset_gamefield()
        self.close()


    




    
"""

Main-GUI-class

"""
class GameDialog(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self._gamefield = Gamefield()
        self._minefield_labels= [[]]    # 2-dimensional array for the GUI-elements of the fields in the minefield
        self._is_game_over = False
        self._is_game_started = False   # if the player has yet clicked on a field

        self.ui = uic.loadUi("MainWindow.ui", self)
        
        self.smileyButton.clicked.connect(self._on_smiley_button_clicked)
        self.actionClose.triggered.connect(self._on_actionClose_clicked)
        self.actionGamefieldsize.triggered.connect(self._on_actionGamefieldsize_clicked)
        
        self._gamefield.num_mines = 50
        self._gamefield.width = 20
        self._gamefield.height = 20
        self.reset_gamefield()
        self.update_gamefield()
        
    def _on_actionGamefieldsize_clicked(self):
        dialog = GamefieldsizeDialog(self)
        dialog.show()
        
    def _on_actionClose_clicked(self):
        self.close()

    def _on_smiley_button_clicked(self, e):
        self.reset_gamefield()
    
    # called when the player has clicked on a mine with indices mine_indices.
    # Opens all fields and shows all mines.
    def _gameover_open_all_fields(self, mine_indices):
        self._is_game_over = True
        self.rightCounter.stop()
        self.smileyButton.setIcon(QIcon(QPixmap(CONSTANTS.IMG_SMILEY_DEAD_PATH)))
        
        # open all fields
        for i in range(0, self._gamefield.height):
            for j in range(0, self._gamefield.width):
                current_label = self._minefield_labels[i][j]
                
                if self._gamefield.is_mine(i, j):
                    current_label.setPixmap(QPixmap(CONSTANTS.IMG_MINE_PATH))
                else:
                    current_label.setPixmap(QPixmap(CONSTANTS.IMG_NUM_MINES[self._gamefield.get_num_neighbouring_mines(i, j)]))
                    
        # make the mine the played clicked on red
        self._minefield_labels[mine_indices[0]][mine_indices[1]].setPixmap(QPixmap(CONSTANTS.IMG_MINE_RED_PATH))
                
    # called when a field has been LEFT clicked to open it
    def _on_field_left_clicked(self, indices):
        if not self._is_game_started:
            self._is_game_started = True
            self.rightCounter.start()
        
        if self._is_game_over:
            return
        
        # do not open flagged fields
        if self._gamefield.is_flagged(indices[0], indices[1]):
            return
        
        # open field and check if the player clicked on a mine
        if not self._gamefield.open_field(indices[0], indices[1]):
            self._gameover_open_all_fields(indices)
        else:
            self.update_gamefield()
            
    # called when a field has been RIGHT clicked to flag it
    def _on_field_right_clicked(self, indices):
        if self._is_game_over:
            return
        
        i, j = indices[0], indices[1]
        
        if self._gamefield.get_num_flagged_fields() == self._gamefield.num_mines and not self._gamefield.is_flagged(i, j):
            return
        
        if self._gamefield.is_flagged(i, j):
            self._gamefield.remove_flag(i, j)
        elif not self._gamefield.is_open(i, j):
            self._gamefield.set_flag(i, j)
            
        self.update_gamefield()
        
    def _on_field_mouse_released(self):
        if not self._is_game_over:
            self.smileyButton.setIcon(QIcon(QPixmap(CONSTANTS.IMG_SMILEY_HAPPY_PATH)))
        
    def _on_field_mouse_down(self):
        if not self._is_game_over:
            self.smileyButton.setIcon(QIcon(QPixmap(CONSTANTS.IMG_SMILEY_TENSE_PATH)))
        
    # closes all fields in the minefield, redistributes mines, resets counters etc.
    def reset_gamefield(self):
        self._gamefield.reset()
        
        self._is_game_over = False
        self._is_game_started = False
        
        self.smileyButton.setIcon(QIcon(QPixmap(CONSTANTS.IMG_SMILEY_HAPPY_PATH)))
        
        self.rightCounter.stop()
        self.rightCounter.number = 0
        
        window_width = CONSTANTS.MINEFIELD_IMG_WIDTH * self._gamefield.width
        window_height = CONSTANTS.MINEFIELD_IMG_HEIGHT * self._gamefield.height + 40
        self.setMinimumSize(window_width, window_height)
        self.setMaximumSize(window_width, window_height)
        
        for i in range(0, self.layout_minefield.rowCount()):
            for j in range(0, self.layout_minefield.columnCount()):
                self.layout_minefield.removeItem(self.layout_minefield.itemAtPosition(i, j))

        self._minefield_labels = [[QLabel_clickable(self) for j in range(self._gamefield.width)] for i in range(self._gamefield.height)]
        
        # set properties of labels/fields
        for i in range(0, self._gamefield.height):
            for j in range(0, self._gamefield.width):
                current_label = self._minefield_labels[i][j]
                
                # pass the data which field has been clicked to the functions with "partial"
                current_label.clicked.connect(partial(self._on_field_left_clicked, (i,j)))
                current_label.rightClicked.connect(partial(self._on_field_right_clicked, (i,j)))
                
                current_label.mouseReleased.connect(self._on_field_mouse_released)
                current_label.mouseDown.connect(self._on_field_mouse_down)
                
                # set default image
                current_label.setPixmap(QPixmap(CONSTANTS.IMG_CLOSED_PATH))
                
                self.layout_minefield.addWidget(current_label, i, j)
                
        self.update_gamefield()
                
    # update minefield according to the data in the Gamefield-object
    def update_gamefield(self):
        self.leftCounter.number = self._gamefield.num_mines - self._gamefield.get_num_flagged_fields()
        
        # set the right images for the labels
        for i in range(0, self._gamefield.height):
            for j in range(0, self._gamefield.width):
                current_label = self._minefield_labels[i][j]
                
                if self._gamefield.is_flagged(i, j):
                    current_label.setPixmap(QPixmap(CONSTANTS.IMG_FLAG_PATH))
                elif self._gamefield.is_open(i, j):
                    current_label.setPixmap(QPixmap(CONSTANTS.IMG_NUM_MINES[self._gamefield.get_num_neighbouring_mines(i, j)]))
                else:
                    current_label.setPixmap(QPixmap(CONSTANTS.IMG_CLOSED_PATH))
                  
        if self._gamefield.is_game_won():
            self._is_game_over = True
            self.smileyButton.setIcon(QIcon(QPixmap(CONSTANTS.IMG_SMILEY_SUNGLASSES_PATH)))
            self.rightCounter.stop()
            
            
            
            
            
            
                  
def main():
    app = QtWidgets.QApplication(sys.argv)
    dialog = GameDialog()
    dialog.show()
    sys.exit(app.exec_())
    
main()
    
    