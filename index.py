from tkinter import ttk
from tkinter import *

import sqlite3

class Product:

    db_name = 'database.db'

    def __init__(self, window):
        self.wind = window
        self.wind.title('Pagos del mes')

        # Creating a Frame Container
        frame = LabelFrame(self.wind, text = 'Agregar nuevo impuesto') 
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)   

        # Impuesto Input
        Label(frame, text = 'Impuesto: ').grid(row = 1, column = 0)
        self.Impuesto = Entry(frame)
        self.Impuesto.focus()
        self.Impuesto.grid(row = 1, column = 1)

        # Importe Input
        Label(frame, text = 'Importe: ').grid(row = 2, column = 0)
        self.Importe = Entry(frame)
        self.Importe.grid(row = 2, column = 1)

        # Button Add Product
        ttk.Button(frame, text = 'Guardar cambios', command = self.add_product).grid(row = 3, columnspan = 2, sticky = W + E)

        # Output Messages
        self.message = Label(text = '', fg = 'red')
        self.message.grid(row = 3, column = 0, columnspan = 2, sticky = W + E)

        # Table
        self.tree = ttk.Treeview(height = 10, columns = 2)
        self.tree.grid(row = 4, column = 0, columnspan = 2)
        self.tree.heading('#0', text = 'Impuesto', anchor = CENTER)
        self.tree.heading('#1', text = 'Importe', anchor = CENTER)

        # Buttons
        ttk.Button(text = 'BORRAR', command = self.delete_product).grid(row = 5, column = 0, sticky = W + E)
        ttk.Button(text = 'EDITAR', command = self.edit_product).grid(row = 5, column = 1, sticky = W + E)

        # Filling the Row
        self.get_products()

    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def get_products(self):
        # cleaning table
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        # quering data
        query = 'SELECT * FROM product ORDER BY id DESC'
        db_rows = self.run_query(query)
        # filling data
        for row in db_rows:
            self.tree.insert('', 0, text = row[1], values = row[2])

    def validation(self):
        return len(self.Impuesto.get()) != 0 and len(self.Importe.get()) !=0

    def add_product(self):
        if self.validation():
            query = 'INSERT INTO product VALUES(NULL, ?, ?)'
            parameters = (self.Impuesto.get(), self.Importe.get())
            self.run_query(query, parameters)
            self.message['text'] = 'Product {} added Successfully'.format(self.Impuesto.get())
            self.Impuesto.delete(0, END)
            self.Importe.delete(0, END)
        else:
            self.message['text'] = 'Impuesto e importe son requeridos'
        self.get_products()

    def delete_product(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text']
        except IndexError as e:
            self.message['text'] = 'Please Select a Record'
            return
        self.message['text'] = ''
        Impuesto = self.tree.item(self.tree.selection())['text'][0]
        query = 'DELETE FROM product WHERE Impuesto = ?'
        self.run_query(query, (Impuesto, ))
        self.message['text'] = 'Record {} deleted Successfully'.format(Impuesto)
        self.get_products()

    def edit_product(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text']
        except IndexError as e:
            self.message['text'] = 'Please Select a Record'
            return
        Impuesto = self.tree.item(self.tree.selection())['text']
        Importe_Anterior = self.tree.item(self.tree.selection())['values'][0]
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Edit Product'

        # Impuesto Anterior
        Label(self.edit_wind, text = 'Impuesto anterior: ').grid(row = 0, column = 1)
        Entry(self.edit_wind, textvariable =StringVar(self.edit_wind, value = Impuesto), state ='readonly').grid(row = 0, column = 2)
        # Nuevo Impuesto
        Label(self.edit_wind, text = 'Nuevo Impuesto').grid(row = 1, column = 1)
        Nuevo_Impuesto = Entry(self.edit_wind)
        Nuevo_Impuesto.grid(row = 1, column = 2)

        # Importe Anterior
        Label(self.edit_wind, text = 'Importe Anterior').grid(row = 2, column = 1)
        Entry(self.edit_wind, textvariable =StringVar(self.edit_wind, value = Importe_Anterior), state ='readonly').grid(row = 2, column = 2)
        # Nuevo Importe
        Label(self.edit_wind, text = 'Nuevo Importe').grid(row = 3, column = 1)
        Nuevo_Importe = Entry(self.edit_wind)
        Nuevo_Importe.grid(row = 3, column = 2)

        Button(self.edit_wind, text = 'Actualizar', command = lambda: self.edit_records(new_name.get(), name, new_name.get(), old_price)).grid(row = 4, column = 2, sticky = W)

    def edit_records(self, Nuevo_Impuesto, Impuesto, Nuevo_Importe, Importe_Anterior):
        query = 'UPDATE product SET Impuesto = ?, Importe = ? WHERE Impuesto = ? AND Importe = ?'
        parameters = (Nuevo_Impuesto, Nuevo_Importe, Importe, Importe_Anterior)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = 'Record {} updated Successfully'.format(Impuesto)
        self.get_products()

if __name__=='__main__':
    window = Tk()
    application = Product(window)
    window.mainloop()