from tkinter import *
from tkinter import ttk
import subprocess




class RMS:
    def __init__(self, root):
        self.root = root
        self.root.title("Emploi du temps")
        self.root.configure(bg="white")
        self.root.geometry("1350x700+0+0")

        Label(root, text="Nombre de classe", bg="black").pack(pady=10)
        self.entry_classes = Entry(root, width=30)
        self.entry_classes.pack(pady=5)

        Label(root, text="Nombre de Salle", bg="black").pack(pady=10)
        self.entry_salles = Entry(root, width=30)
        self.entry_salles.pack(pady=5)

        Label(root, text="(Prof, Module, Groupes, NbSéancesTotal, IndicesDispos)", bg="black").pack(pady=10)
        self.entry_data = Entry(root, width=50)
        self.entry_data.pack(pady=5)

        
        Button(root, text="Générer Emploi du temps", command=self.run_program).pack(pady=20)

    def run_program(self):
        classes = self.entry_classes.get()
        salles = self.entry_salles.get()
        data = self.entry_data.get()

        print("Classes:", classes)
        print("Salles:", salles)
        print("Data:", data)

        subprocess.run(["python3", "algotest.py", classes, salles, data])

root = Tk()

frm = ttk.Frame(root, padding=100)
frm.grid()
ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=1)
if __name__ == '__main__':
    root = Tk()
    obj=RMS(root)
    root.mainloop()
