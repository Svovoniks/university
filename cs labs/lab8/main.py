import psycopg2
import sys

from PyQt5.QtWidgets import (QApplication, QWidget,
                             QTabWidget, QAbstractScrollArea,
                             QVBoxLayout, QHBoxLayout,
                             QTableWidget, QGroupBox,
                         QTableWidgetItem, QPushButton, QMessageBox)

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self._connect_to_db()

        self.setWindowTitle("Shedule")

        self.vbox = QVBoxLayout(self)

        self.weekdays = [
              'понедельник',
              'вторник',
              'среда',
              'четверг',
              'пятница']

        self.main_tab_view = QTabWidget(self)
        self.vbox.addWidget(self.main_tab_view)

        self._create_shedule_tab()
        self._create_teacher_tab()
        self._create_subject_tab()

    def _connect_to_db(self):
        self.conn = psycopg2.connect(database="bot_db",
                                     user="",
                                     password="",
                                     host="",
                                     port="")

        self.cursor = self.conn.cursor()

    def sort_days(self, it):
        it = it.lower()
        if it in self.weekdays:
            return self.weekdays.index(it)
        else:
            return 6 + (it[0]=='с')


    def setup_multy_tab(self):
        self.cursor.execute("SELECT t.day FROM bot.timetable t")
        ls = set([i[0] for i in self.cursor.fetchall()])
       
        
        if len(ls) == 0:
            ls = self.weekdays
        else:
            ls = sorted(ls, key=self.sort_days)
        day_tab_view = QTabWidget()

        for i in ls:
            day_tab = QWidget()
            day_tab_view.addTab(day_tab, i[0].upper()+i[1:].lower())
            day_tab.setLayout(self.get_tab_layout('timetable',
             ['ID', 'Day', 'Subject', 'Start time', 'End time', 'Room number', 'Week'],
             i,
             f"day='{i}'"))

        self.day_tab_layout.addWidget(day_tab_view)

    def reset_multy_tab(self):
        self.day_tab_layout.removeWidget(self.day_tab_layout.itemAt(0).widget())
        self.main_tab_view
        
        self.setup_multy_tab()
        
        self.schedule_tab.update()
        self.subject_tab.update()
        self.teacher_tab.update()

    def _create_shedule_tab(self):
        self.schedule_tab = QWidget()
        self.main_tab_view.addTab(self.schedule_tab, 'Schedule')

        self.day_tab_layout = QVBoxLayout()

        self.setup_multy_tab()

        self.schedule_tab.setLayout(self.day_tab_layout)

    def _create_teacher_tab(self):
        self.teacher_tab = QWidget()
        self.main_tab_view.addTab(self.teacher_tab, 'Teacher')

        self.teacher_tab.setLayout(self.get_tab_layout('teacher',
         ['ID', 'Full name', 'Subject'], 'Teacher'))

    def _create_subject_tab(self):
        self.subject_tab = QWidget()
        self.main_tab_view.addTab(self.subject_tab, 'Subject')

        self.subject_tab.setLayout(self.get_tab_layout('subject',
            ['ID', 'Name'], 'Subject'))

    def get_tab_layout(self, table_name, fields, decor, table_filter=''):
        main_layout = QVBoxLayout()
        update_layout = QHBoxLayout()
        table_container_layout = QHBoxLayout()
     
        main_layout.addLayout(table_container_layout)
        main_layout.addLayout(update_layout)

        view_group = QGroupBox(decor)
        table_layout, table = self.get_table_layout(table_name, fields, table_filter)
        view_group.setLayout(table_layout)
        table_container_layout.addWidget(view_group)

        update_shedule_button = QPushButton("Update")
        update_layout.addWidget(update_shedule_button)
        update_shedule_button.clicked.connect(
            lambda ch, table=table, table_name=table_name: self._update_button(table, table_name, table_filter))
        return main_layout

    def get_table_layout(self, table_name, fields, table_filter=''):
        table = QTableWidget()
        table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        table.setColumnCount(len(fields)+2)
        table.setHorizontalHeaderLabels(fields+['',''])
        self.fill_table(table, table_name, table_filter)


        table_layout = QVBoxLayout()
        table_layout.addWidget(table)
        return (table_layout, table)

    def fill_table(self, table, table_name, table_filter=''):
        self.cursor.execute(f"SELECT * FROM bot.{table_name}{' WHERE '*(table_filter!='')}{table_filter}")
        records = sorted(list(self.cursor.fetchall()), key=lambda a: a[0])


        table.setRowCount(len(records) + 1)

        for i in range(len(records)):
            commit_button = QPushButton("Commit")
            delete_button = QPushButton("Delete")

            for j in range(len(records[i])):
                table.setItem(i, j, QTableWidgetItem(str(records[i][j])))
            table.setSpan(i, len(records[i]), 1, 1)
            table.setSpan(i, len(records[i])+1, 1, 2)
            table.setCellWidget(i, len(records[i]), commit_button)
            table.setCellWidget(i, len(records[i])+1, delete_button)

            commit_button.clicked.connect(
                lambda ch, row=i, table=table, table_name=table_name: self._commit_button(row, table, table_name))
            delete_button.clicked.connect(
                lambda ch, row=i, table=table, table_name=table_name: self._delete_button(row, table, table_name, table_filter))

        add_button = QPushButton("Add entry")
        table.setSpan(len(records), table.columnCount()-2, 1, 2)
        table.setCellWidget(len(records), table.columnCount()-2, add_button)
        add_button.clicked.connect(
            lambda ch, row=len(records), table=table, table_name=table_name: self._add_button(row, table, table_name, table_filter))
        table.resizeRowsToContents()

    def quote(self, value_type, value):
        if value_type == 'integer':
            return value
        return f"'{value}'"

    def form_update(self, table_name, row_data, fields):
        values = ''
        for i in range(len(row_data)):
            values += f"{row_data[i][3]} = {self.quote(row_data[i][7], fields[i])}, "
        return f"UPDATE bot.{table_name} SET {values[:-2]} WHERE id={fields[0]}"

    
    def _update_button(self, table, table_name, table_filter):
        table.clearContents()
        self.fill_table(table, table_name, table_filter)

    def _collet_data(self, row_number, table):
        fields = []
        for i in range(table.columnCount()):
            try:
                fields.append(table.item(row_number, i).text())
            except:
                fields.append(None)
        return fields

    def _commit_button(self, row_number, table, table_name):
        fields = self._collet_data(row_number, table)

        try:
            self.cursor.execute(f"SELECT * FROM information_schema.columns WHERE table_schema = 'bot' AND table_name = '{table_name}'")
            self.cursor.execute(self.form_update(table_name, list(self.cursor.fetchall()), fields))
            self.conn.commit()
            
        except (Exception) as e:
            print(e)
            QMessageBox.about(self, "Error", "Make sure all fields are filled correctly")
            self._connect_to_db()

    def _delete_button(self, row_number, table, table_name, table_filter):
        try:
            self.cursor.execute(f"DELETE FROM bot.{table_name} WHERE id={table.item(row_number, 0).text()}")
            self.conn.commit()
            self._update_button(table, table_name, table_filter)
            self.reset_multy_tab()
        except (Exception) as e:
            QMessageBox.about(self, "Error", "Make sure the row you are trying \
to delete is not referenced anywhere in the database")
            self._connect_to_db()

    def _add_button(self, row_number, table, table_name, table_filter):
        fields = self._collet_data(row_number, table)
        try:
            self.cursor.execute(f"SELECT * FROM information_schema.columns \
                WHERE table_schema = 'bot' AND table_name = '{table_name}'")
            row_data = list(self.cursor.fetchall())

            if fields[0] == None:
                fields = fields[1:-2]
                row_data = row_data[1:]

            self.cursor.execute(
                f"INSERT INTO bot.{table_name} \
                ({', '.join([i[3] for i in row_data])})\
                VALUES({', '.join([self.quote(row_data[i][7], fields[i]) for i in range(len(row_data))])})")
            self.conn.commit()
            self._update_button(table, table_name, table_filter)
            self.reset_multy_tab()

        except (Exception) as e:
            QMessageBox.about(self, "Error", "Make sure all fields are filled correctly")
            self._connect_to_db()


app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())
