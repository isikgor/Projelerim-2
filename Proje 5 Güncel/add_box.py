import tkinter as tk
from tkinter import messagebox
import datetime as dt 


class AddNewBox(tk.Tk):
    def __load__(self):

        self.resizable(0,0)

        if self.id != -1:
            self.title('Kayıt Yenileme')
        else:
            self.title('Kayıt ekleme')


        var1 = tk.StringVar()
        var2 = tk.StringVar()
        

        row1 = tk.Frame(self)
        label1 = tk.Label(row1, width=15, text="Ad Soyad", anchor='w')
        self.entry1 = tk.Entry(row1,textvariable=var1)

        row2 = tk.Frame(self)
        label2 = tk.Label(row2, width=15, text="Kitap", anchor='w')
        self.entry2 = tk.Entry(row2)

        row1.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        label1.pack(side=tk.LEFT)
        self.entry1.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        
        row2.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        label2.pack(side=tk.LEFT)
        self.entry2.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

        row3 = tk.Frame(self)
        ok_button = tk.Button(row3,text='Ekle' if self.id == -1 else 'Yenile',command = self.add)
        cancel_button = tk.Button(row3,text='İptal',command = self.close)
        
        row3.pack(side=tk.BOTTOM,fill=tk.X,padx=5,pady = 5)
        ok_button.pack(side=tk.LEFT,expand=tk.YES, fill=tk.X)
        cancel_button.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    def close(self):
        self.quit()
        self.destroy()

    def add(self):

        if self.id == -1:
            self.root.dbase.add_new_record(self.root.combobox.get(),
                                       self.entry1.get(),
                                       self.entry2.get(),
                                       self.get_date())
        else:
            self.root.dbase.update_record(self.root.combobox.get(),
                                        self.id,
                                        self.entry1.get(),
                                        self.entry2.get(),
                                        self.get_date())

        self.close()
    
    def get_date(self):
        date = dt.datetime.now()
        return f"{date.day}.{date.month}.{date.year} {date.hour}:{date.minute}:{date.second}"

    def run(self,root,x = 0, y = 0,id = -1,name = '', address = ''):
        
        self.id = id
        self.name = name
        self.address = address

        self.root = root
        self.geometry(f"300x115+{x}+{y}")
        self.__load__()
        self.mainloop()


class InputBox(tk.Tk):
    def __load__(self,root,x,y,values = dict):
        
        self.resizable(0, 0)

        self.root = root
        self.geometry(f"300x100+{x}+{y}")
        self.title("Ara")
        self.values = values

        row1 = tk.Frame(self)
        label1 = tk.Label(row1, width=15, text="Aranacak Kelime: ", anchor='w')
        self.entry1 = tk.Entry(row1)

        row1.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        label1.pack(side=tk.LEFT)
        self.entry1.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

        row2 = tk.Frame(self)
        ok_button = tk.Button(
            row2, text='Ara', command=self.search)
        cancel_button = tk.Button(row2, text='İptal', command=self.close)

        row2.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
        ok_button.pack(side=tk.LEFT, expand=tk.YES, fill=tk.X)
        cancel_button.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        
    def close(self):
        self.quit()
        self.destroy()

    def search(self):
        text = self.entry1.get()
        found = -1
        for v in list(self.values.keys()):
            if self.values.get(v)["name"] == text or self.values.get(v)["address"] == text or self.values.get(v)["date"] == text:
                found = v
                break

        if found != -1:
            self.root.select(found)
        else:
            messagebox.showerror("Bulunmadı", "Aranan değer bulunmadı.")
            
        self.close()

