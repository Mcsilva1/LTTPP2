import sqlite3
from typing import List, Tuple

class Database:
    def __init__(self, db_name: str = "sistema.db"):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.create_tables()

    def connect(self):
        """Estabelece conexão com o banco de dados."""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def close(self):
        """Fecha a conexão com o banco de dados."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def create_tables(self):
        """Cria as tabelas Clientes e Pedidos com relacionamento."""
        self.connect()
        # Tabela Clientes
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
        """)
        # Tabela Pedidos com chave estrangeira
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS pedidos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER NOT NULL,
                produto TEXT NOT NULL,
                valor REAL NOT NULL,
                FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE
            )
        """)
        self.conn.commit()
        self.close()

    def add_client(self, nome: str, email: str) -> None:
        """Adiciona um novo cliente ao banco de dados."""
        self.connect()
        try:
            self.cursor.execute("INSERT INTO clientes (nome, email) VALUES (?, ?)", (nome, email))
            self.conn.commit()
        except sqlite3.IntegrityError:
            raise Exception("Email já cadastrado!")
        finally:
            self.close()

    def update_client(self, client_id: int, nome: str, email: str) -> None:
        """Atualiza os dados de um cliente existente."""
        self.connect()
        try:
            self.cursor.execute("UPDATE clientes SET nome = ?, email = ? WHERE id = ?", (nome, email, client_id))
            if self.cursor.rowcount == 0:
                raise Exception("Cliente não encontrado!")
            self.conn.commit()
        except sqlite3.IntegrityError:
            raise Exception("Email já cadastrado!")
        finally:
            self.close()

    def delete_client(self, client_id: int) -> None:
        """Exclui um cliente do banco de dados."""
        self.connect()
        try:
            self.cursor.execute("DELETE FROM clientes WHERE id = ?", (client_id,))
            if self.cursor.rowcount == 0:
                raise Exception("Cliente não encontrado!")
            self.conn.commit()
        finally:
            self.close()

    def get_clients(self) -> List[Tuple]:
        """Retorna todos os clientes do banco de dados."""
        self.connect()
        try:
            self.cursor.execute("SELECT id, nome, email FROM clientes")
            clients = self.cursor.fetchall()
            return clients
        finally:
            self.close()

    def get_client_id_by_name(self, nome: str) -> int:
        """Retorna o ID do cliente com base no nome."""
        self.connect()
        try:
            self.cursor.execute("SELECT id FROM clientes WHERE nome = ?", (nome,))
            result = self.cursor.fetchone()
            if not result:
                raise Exception("Cliente não encontrado!")
            return result[0]
        finally:
            self.close()

    def add_order(self, cliente_id: int, produto: str, valor: float) -> None:
        """Adiciona um novo pedido ao banco de dados."""
        self.connect()
        try:
            self.cursor.execute("INSERT INTO pedidos (cliente_id, produto, valor) VALUES (?, ?, ?)", 
                            (cliente_id, produto, valor))
            self.conn.commit()
        except sqlite3.IntegrityError:
            raise Exception("Cliente não encontrado!")
        finally:
            self.close()

    def update_order(self, order_id: int, cliente_id: int, produto: str, valor: float) -> None:
        """Atualiza os dados de um pedido existente."""
        self.connect()
        try:
            self.cursor.execute("UPDATE pedidos SET cliente_id = ?, produto = ?, valor = ? WHERE id = ?",
                            (cliente_id, produto, valor, order_id))
            if self.cursor.rowcount == 0:
                raise Exception("Pedido não encontrado!")
            self.conn.commit()
        except sqlite3.IntegrityError:
            raise Exception("Cliente não encontrado!")
        finally:
            self.close()

    def delete_order(self, order_id: int) -> None:
        """Exclui um pedido do banco de dados."""
        self.connect()
        try:
            self.cursor.execute("DELETE FROM pedidos WHERE id = ?", (order_id,))
            if self.cursor.rowcount == 0:
                raise Exception("Pedido não encontrado!")
            self.conn.commit()
        finally:
            self.close()

    def get_orders(self) -> List[Tuple]:
        """Retorna todos os pedidos com o nome do cliente."""
        self.connect()
        try:
            self.cursor.execute("""
                SELECT p.id, c.nome, p.produto, p.valor 
                FROM pedidos p 
                JOIN clientes c ON p.cliente_id = c.id
            """)
            orders = self.cursor.fetchall()
            return orders
        finally:
            self.close()