import sys, re
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton, QGridLayout
from PyQt5.QtGui import QRegularExpressionValidator
from PyQt5.QtCore import QRegularExpression
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor

class Calculator(QWidget):

    def __init__(self):
        super(Calculator, self).__init__()
        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)

        self.input = QLineEdit(self)
        self.text = '0'
        self.completed = True

        regex = QRegularExpression(r'-?\d+(\.\d+)?')
        self.validator = QRegularExpressionValidator(regex)
        self.input.setValidator(self.validator)
        self.input.setText('0')
        self.input.setReadOnly(True)

        self.num_1 = 0
        self.num_2 = 1
        self.operation = ''
        self.last_pressed = 'number'
        self.operation_chosen = False


        self.grid_layout.addWidget(self.input, 0, 0, 1, 3)

        k = 7
        for i in range(9):
            b = QPushButton(str(k), self)
            b.clicked.connect(lambda a, b=k: self._button(str(b)))
            self.grid_layout.addWidget(b, 1+i//3, i%3)
            if k%3==0:
                k-=5
            else:
                k+=1

        delete = QPushButton('=', self)
        delete.clicked.connect(lambda: self._result())
        self.grid_layout.addWidget(delete, 0, 4, 1, 1)

        div = QPushButton('/', self)
        div.setCheckable(True)
        div.clicked.connect(lambda: self._operation('/'))
        self.grid_layout.addWidget(div, 1, 4, 1, 1)

        mult = QPushButton('*', self)
        mult.setCheckable(True)
        mult.clicked.connect(lambda: self._operation('*'))
        self.grid_layout.addWidget(mult, 2, 4, 1, 1)

        minus = QPushButton('-', self)
        minus.setCheckable(True)
        minus.clicked.connect(lambda: self.on_minus('-'))
        self.grid_layout.addWidget(minus, 3, 4, 1, 1)

        plus = QPushButton('+', self)
        plus.setCheckable(True)
        plus.clicked.connect(lambda: self._operation('+'))
        self.grid_layout.addWidget(plus, 4, 4, 1, 1)

        zero = QPushButton('0', self)
        zero.clicked.connect(lambda: self._button('0'))
        self.grid_layout.addWidget(zero, 4, 1, 1, 1)

        point = QPushButton('.', self)
        point.clicked.connect(lambda: self._button('.'))
        self.grid_layout.addWidget(point, 4, 2, 1, 1)

        ce = QPushButton('CE', self)
        ce.clicked.connect(self.on_ce)
        self.grid_layout.addWidget(ce, 4, 0, 1, 1)

        self.operations = [plus, minus, mult, div]


    def on_ce(self):
        self.operation=''
        self.num_1=0
        self.input.setText('0')
        for i in self.operations:
            i.setChecked(False)

    def on_minus(self, param):
        if self.input.text() == '0' or self.last_pressed == 'operation':
            self.input.setText('-')
            self.sender().setChecked(self.operation==param)
            self.last_pressed = 'number'
        else:
            self._operation(param)

    def check_line(self, line):
        if re.match(r'^-?\d+\.?(\d+)?$', line) == None and re.match(r'^-?\d+$', line) == None:
            return False
        return True

    def _button(self, param):
        line = self.input.text()*(not(self.last_pressed != 'number' and self.operation_chosen))+param
        if len(line) > 1 and line[0] == '0' and line[1] != '.':
            line = line[1:]
        if len(line) > 2 and line[0:2] == '-0' and line[3] != '.':
            line = '-' + line[2:]
        if self.validator.validate(line, 0)[0] == QRegularExpressionValidator.Acceptable or \
                self.validator.validate(line, 0)[0] == QRegularExpressionValidator.Intermediate:
            self.input.setText(line)
            self.last_pressed = 'number'

    def _operation(self, op):
        if not self.check_line(self.input.text()):
            for i in self.operations:
                i.setChecked(False)
            return
        if not self.completed and self.last_pressed != 'operation':
            self._result()
        for i in self.operations:
            if i.text() != op:
                i.setChecked(False)
            else:
                i.setChecked(True)
                self.operation_chosen = True
                self.operation = op
        self.last_pressed = 'operation'
        self.num_1 = float(self.input.text())
        self.completed = False

    def try_int(self, num):
        if num == int(num):
            return int(num)
        return num

    def _result(self):
        if not self.check_line(self.input.text()):
            return
        if self.last_pressed != 'equal':
            self.num_2 = float(self.input.text())

        if self.operation == "+":
            self.input.setText(str(self.try_int(self.num_1 + self.num_2)))
            self.num_1 = self.num_1 + self.num_2
        if self.operation == "*":
            self.input.setText(str(self.try_int(self.num_1 * self.num_2)))
            self.num_1 = self.num_1 * self.num_2
        if self.operation == "-":
            self.input.setText(str(self.try_int(self.num_1 - self.num_2)))
            self.num_1 = self.num_1 - self.num_2
        if self.operation == "/":
            if self.num_2 != 0:
                self.input.setText(str(self.try_int(self.num_1 / self.num_2)))
                self.num_1 = self.num_1 / self.num_2
            else:
                self.input.setText('Error: division by zero')
                self.op = ''
                for i in self.operations:
                    i.setChecked(False)
        
        self.last_pressed = 'equal'
        self.completed = True


app = QApplication(sys.argv)

win = Calculator()
win.show()

sys.exit(app.exec_())
