# Author: Femke Spaans
# Date: 02.04.2020
# Name: afvink 6

import mysql.connector
from tkinter import *


def main():
    MyGUI()


class MyGUI():

    def __init__(self):
        root = Tk()
        root.title("PyPiep")

        main_frame = Frame(root)
        main_frame.grid(row=0, column=0, padx=82, pady=10)

        # message
        messages_frame = Frame(main_frame, width=150, height=150)
        messages_frame.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

        message_label = Label(messages_frame, text="Input Message:")
        message_label.grid(row=0, column=0, sticky="nw", pady=(2, 0))

        self.message_entry = Entry(messages_frame, width=50, borderwidth=5)
        self.message_entry.grid(row=0, column=1, sticky="nw")

        message_button = Button(messages_frame, text="Submit Message",
                                command=self.postMessage)
        message_button.grid(row=0, column=2, sticky="nw", padx=10)

        # filter
        filter_frame = Frame(messages_frame)
        filter_frame.grid(row=1, column=0, sticky="nw", columnspan=2)

        filter_label = Label(filter_frame, text="Filter Message:")
        filter_label.grid(row=0, column=0, sticky="nw", pady=(13, 0))

        refresh_button = Button(filter_frame, text="Refresh",
                                command=self.myMessages)
        refresh_button.grid(row=1, column=0)

        self.filter_entry = Entry(filter_frame, text="Filter", width=50,
                                  borderwidth=5)
        self.filter_entry.grid(row=0, column=2, padx=10, pady=10)

        filter_button = Button(filter_frame, text="Filter",
                               command=self.filterMessage)
        filter_button.grid(row=0, column=3, sticky="nw", padx=10, pady=10)

        # display
        self.messages_text = Text(main_frame)
        self.messages_text.grid(row=2, column=0, sticky="nw")

        scrollbar = Scrollbar(main_frame, command=self.messages_text.yview)
        scrollbar.grid(row=2, column=1, sticky="ns")
        self.messages_text.config(yscrollcommand=scrollbar.set)

        root.mainloop()

    def myMessages(self):
        conn = mysql.connector.connect(
            host="hannl-hlo-bioinformatica-mysqlsrv.mysql.database.azure.com",
            user="fxfke@hannl-hlo-bioinformatica-mysqlsrv",
            database="fxfke",
            password="634484")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT piep.bericht, "
            "student.voornaam, "
            "student.tussenvoegsels, "
            "student.achternaam "
            "FROM piep, student "
            "WHERE student.student_nr = piep.student_nr "
            "ORDER BY piep_id ASC")
        rows = cursor.fetchall()
        for i in rows:
            self.messages_text.insert("1.0", str(i) + "\n\n")
        cursor.close()
        conn.close()

    def postMessage(self):
        conn = mysql.connector.connect(
            host="hannl-hlo-bioinformatica-mysqlsrv.mysql.database.azure.com",
            user="fxfke@hannl-hlo-bioinformatica-mysqlsrv",
            database="fxfke",
            password="634484")
        cursor = conn.cursor()
        message = self.message_entry.get()
        cursor.execute("INSERT INTO piep (bericht) value ('" + message + "')")
        conn.commit()
        cursor.close()
        conn.close()

    def filterMessage(self):
        conn = mysql.connector.connect(
            host="hannl-hlo-bioinformatica-mysqlsrv.mysql.database.azure.com",
            user="fxfke@hannl-hlo-bioinformatica-mysqlsrv",
            database="fxfke",
            password="634484")
        cursor = conn.cursor()
        message = self.filter_entry.get().replace("#", "")
        cursor.execute("SELECT piep.bericht, "
                       "student.voornaam, "
                       "student.tussenvoegsels, "
                       "student.achternaam "
                       "FROM piep, student "
                       "WHERE student.student_nr = piep.student_nr "
                       "AND bericht LIKE '%#" + message + "%'")
        rows = cursor.fetchall()
        self.messages_text.delete("1.0", "end")
        for i in rows:
            self.messages_text.insert("1.0", str(i) + "\n\n")
        cursor.close()
        conn.close()


main()
