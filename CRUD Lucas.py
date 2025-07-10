
import sqlite3
import bcrypt
import tkinter as tk
from tkinter import messagebox

# Conexão com banco de dados
conn = sqlite3.connect('usuarios.db')
cursor = conn.cursor()

# Criar tabela
cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL
    )
''')
conn.commit()

# Funções auxiliares para senha
def hash_senha(senha):
    return bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verificar_senha(senha_informada, senha_hash):
    return bcrypt.checkpw(senha_informada.encode('utf-8'), senha_hash.encode('utf-8'))

# Janela principal
janela = tk.Tk()
janela.title("Cadastro de Usuários")
janela.geometry("500x400")

# Funções de interface
def cadastrar():
    nome = entrada_nome.get()
    email = entrada_email.get()
    senha = entrada_senha.get()

    if not nome or not email or not senha:
        messagebox.showwarning("Campos vazios", "Preencha todos os campos.")
        return

    senha_hash = hash_senha(senha)
    try:
        cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)", (nome, email, senha_hash))
        conn.commit()
        messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
        entrada_nome.delete(0, tk.END)
        entrada_email.delete(0, tk.END)
        entrada_senha.delete(0, tk.END)
    except sqlite3.IntegrityError:
        messagebox.showerror("Erro", "Email já cadastrado.")

def listar():
    cursor.execute("SELECT id, nome, email FROM usuarios")
    usuarios = cursor.fetchall()
    texto = "\n".join([f"ID: {u[0]} | Nome: {u[1]} | Email: {u[2]}" for u in usuarios])
    messagebox.showinfo("Usuários Cadastrados", texto if texto else "Nenhum usuário encontrado.")

def editar():
    
    id_usuario = input("ID do usuário que deseja editar: ")
    novo_nome = input("Novo nome: ")
    novo_email = input("Novo email: ")
    nova_senha = input("Nova senha: ")
    nova_senha_hash = hash_senha(nova_senha)
    try:
        cursor.execute("UPDATE usuarios SET nome=?, email=?, senha=? WHERE id=?", (novo_nome, novo_email, nova_senha_hash, id_usuario))
        conn.commit()
        if cursor.rowcount:
            print("Usuário atualizado com sucesso!\n")
        else:
            print("Usuário não encontrado.\n")
    except sqlite3.IntegrityError:
        print("Erro: esse email já está sendo usado")

def excluir():
    id_usuario = input("ID do usuário que deseja excluir: ")
    cursor.execute("DELETE FROM usuarios WHERE id=?", (id_usuario,))
    conn.commit()
    if cursor.rowcount:
        print("Usuário excluído com sucesso!\n")
    else:
        print("Usuário não encontrado.\n")  
    
def login():
    email = entrada_email.get()
    senha = entrada_senha.get()
    cursor.execute("SELECT senha FROM usuarios WHERE email=?", (email,))
    resultado = cursor.fetchone()
    if resultado and verificar_senha(senha, resultado[0]):
        messagebox.showinfo("Login", "Login bem-sucedido!")
    else:
        messagebox.showerror("Erro", "Email ou senha incorretos.")



# Widgets
tk.Label(janela, text="Nome").pack()
entrada_nome = tk.Entry(janela)
entrada_nome.pack()

tk.Label(janela, text="Email").pack()
entrada_email = tk.Entry(janela)
entrada_email.pack()

tk.Label(janela, text="Senha").pack()
entrada_senha = tk.Entry(janela, show="*")
entrada_senha.pack()

tk.Button(janela, text="Cadastrar", command=cadastrar, bg="#4CAF50", fg="white").pack(pady=5)
tk.Button(janela, text="Listar Usuários", command=listar, bg="#9C27B0", fg="white").pack(pady=5)
tk.Button(janela, text="Editar Usuário", command =editar, bg= "#4C5A85", fg="black").pack(pady=5)
tk.Button(janela, text="Excluir", command =excluir, bg= "#FF5100", fg="black").pack(pady=5)
tk.Button(janela, text="Login", command=login, bg="#2196F3", fg="white").pack(pady=5)
tk.Button(janela, text="Sair", command=janela.quit, bg="#F700FF", fg="white").pack(pady=5)


# Iniciar interface
janela.mainloop()

# Fechar conexão
conn.close()
