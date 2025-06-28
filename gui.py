import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Tuple

class GUI:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        self.root.title("Sistema de Gerenciamento de Clientes e Pedidos")
        self.root.geometry("800x600")
        self.create_main_window()

    def create_main_window(self):
        # Notebook para abas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True, fill="both")

        # Frames para cada aba
        self.client_frame = ttk.Frame(self.notebook)
        self.order_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.client_frame, text="Clientes")
        self.notebook.add(self.order_frame, text="Pedidos")

        self.setup_client_tab()
        self.setup_order_tab()

    def setup_client_tab(self):
        # Frame para entrada de dados do cliente
        input_frame = ttk.LabelFrame(self.client_frame, text="Dados do Cliente")
        input_frame.pack(pady=10, padx=10, fill="x")

        # Campos de entrada
        ttk.Label(input_frame, text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.client_name = ttk.Entry(input_frame)
        self.client_name.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Email:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.client_email = ttk.Entry(input_frame)
        self.client_email.grid(row=1, column=1, padx=5, pady=5)

        # Botões CRUD
        button_frame = ttk.Frame(self.client_frame)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Adicionar", command=self.add_client).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Atualizar", command=self.update_client).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Excluir", command=self.delete_client).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Listar", command=self.list_clients).pack(side="left", padx=5)

        # Treeview para exibir clientes
        self.client_tree = ttk.Treeview(self.client_frame, columns=("ID", "Nome", "Email"), show="headings")
        self.client_tree.heading("ID", text="ID")
        self.client_tree.heading("Nome", text="Nome")
        self.client_tree.heading("Email", text="Email")
        self.client_tree.pack(pady=10, padx=10, fill="both", expand=True)
        self.client_tree.bind("<<TreeviewSelect>>", self.on_client_select)

    def setup_order_tab(self):
        # Frame para entrada de dados do pedido
        input_frame = ttk.LabelFrame(self.order_frame, text="Dados do Pedido")
        input_frame.pack(pady=10, padx=10, fill="x")

        # Campos de entrada
        ttk.Label(input_frame, text="Cliente:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.client_combo = ttk.Combobox(input_frame, state="readonly")
        self.client_combo.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Produto:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.order_product = ttk.Entry(input_frame)
        self.order_product.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Valor:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.order_value = ttk.Entry(input_frame)
        self.order_value.grid(row=2, column=1, padx=5, pady=5)

        # Botões CRUD
        button_frame = ttk.Frame(self.order_frame)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Adicionar", command=self.add_order).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Atualizar", command=self.update_order).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Excluir", command=self.delete_order).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Listar", command=self.list_orders).pack(side="left", padx=5)

        # Treeview para exibir pedidos
        self.order_tree = ttk.Treeview(self.order_frame, columns=("ID", "Cliente", "Produto", "Valor"), show="headings")
        self.order_tree.heading("ID", text="ID")
        self.order_tree.heading("Cliente", text="Cliente")
        self.order_tree.heading("Produto", text="Produto")
        self.order_tree.heading("Valor", text="Valor")
        self.order_tree.pack(pady=10, padx=10, fill="both", expand=True)
        self.order_tree.bind("<<TreeviewSelect>>", self.on_order_select)

    def add_client(self):
        name = self.client_name.get().strip()
        email = self.client_email.get().strip()
        if not name or not email:
            messagebox.showerror("Erro, Preencha todos os campos!")
            return
        try:
            self.db.add_client(name, email)
            messagebox.showinfo("Sucesso", "Cliente adicionado com sucesso!")
            self.clear_client_fields()
            self.list_clients()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar cliente: {str(e)}")

    def update_client(self):
        selected = self.client_tree.selection()
        if not selected:
            messagebox.showerror("Erro", "Selecione um cliente para atualizar!")
            return
        client_id = self.client_tree.item(selected)["values"][0]
        name = self.client_name.get().strip()
        email = self.client_email.get().strip()
        if not name or not email:
            messagebox.showerror("Erro, Preencha todos os campos!")
            return
        try:
            self.db.update_client(client_id, name, email)
            messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso!")
            self.clear_client_fields()
            self.list_clients()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar cliente: {str(e)}")

    def delete_client(self):
        selected = self.client_tree.selection()
        if not selected:
            messagebox.showerror("Erro", "Selecione um cliente para excluir!")
            return
        client_id = self.client_tree.item(selected)["values"][0]
        if messagebox.askyesno("Confirmação", "Deseja excluir este cliente?"):
            try:
                self.db.delete_client(client_id)
                messagebox.showinfo("Sucesso", "Cliente excluído com sucesso!")
                self.clear_client_fields()
                self.list_clients()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir cliente: {str(e)}")

    def list_clients(self):
        for item in self.client_tree.get_children():
            self.client_tree.delete(item)
        try:
            clients = self.db.get_clients()
            for client in clients:
                self.client_tree.insert("", "end", values=client)
            self.update_client_combo()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao listar clientes: {str(e)}")

    def add_order(self):
        client_name = self.client_combo.get()
        product = self.order_product.get().strip()
        value = self.order_value.get().strip()
        if not client_name or not product or not value:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return
        try:
            value = float(value)
            client_id = self.db.get_client_id_by_name(client_name)
            self.db.add_order(client_id, product, value)
            messagebox.showinfo("Sucesso", "Pedido adicionado com sucesso!")
            self.clear_order_fields()
            self.list_orders()
        except ValueError:
            messagebox.showerror("Erro", "Valor deve ser um número!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar pedido: {str(e)}")

    def update_order(self):
        selected = self.order_tree.selection()
        if not selected:
            messagebox.showerror("Erro", "Selecione um pedido para atualizar!")
            return
        order_id = self.order_tree.item(selected)["values"][0]
        client_name = self.client_combo.get()
        product = self.order_product.get().strip()
        value = self.order_value.get().strip()
        if not client_name or not product or not value:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return
        try:
            value = float(value)
            client_id = self.db.get_client_id_by_name(client_name)
            self.db.update_order(order_id, client_id, product, value)
            messagebox.showinfo("Sucesso", "Pedido atualizado com sucesso!")
            self.clear_order_fields()
            self.list_orders()
        except ValueError:
            messagebox.showerror("Erro", "Valor deve ser um número!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar pedido: {str(e)}")

    def delete_order(self):
        selected = self.order_tree.selection()
        if not selected:
            messagebox.showerror("Erro", "Selecione um pedido para excluir!")
            return
        order_id = self.order_tree.item(selected)["values"][0]
        if messagebox.askyesno("Confirmação", "Deseja excluir este pedido?"):
            try:
                self.db.delete_order(order_id)
                messagebox.showinfo("Sucesso", "Pedido excluído com sucesso!")
                self.clear_order_fields()
                self.list_orders()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir pedido: {str(e)}")

    def list_orders(self):
        for item in self.order_tree.get_children():
            self.order_tree.delete(item)
        try:
            orders = self.db.get_orders()
            for order in orders:
                self.order_tree.insert("", "end", values=order)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao listar pedidos: {str(e)}")

    def on_client_select(self, event):
        selected = self.client_tree.selection()
        if selected:
            values = self.client_tree.item(selected)["values"]
            self.client_name.delete(0, tk.END)
            self.client_name.insert(0, values[1])
            self.client_email.delete(0, tk.END)
            self.client_email.insert(0, values[2])

    def on_order_select(self, event):
        selected = self.order_tree.selection()
        if selected:
            values = self.order_tree.item(selected)["values"]
            self.client_combo.set(values[1])
            self.order_product.delete(0, tk.END)
            self.order_product.insert(0, values[2])
            self.order_value.delete(0, tk.END)
            self.order_value.insert(0, values[3])

    def clear_client_fields(self):
        self.client_name.delete(0, tk.END)
        self.client_email.delete(0, tk.END)

    def clear_order_fields(self):
        self.client_combo.set("")
        self.order_product.delete(0, tk.END)
        self.order_value.delete(0, tk.END)

    def update_client_combo(self):
        clients = self.db.get_clients()
        self.client_combo["values"] = [client[1] for client in clients]