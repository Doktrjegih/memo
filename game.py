import random
import sys

from PyQt6.QtCore import QSize, QTimer
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (QWidget, QPushButton, QApplication)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.state = None
        self.first_position = None
        self.all_buttons = []
        self.player1 = 0
        self.player2 = 0
        self.current_player_name = 'player1'
        self.initUI()

    def initUI(self):
        matrix = self.create_matrix()
        for counter, row in enumerate(matrix):
            for counter_, element in enumerate(row):
                btn = QPushButton(self)
                btn.setIcon(QIcon('back.png'))
                btn.setIconSize(QSize(50, 50))
                btn.move(counter * 85, counter_ * 80)
                btn.clicked.connect(lambda state, x=element, btn=btn: self.handleButton(x, btn))
                self.all_buttons.append(btn)
        self.setGeometry(300, 300, 340, 310)  # 4*4
        # self.setGeometry(300, 300, 520, 480)  # 6*6
        self.setWindowTitle(f"player1 {self.player1} | {self.player2} player2 ({self.current_player_name}'s turn)")
        self.show()

    def handleButton(self, value, btn: QPushButton):
        btn.setIcon(QIcon(f'img_{value}.png'))
        if self.state:
            for button in self.all_buttons:
                button.blockSignals(True)
            if value == self.state:
                timer = QTimer(self)
                timer.setSingleShot(True)
                timer.timeout.connect(lambda: self.remove_buttons(btn))
                timer.start(1000)
            else:
                timer = QTimer(self)
                timer.setSingleShot(True)
                timer.timeout.connect(lambda: self.hide_buttons(btn))
                timer.start(1000)
        else:
            self.state = value
            self.first_position = btn
            btn.setIcon(QIcon(f'img_{value}.png'))
            btn.blockSignals(True)

    def remove_buttons(self, btn):
        btn.close()
        self.first_position.close()
        self.state = None
        self.first_position = None
        for button in self.all_buttons:
            button.blockSignals(False)
        if self.current_player_name == 'player1':
            self.player1 += 1
        else:
            self.player2 += 1
        self.setWindowTitle(f"player1 {self.player1} | {self.player2} player2 ({self.current_player_name}'s turn)")

    def hide_buttons(self, btn):
        btn.setIcon(QIcon('back.png'))
        self.first_position.setIcon(QIcon('back.png'))
        self.state = None
        self.first_position = None
        for button in self.all_buttons:
            button.blockSignals(False)
        if self.current_player_name == 'player1':
            self.current_player_name = 'player2'
        else:
            self.current_player_name = 'player1'
        self.setWindowTitle(f"player1 {self.player1} | {self.player2} player2 ({self.current_player_name}'s turn)")

    def create_matrix(self):
        def add_element():
            while values:
                number = random.choice(values)
                element = None
                while element is None:
                    index = random.randint(0, 3)
                    if len(matrix[index]) < 4:
                        matrix[index].append(number)
                        element = True
                values.remove(number)
        matrix = [[] for x in range(4)]
        values = [x for x in range(1, 9)]
        add_element()
        values = [x for x in range(1, 9)]
        add_element()
        return matrix


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec())
