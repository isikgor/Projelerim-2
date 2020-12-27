import tkinter as tki
from tkinter import ttk, filedialog,messagebox

import  database as db
import add_box as abox 


tk = tki.Tk()
tk.resizable(0, 0)
widthofScreen = tk.winfo_screenwidth()
heightofScreen = tk.winfo_screenheight()

tk.geometry(str.format(
    "1280x720+{0}+{1}", str(int(widthofScreen/2-640)), str(int(heightofScreen/2-360))))
tk.title("Veritabanı Uygulamaları | Abdulkadir Işıkgör")


class Application:
    

    def __init__(self,root):
        self.root = root
        self.__load__()

    def __load__(self):

        self.tree = None
        self.commands_row = None

        self.groupbox1 = tki.LabelFrame(self.root, text="Veritabanı Dosyası")
        self.groupbox1.grid(row=0, column=1, padx=5, pady=5)
        self.groupbox1.place(
            x=0, y=0, width = 1280, height = 100)

        self.groupbox2 = tki.LabelFrame(self.root, text="Veritabanı")
        self.groupbox2.grid(row=0, column=1, padx=5, pady=5)
        self.groupbox2.place(
            x=0, y=100, width=1280, height=620)

        path_label = tki.Label(
            self.root, text='Veritabanı dosyası: ')
        path_label.place(x=40, y=20)

        self.source_path = tki.StringVar()

        self.path = tki.Entry(self.root, textvariable = self.source_path ,width=100)
        self.path.place(x=160, y=22)
        self.path.configure(state =tki.DISABLED)

        path_label = tki.Label(
            self.root, text='Tablo: ')
        path_label.place(x=550, y=60)

        self.combobox = ttk.Combobox(self.root)
        self.combobox.place(x=600, y=60, width=150, height=20)
        self.combobox.configure (state = tki.DISABLED)

        self.open_button = tki.Button(
            self.root, text='Dosya Aç',command=self.open_file)
        self.open_button.place(x=800, y = 22, width=100, height=20)

        self.show_button = tki.Button(
            self.root, text='Tabloyu Göster',command=self.__load_db__)
        self.show_button.place(x=800, y=60, width=100, height=30)
        self.show_button.config(state = tki.DISABLED)

    def open_file(self):
        self.source_path.set(filedialog.askopenfilename(
            initialdir="/", title="Bir text dosyası seç", filetypes=(("Veritabanı Dosyaları", "*.db *.db3 *.sqlite *.sqlite3"),)))

        src = self.source_path.get()
        if src != '':
            self.open_button.config(state=tki.DISABLED)
            self.combobox.configure(state = tki.NORMAL)
            self.show_button.config(state=tki.NORMAL)
            
            self.dbase = db.Database(src)
            self.combobox['values'] = self.dbase.get_tables()
        else:
            self.open_button.config(state=tki.NORMAL)
            self.combobox.configure(state=tki.DISABLED)
            self.show_button.config(state=tki.DISABLED)

    def __load_db__(self):

        table = self.combobox.get()

        if table == '':
            messagebox.showerror('Tablo Seçiniz', 'Lütfen bir tablo seçiniz.', parent=self.root)
            return

        if self.tree != None:
            self.tree.destroy()

        if self.commands_row != None:
            self.commands_row.destroy()

        self.tree = ttk.Treeview(self.root)
        self.tree['columns'] = ('name', 'address', 'date')

        self.tree.heading('#0', text='ID')
        self.tree.column('#0',anchor='center', width=30)

        self.tree.heading('name', text='Ad Soyad')
        self.tree.column('name', anchor='center', width=100)

        self.tree.heading('address', text='Kitap')
        self.tree.column('address', anchor='center', width=100)

        self.tree.heading('date', text='Tarih')
        self.tree.column('date', anchor='center', width=100)

        self.tree.place(x=0, y=120, width=1280,height=520)

        self.all_records = dict(self.dbase.get_all_records(self.combobox.get()))

        for record in self.all_records:
            e = str(record)
            self.tree.insert('','end',e,text = e)
            self.tree.set(e,'name', self.all_records.get(record).get('name'))
            self.tree.set(e,'address', self.all_records.get(record).get('address'))
            self.tree.set(e,'date', self.all_records.get(record).get('date'))
        
        
        self.commands_row = tki.Frame(self.root)
        self.commands_row.pack(side=tki.BOTTOM, fill = tki.X)

        add_new_button = tki.Button(self.commands_row, text='Yeni Ekle',height='3', command=self.add)
        delete_button = tki.Button(
            self.commands_row, text='Sil', height='3',  command=self.delete_item)
        update_button = tki.Button(
            self.commands_row, text='Güncelle', height='3',  command=self.update)
        refresh_button = tki.Button(
            self.commands_row, text='Listeyi Yenile', height='3',  command=self.__load_db__)

        search = tki.Button(
            self.commands_row, text='Ara', height='3',  command=self.search)
        
        search.pack(side=tki.RIGHT, expand=tki.YES, fill=tki.X)
        refresh_button.pack(side=tki.RIGHT, expand=tki.YES, fill=tki.X)
        delete_button.pack(side=tki.RIGHT, expand=tki.YES, fill=tki.X)
        update_button.pack(side=tki.RIGHT, expand=tki.YES, fill=tki.X)
        add_new_button.pack(side=tki.RIGHT, expand=tki.YES, fill=tki.X)

    def run(self):
        self.root.mainloop()

    def add(self):
        inb = abox.AddNewBox()
        inb.run(self,int(widthofScreen/2 - 150),int(heightofScreen / 2 - 55))
        self.__load_db__()

    def update(self):

        id = int(self.tree.selection()[0])

        inb = abox.AddNewBox()
        inb.run(self, int(widthofScreen/2 - 150), int(heightofScreen / 2 - 55),id,self.all_records.get(id).get("name"),self.all_records.get(id).get("address"))
        
        self.__load_db__()

    def search(self):
        inputBox = abox.InputBox()
        inputBox.__load__(self,int(widthofScreen / 2 - 150),int( heightofScreen / 2 - 50), self.dbase.get_all_records(self.combobox.get()))
        inputBox.mainloop()

    def select(self, id):
        self.tree.selection_set(id)

    def delete_item(self):

        if self.tree.selection() == '':
            return

        id = int(self.tree.selection()[0])


        self.dbase.delete_record(self.combobox.get(),id)

        self.__load_db__()

app = Application(tk)
app.run()
