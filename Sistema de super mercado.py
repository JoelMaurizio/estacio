import tkinter as tk
from tkinter import messagebox, simpledialog

class Produto:
    def __init__(self, codigo, nome, preco):
        self.codigo = codigo
        self.nome = nome
        self.preco = preco

class Carrinho:
    def __init__(self):
        self.itens = {}
    
    def adicionar_produto(self, produto, quantidade):
        if produto.codigo in self.itens:
            self.itens[produto.codigo]['quantidade'] += quantidade
        else:
            self.itens[produto.codigo] = {'produto': produto, 'quantidade': quantidade}
    
    def remover_produto(self, codigo, quantidade):
        if codigo in self.itens:
            if self.itens[codigo]['quantidade'] <= quantidade:
                del self.itens[codigo]
            else:
                self.itens[codigo]['quantidade'] -= quantidade
    
    def calcular_total(self):
        total = 0
        for item in self.itens.values():
            total += item['produto'].preco * item['quantidade']
        return total
    
    def listar_itens(self):
        return [(item['produto'].nome, item['produto'].preco, item['quantidade']) for item in self.itens.values()]

class SistemaCaixa:
    def __init__(self):
        self.produtos = {}
        self.carrinho = Carrinho()
    
    def adicionar_produto(self, codigo, nome, preco):
        self.produtos[codigo] = Produto(codigo, nome, preco)
    
    def listar_produtos(self):
        return [(produto.codigo, produto.nome, produto.preco) for produto in self.produtos.values()]
    
    def adicionar_ao_carrinho(self, codigo, quantidade):
        if codigo in self.produtos:
            produto = self.produtos[codigo]
            self.carrinho.adicionar_produto(produto, quantidade)
        else:
            return f"Produto com código {codigo} não encontrado."
    
    def remover_do_carrinho(self, codigo, quantidade):
        self.carrinho.remover_produto(codigo, quantidade)
    
    def finalizar_compra(self):
        itens = self.carrinho.listar_itens()
        total = self.carrinho.calcular_total()
        return itens, total

class App:
    def __init__(self, root):
        self.sistema = SistemaCaixa()
        
        # Inicializando produtos
        self.sistema.adicionar_produto('001', 'Arroz', 25.50)
        self.sistema.adicionar_produto('002', 'Feijão', 7.30)
        self.sistema.adicionar_produto('003', 'Macarrão', 4.80)
        
        self.root = root
        self.root.title("Sistema de Caixa de Supermercado")
        
        self.frame = tk.Frame(root)
        self.frame.pack(padx=10, pady=10)
        
        # Registro de produtos
        self.label_registro = tk.Label(self.frame, text="Registrar Novo Produto")
        self.label_registro.pack()
        
        self.label_codigo = tk.Label(self.frame, text="Código:")
        self.label_codigo.pack()
        self.entry_codigo = tk.Entry(self.frame)
        self.entry_codigo.pack()
        
        self.label_nome = tk.Label(self.frame, text="Nome:")
        self.label_nome.pack()
        self.entry_nome = tk.Entry(self.frame)
        self.entry_nome.pack()
        
        self.label_preco = tk.Label(self.frame, text="Preço:")
        self.label_preco.pack()
        self.entry_preco = tk.Entry(self.frame)
        self.entry_preco.pack()
        
        self.btn_registrar = tk.Button(self.frame, text="Registrar Produto", command=self.registrar_produto)
        self.btn_registrar.pack()
        
        # Passar compras
        self.label_produtos = tk.Label(self.frame, text="Produtos Disponíveis:")
        self.label_produtos.pack()
        
        self.lista_produtos = tk.Listbox(self.frame)
        self.lista_produtos.pack()
        
        self.label_codigo_carrinho = tk.Label(self.frame, text="Código:")
        self.label_codigo_carrinho.pack()
        self.entry_codigo_carrinho = tk.Entry(self.frame)
        self.entry_codigo_carrinho.pack()
        
        self.label_quantidade = tk.Label(self.frame, text="Quantidade:")
        self.label_quantidade.pack()
        self.entry_quantidade = tk.Entry(self.frame)
        self.entry_quantidade.pack()
        
        self.btn_adicionar = tk.Button(self.frame, text="Adicionar ao Carrinho", command=self.adicionar_ao_carrinho)
        self.btn_adicionar.pack()
        
        self.btn_remover = tk.Button(self.frame, text="Remover do Carrinho", command=self.remover_do_carrinho)
        self.btn_remover.pack()
        
        self.btn_finalizar = tk.Button(self.frame, text="Finalizar Compra", command=self.finalizar_compra)
        self.btn_finalizar.pack()
        
        # Atualiza a lista de produtos
        self.atualizar_lista_produtos()
    
    def atualizar_lista_produtos(self):
        self.lista_produtos.delete(0, tk.END)
        for codigo, nome, preco in self.sistema.listar_produtos():
            self.lista_produtos.insert(tk.END, f"Código: {codigo} | Nome: {nome} | Preço: R${preco:.2f}")

    def registrar_produto(self):
        codigo = self.entry_codigo.get()
        nome = self.entry_nome.get()
        try:
            preco = float(self.entry_preco.get())
            self.sistema.adicionar_produto(codigo, nome, preco)
            self.atualizar_lista_produtos()
            messagebox.showinfo("Sucesso", f"Produto {nome} registrado com sucesso.")
        except ValueError:
            messagebox.showerror("Erro", "Preço deve ser um número.")

    def adicionar_ao_carrinho(self):
        codigo = self.entry_codigo_carrinho.get()
        try:
            quantidade = int(self.entry_quantidade.get())
            mensagem = self.sistema.adicionar_ao_carrinho(codigo, quantidade)
            if mensagem:
                messagebox.showerror("Erro", mensagem)
        except ValueError:
            messagebox.showerror("Erro", "Quantidade deve ser um número inteiro.")
    
    def remover_do_carrinho(self):
        codigo = self.entry_codigo_carrinho.get()
        try:
            quantidade = int(self.entry_quantidade.get())
            self.sistema.remover_do_carrinho(codigo, quantidade)
        except ValueError:
            messagebox.showerror("Erro", "Quantidade deve ser um número inteiro.")
    
    def finalizar_compra(self):
        itens, total = self.sistema.finalizar_compra()
        itens_str = "\n".join([f"{nome} - R${preco:.2f} x {quantidade} = R${(preco * quantidade):.2f}" for nome, preco, quantidade in itens])
        mensagem = f"Itens no carrinho:\n{itens_str}\n\nTotal a pagar: R${total:.2f}"
        messagebox.showinfo("Resumo da Compra", mensagem)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
