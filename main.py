import tkinter as tk
from gui import GUI
from db import Database

def main():
    # Inicializa a janela principal do Tkinter
    root = tk.Tk()
    # Instancia o banco de dados
    db = Database("sistema.db")
    # Instancia a interface gráfica, passando a janela e o banco de dados
    app = GUI(root, db)
    # Inicia o loop principal da aplicação
    root.mainloop()

if __name__ == "__main__":
    main()

