import customtkinter as ctk
from tkinter import *
import sqlite3
from tkinter import messagebox
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
import mplfinance as mpf



class BackEnd():
    def conecta_db(self):
        self.conn = sqlite3.connect("Sistema_cadastros.db")
        self.cursor = self.conn.cursor()
        print("Banco de dados conectado")

    def desconecta_db(self):
        self.conn.close()
        print("Banco de dados desconectado")    

    def cria_tabela(self):
        self.conecta_db()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Usuarios(
                Id INTEGER PRIMARY KEY AUTOINCREMENT, 
                Username TEXT NOT NULL,
                Email TEXT NOT NULL,
                Senha TEXT NOT NULL,
                Confirma_Senha TEXT NOT NULL
            );
        """)
        self.conn.commit()
        print("Tabela criada com sucesso!")
        self.desconecta_db()

    def cadastrar_usuario(self):
        self.username_cadastro = self.username_cadastro_entry.get()
        self.email_cadastro = self.email_cadastro_entry.get()
        self.senha_cadastro = self.senha_cadastro_entry.get()
        self.confirma_senha_cadastro = self.confirma_senha_entry.get()

        self.conecta_db()

        self.cursor.execute("""
            INSERT INTO Usuarios (Username, Email, Senha, Confirma_Senha)
            VALUES (?, ?, ?, ?)""", (self.username_cadastro, self.email_cadastro, self.senha_cadastro, self.confirma_senha_cadastro))
        
        try:
            if (self.username_cadastro == "" or self.email_cadastro == "" or self.senha_cadastro == "" or self.confirma_senha_cadastro == ""):
                messagebox.showerror(title="Sistema de login", message="--ERRO87--\nPreencha todos os campo!")
            elif (len(self.username_cadastro) < 5):
                messagebox.showwarning(title="Sistema de login", message="O nome de usuário deve conter 5 caracteres")
            elif (len(self.senha_cadastro) < 5):
                messagebox.showwarning(title="Sistema de login", message="A senha deve conter 5 caracteres")
            elif (self.senha_cadastro != self.confirma_senha_cadastro):
                messagebox.showerror(title="Sistema de login", message="--ERRO87--\nA senha está diferente")
            else:
                self.conn.commit()
                messagebox.showinfo(title="Sistema de login", message=f"Parabéns {self.username_cadastro}\nCadastro feito com sucesso, aguarde alguns minutos")
                self.desconecta_db()
                self.limpa_entry_cadastro()
        except:
            messagebox.showerror(title="Sistema de login", message="Erro no processo do seu cadastro\nTente novamente")
            self.desconecta_db()

    def verifica_login(self):
        self.username_login = self.username_login_entry.get()
        self.senha_login = self.senha_login_entry.get()

        self.conecta_db()

        self.cursor.execute("""SELECT * FROM Usuarios 
                            WHERE (Username =? AND Senha =?)""", (self.username_login, self.senha_login))

        self.verifica_dados = self.cursor.fetchone() # Percorrendo na tabela usuarios 

        try:
            if (self.username_login =="" or self.senha_login== ""):
                messagebox.showwarning(title="Bot do Sistema de login", message="Preencha todos os campos!")
            elif (self.username_login in self.verifica_dados and self.senha_login in self.verifica_dados):
                messagebox.showinfo(title="Sistema de login", message=f"Parabens {self.username_login}\nLogin feito com sucesso")
                self.desconecta_db()
                self.limpa_entry_login()
                # Abrir a nova janela após o login
                main_window = MainWindow(self.username_login)
                main_window.mainloop()
        except:
            messagebox.showerror(title="Sitema de login", message="ERRO84\nDados não encontrados no sistema")
            self.desconecta_db()

class MainWindow(ctk.CTk):
    def __init__(self, username):
        super().__init__()
        self.geometry("1300x700")
        self.title(f"Bem-vindo, {username}")

        self.fig, self.ax = None, None
 
# Crie um frame principal para conter os widgets
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill=BOTH, expand=True)

        # Crie um frame para as entradas
        entry_frame = ctk.CTkFrame(main_frame)
        entry_frame.grid(row=0, column=0, padx=20, pady=20)

 # Estilo semelhante ao da tela de cadastro
        entry_style = {
            "width": 250,
            "font": ("Avant Garde", 16, "bold"),
            "corner_radius": 15
        }
        


        self.label_welcome = ctk.CTkLabel(main_frame, text=f"Bem-vindo, {username}", font=("Avant Garde", 18, "bold"))
        self.label_welcome.grid(row=0, column=1, padx=20, pady=20, columnspan=2)

        self.entry_nome_acao = ctk.CTkEntry(entry_frame, placeholder_text="Nome da ação na bolsa", **entry_style)
        self.entry_nome_acao.grid(row=1, column=0, padx=20, pady=10)

        self.entry_data_inicio = ctk.CTkEntry(entry_frame, placeholder_text="Data de início (AAAA-MM-DD)", **entry_style)
        self.entry_data_inicio.grid(row=2, column=0, padx=20, pady=10)

        self.entry_data_fim = ctk.CTkEntry(entry_frame, placeholder_text="Data de fim (AAAA-MM-DD)", **entry_style)
        self.entry_data_fim.grid(row=3, column=0, padx=20, pady=10)

        self.button_buscar_acao = ctk.CTkButton(entry_frame, text="Buscar Ação", font=("Avant Garde", 16, "bold"), command=self.buscar_acao)
        self.button_buscar_acao.grid(row=4, column=0, padx=20, pady=10)

        self.button_atualizar = ctk.CTkButton(entry_frame, text="Atualizar Gráfico", font=("Avant Garde", 16, "bold"), command=self.atualizar_grafico)
        self.button_atualizar.grid(row=5, column=0, padx=20, pady=10)

      # Crie o gráfico à direita com um tamanho menor
        self.fig, self.ax = plt.subplots(figsize=(8, 4))  # Ajusta o tamanho do gráfico
        self.canvas = FigureCanvasTkAgg(self.fig, master=main_frame)
        self.canvas.get_tk_widget().grid(row=0, column=1, rowspan=6, padx=20, pady=20)



        self.acao_data = None
        self.acao_symbol = None
        self.buscar_acao("AAPL", "2023-01-01", "2023-10-31")



    def buscar_acao(self, symbol=None, start=None, end=None):
        if symbol is None:
            symbol = self.entry_nome_acao.get()
            start = self.entry_data_inicio.get()
            end = self.entry_data_fim.get()
            
        try:
            data = yf.Ticker(symbol)
            df = data.history(start=start, end=end)

            self.acao_symbol = symbol
            self.acao_data = df

            self.atualizar_grafico()
        except Exception as e:
            print(f"Erro ao buscar dados da ação {symbol}: {e}")

    def atualizar_grafico(self):
        if self.acao_data is not None:
            if self.ax is None:
                self.fig, self.ax = plt.subplots(figsize=(8, 4))
                self.canvas = FigureCanvasTkAgg(self.fig, master=self)
                self.canvas.get_tk_widget().grid(row=0, column=1, rowspan=6, padx=20, pady=20)

            self.ax.clear()

       # Personalize o estilo do gráfico de velas usando o estilo 'classic'
        style = mpf.make_mpf_style(base_mpl_style='seaborn-darkgrid', rc={'figure.facecolor': '#333333'})

        # Defina o tamanho do gráfico de velas para um tamanho maior
        mpf.plot(self.acao_data, type='candle', style=style, title=f"Gráfico da Ação {self.acao_symbol}", ylabel='Preço', figscale=1.5, ax=self.ax)
        
        # Adicione o volume no painel inferior
        mpf.plot(self.acao_data, type='candle', style=style, title=f"Gráfico da Ação {self.acao_symbol}", ylabel='Preço', figscale=1.5, ax=self.ax)
        self.ax.set_xlabel("Data")
        self.ax.set_ylabel("Preço")
        self.ax.set_title(f"Gráfico da Ação {self.acao_symbol}")

        
        # Adicione uma média móvel exponencial (EMA) de 12 períodos
        add_plot = mpf.make_addplot([None, None, None, None, 150], panel=0, color='green', secondary_y=False)
        mpf.plot(self.acao_data, addplot=add_plot, style=style, title=f"Gráfico da Ação {self.acao_symbol}", ylabel='Preço', figscale=1.5, ax=self.ax)

        # Atualize o canvas da Figura
        self.canvas.draw()

    

    def update_grafico(self, frame):
        if hasattr(self, 'acao_symbol'):
            data = yf.Ticker(self.acao_symbol)
            df = data.history(period="1d", interval="1m")

            self.atualizar_grafico(df, self.acao_symbol)
   











class App(ctk.CTk, BackEnd):
    def __init__(self):
        super().__init__()
        self.configuracoes_da_janela_inicial()
        self.tela_de_login()
        self.cria_tabela()

    # Configurando a janela inicial
    def configuracoes_da_janela_inicial(self):
        self.geometry("700x400")
        self.title("Sistema de Login")
        self.resizable(False, False)

    def tela_de_login(self):
        # Imagem
        self.img = PhotoImage(file="pword.png")
        self.lb_img = ctk.CTkLabel(self, text=None, image=self.img)
        self.lb_img.grid(row=1, column=0, padx=10)

        # Titulos
        self.title = ctk.CTkLabel(self, text="Faça o login ou Cadastre-se\nna plataforma para acessar\na área de trabalho!", font=("Avant Garde", 14, "bold"))
        self.title.grid(row=0, column=0, pady=10, padx=10)

        # Formulario de login
        self.frame_login = ctk.CTkFrame(self, width=350, height=380)
        self.frame_login.place(x=350, y=10)

        # Widgets
        self.lb_title = ctk.CTkLabel(self.frame_login, text="Faça o seu login", font=("Avant Garde", 14, "bold"))
        self.lb_title.grid(row=0, column=0, padx=10, pady=10)

        self.username_login_entry = ctk.CTkEntry(self.frame_login, width=300, placeholder_text="Nome de usuário", font=("Avant Garde", 16, "bold"), corner_radius=15)
        self.username_login_entry.grid(row=1, column=0, pady=10, padx=10)

        self.senha_login_entry = ctk.CTkEntry(self.frame_login, width=300, placeholder_text="PIN", font=("Avant Garde", 16, "bold"), corner_radius=15, show="•")
        self.senha_login_entry.grid(row=2, column=0, pady=10, padx=10)

        self.ver_senha = ctk.CTkCheckBox(self.frame_login, text="Ver senha", font=("Avant Garde", 14, "bold"), corner_radius=20)
        self.ver_senha.grid(row=3, column=0, pady=10, padx=10)

        self.btn_login = ctk.CTkButton(self.frame_login, width=300, text="Fazer login".upper(),  font=("Avant Garde", 16, "bold"), corner_radius=15, command=self.verifica_login)
        self.btn_login.grid(row=4, column=0, pady=10, padx=10)

        self.spam = ctk.CTkLabel(self.frame_login, text="Se não tem conta, clique no botão abaixo para se\ncadastrar no sistema", font=("Avant Garde", 10, "bold"))
        self.spam.grid(row=5, column=0, pady=10, padx=10)

        self.btn_cadastro = ctk.CTkButton(self.frame_login, width=300, fg_color="green", hover_color="#050", text="Fazer Cadastro".upper(), font=("Avant Garde", 16, "bold"), corner_radius=15, command=self.tela_de_cadastro)
        self.btn_cadastro.grid(row=6, column=0, pady=10, padx=10)
        

    def tela_de_cadastro(self):
        # Remover o formulario de login
        self.frame_login.place_forget()

        # frame cadastro
        self.frame_cadastro = ctk.CTkFrame(self, width=350, height=380)
        self.frame_cadastro.place(x=350, y=10)

        # Título 
        self.lb_title = ctk.CTkLabel(self.frame_cadastro, text="Faça o seu login", font=("Avant Garde", 14, "bold"))
        self.lb_title.grid(row=0, column=0, padx=10, pady=10)

        # Widgets cadastro
        self.username_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="Seu nome de usuário", font=("Avant Garde", 16, "bold"), corner_radius=15)
        self.username_cadastro_entry.grid(row=1, column=0, pady=5, padx=10)

        self.email_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="Email de usuário", font=("Avant Garde", 16, "bold"), corner_radius=15)
        self.email_cadastro_entry.grid(row=2, column=0, pady=5, padx=10)

        self.senha_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="PIN", font=("Avant Garde", 16, "bold"), corner_radius=15, show="•")
        self.senha_cadastro_entry.grid(row=3, column=0, pady=5, padx=10)

        self.confirma_senha_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="Confirmar PIN", font=("Avant Garde", 16, "bold"), corner_radius=15, show="•")
        self.confirma_senha_entry.grid(row=4, column=0, pady=5, padx=10)

        self.ver_senha = ctk.CTkCheckBox(self.frame_cadastro, text="Clique para ver a senha", font=("Avant Garde", 14, "bold"), corner_radius=20)
        self.ver_senha.grid(row=5, column=0, pady=5)

        self.btn_cadastrar_user = ctk.CTkButton(self.frame_cadastro, width=300, fg_color="green", hover_color="#050", text="Fazer cadastro".upper(), font=("Avant Garde", 16, "bold"), corner_radius=15, command=self.cadastrar_usuario)
        self.btn_cadastrar_user.grid(row=6, column=0, pady=5, padx=10)

        self.btn_login_back = ctk.CTkButton(self.frame_cadastro, width=300, text="Voltar ao login".upper(), font=("Avant Garde", 16, "bold"), corner_radius=15, fg_color="#444", hover_color="#333", command=self.tela_de_login)
        self.btn_login_back.grid(row=7, column=0, pady=10, padx=10)

    def limpa_entry_cadastro(self):
        self.username_cadastro_entry.delete(0, END)
        self.email_cadastro_entry.delete(0, END)
        self.senha_cadastro_entry.delete(0, END)
        self.confirma_senha_entry.delete(0, END)

    def limpa_entry_login(self):
        self.username_login_entry.delete(0, END)
        self.senha_login_entry.delete(0, END)




if __name__ == "__main__":
    app = App()
    app.mainloop()






