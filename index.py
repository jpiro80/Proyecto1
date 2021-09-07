from tkinter import ttk
from tkinter import *

import sqlite3

class gastos_mensuales:

    db_name = 'database.db'

    def __init__(self, window):
        self.wind = window
        self.wind.title('Pagos del mes')

        # Creating a Frame Container
        frame = LabelFrame(self.wind, text = 'Agregar un nuevo pago') 
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)

        # Year Input
        Label(frame, text = 'Año: ').grid(row = 1, column = 0)
        self.year = Entry(frame)
        self.year.grid(row = 1, column = 1)

        # Month Input
        Label(frame, text = 'Mes: ').grid(row = 2, column = 0)
        self.month = Entry(frame)
        self.month.grid(row = 2, column = 1)

        # Luz Input
        Label(frame, text = 'Luz: ').grid(row = 3, column = 0)
        self.luz = Entry(frame)
        self.luz.grid(row = 3, column = 1)

        # Gas Input
        Label(frame, text = 'Gas: ').grid(row = 4, column = 0)
        self.gas = Entry(frame)
        self.gas.grid(row = 4, column = 1)

        # Agua Input
        Label(frame, text = 'Agua: ').grid(row = 5, column = 0)
        self.agua = Entry(frame)
        self.agua.grid(row = 5, column = 1)

        # Internet Input
        Label(frame, text = 'Internet: ').grid(row = 6, column = 0)
        self.internet = Entry(frame)
        self.internet.grid(row = 6, column = 1)

        # Arriendo Input
        Label(frame, text = 'Arriendo: ').grid(row = 7, column = 0)
        self.arriendo = Entry(frame)
        self.arriendo.grid(row = 7, column = 1)

        # Gastos Comunes Input
        Label(frame, text = 'Gastos Comunes: ').grid(row = 8, column = 0)
        self.gastos_comunes = Entry(frame)
        self.gastos_comunes.grid(row = 8, column = 1)

        # Button Add Gasto
        ttk.Button(frame, text = 'Agregar', command = self.add_gastos_mensuales).grid(row = 9, columnspan = 2, sticky = W + E)

        # Output Messages
        self.message = Label(text = '', fg = 'red')
        self.message.grid(row = 1, column = 0, columnspan = 2, sticky = W + E)

        # Table
        self.tree = ttk.Treeview(height = 12, columns = ('#1','#2','#3','#4','#5','#6','#7','#8'))
        self.tree['show'] = 'headings'
        self.tree.grid(row = 4, column = 0, columnspan = 2)
        self.tree.heading('#1', text = 'Año', anchor = CENTER)
        self.tree.heading('#2', text = 'Mes', anchor = CENTER)
        self.tree.heading('#3', text = 'Luz', anchor = CENTER)
        self.tree.heading('#4', text = 'Gas', anchor = CENTER)
        self.tree.heading('#5', text = 'Agua', anchor = CENTER)
        self.tree.heading('#6', text = 'Internet', anchor = CENTER)
        self.tree.heading('#7', text = 'Arriendo', anchor = CENTER)
        self.tree.heading('#8', text = 'Gastos Comunes', anchor = CENTER)

        # Buttons
        ttk.Button(text = 'BORRAR', command = self.delete_gasto).grid(row = 10, column = 0, sticky = W + E)
        ttk.Button(text = 'EDITAR', command = self.edit_gasto).grid(row = 10, column = 1, sticky = W + E)

        # Filling the Row
        self.get_gastos_mensuales()

    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def get_gastos_mensuales(self):
        # cleaning table
        records = self.tree.get_gastos_mensuales()
        for element in records:
            self.tree.delete(element)
        # quering data
        query = 'SELECT * FROM gastos_mensuales ORDER BY name DESC'
        db_rows = self.run_query(query)
        # filling data
        for row in db_rows:
            self.tree.insert('', 0, text = row[1], values = row[2])

    def validation(self):
        return len(self.name.get()) != 0 and len(self.price.get()) !=0

    def add_gastos_mensuales(self):
        if self.validation():
            query = 'INSERT INTO gastos_mensuales VALUES(NULL, ?, ?)'
            parameters = (self.year.get(), self.month.get())
            self.run_query(query, parameters)
            self.message['text'] = 'El importe {} fue agregado correctamente'.format(self.name.get())
            self.year.delete(0, END)
            self.month.delete(0, END)
        else:
            self.message['text'] = 'Por favor, rellene los campos vacíos'
        self.get_gastos()

    def delete_gasto(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'No se ha seleccionado un impuesto'
            return
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM gastos_mensuales WHERE name = ?'
        self.run_query(query, (name, ))
        self.message['text'] = 'El impuesto {} fue eliminado correctamente'.format(name)
        self.get_gastos()

    def edit_gasto(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'No se ha seleccionado un impuesto'
            return
        name = self.tree.item(self.tree.selection())['text']
        old_price = self.tree.item(self.tree.selection())['values'][0]
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Edit gastos_mensuales'

        # Old Name
        Label(self.edit_wind, text = 'Impuesto actual: ').grid(row = 0, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = name), state = 'readonly').grid(row = 0, column = 2)
        # New Name
        Label(self.edit_wind, text = 'Nuevo impuesto').grid(row = 1, column = 1)
        new_name = Entry(self.edit_wind)
        new_name.grid(row = 1, column = 2)

         # Old Price
        Label(self.edit_wind, text = 'Importe actual: ').grid(row = 2, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_price), state = 'readonly').grid(row = 2, column = 2)
        # New Price
        Label(self.edit_wind, text = 'Nuevo importe').grid(row = 3, column = 1)
        new_price = Entry(self.edit_wind)
        new_price.grid(row = 3, column = 2)

        Button(self.edit_wind, text = 'Actualizar', command = lambda: self.edit_records(new_name.get(), name, new_price.get(), old_price)).grid(row = 4, column = 2, sticky = W)

    def edit_records(self, new_name, name, new_price, old_price):
        query = 'UPDATE product SET name = ?, price = ? WHERE name = ? AND price = ?'
        parameters = (new_name, new_price, name, old_price)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = 'El impuesto {} fue modificado correctamente'.format(name)
        self.get_gastos_mensuales()

if __name__== '__main__':
    window = Tk()
    application = gastos_mensuales(window)
    window.mainloop()

    

