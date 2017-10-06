from tkinter import *
import sqlite3
import socket
import threading
import queue
import clienteudpgui
HOST = '127.0.0.1'
PORT = 80
class Banco():
	def __init__(self):
		self.conexao = sqlite3.connect('login_signin.db')
		self.createTable()

	def createTable(self):
		c=self.conexao.cursor()

		c.execute("""create table if not exists usuarios (
					 idusuario integer primary key autoincrement ,
					 nome text,
					 usuario text,
					 senha text)""")
		self.conexao.commit()
		c.close()

class Login:
	user="user"
	def __init__(self,master=None):
		self.master=master
		
		self.primeiroContainer = Frame(master)
		self.primeiroContainer.pack()

		self.segundoContainer = Frame(master)
		self.segundoContainer.pack()

		self.terceiroContainer = Frame(master)
		self.terceiroContainer.pack()

		self.quartoContainer = Frame(master)
		self.quartoContainer.pack()

		self.titulo = Label(self.primeiroContainer, text="Dados do usuário")
		self.titulo.pack()

		self.nomeLabel = Label(self.segundoContainer, text="Usuário")
		self.nomeLabel.pack()

		self.nome = Entry(self.segundoContainer)
		self.nome.bind("<Return>",self.noenter)
		self.nome.pack(side=LEFT)

		self.senhaLabel = Label(self.terceiroContainer, text="Senha")
		self.senhaLabel.pack()

		self.senha = Entry(self.terceiroContainer)
		self.senha["show"]="*"
		self.senha.bind("<Return>",self.noenter)
		self.senha.pack(side=LEFT)

		self.autenticar = Button(self.quartoContainer)
		self.autenticar["text"] = "Autenticar"
		self.autenticar["command"] = self.verificaSenha
		self.autenticar.pack()

		self.signin = Button(self.quartoContainer)
		self.signin["text"] = "Sign In"
		self.signin["command"] = self.chamaSignin
		self.signin.pack()

		self.mensagem = Label(self.quartoContainer,text="")
		self.mensagem.pack()

		self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.udp.setblocking(False)
		self.dest=(HOST,PORT)
		
		
	def verificaSenha(self):
		
		self.enviarlogin()
		self.result=("").encode()
		while self.result.decode() == "":
			try:
				self.result,self.srv = self.udp.recvfrom(1024)
			except:
				pass
		if self.result.decode() == "success":
			self.mensagem["text"] = "Autenticado"
			Login.user=self.user
			self.udp.close()
			self.chamarChat()
		if self.result.decode() == "wpassword":
			self.mensagem["text"] =	"Senha incorreta"
			self.senha.delete(0,'end')
		if self.result.decode() == "usernotfound":
			self.mensagem["text"] =	"Usuário incorreto"
			self.senha.delete(0,'end')

	def noenter(self,event):
		self.verificaSenha()

	def chamaSignin(self):
		self.master.destroy()
		root2=Tk()
		root2.wm_title("Sign In")
		Signin(root2)
		root2.mainloop()

	def enviarlogin(self):
		try:
			self.user = self.nome.get()
			self.password = self.senha.get()
			self.stats = "login"
			if self.user != "":
				self.udp.sendto(self.stats.encode(),self.dest)
				self.udp.sendto(self.user.encode(),self.dest)
				self.udp.sendto(self.password.encode(),self.dest)

		except :
			pass
	def chamarChat(self):
		
		root2 = Tk()
		root2.wm_title("Chat")
		clienteudpgui.username = self.user
		clienteudpgui.parteGrafica(root2)

		self.master.destroy()
		root2.mainloop()
		
		

class Signin:
	def __init__(self,master=None):

		self.master = master

		self.primeiroContainer = Frame(master)
		self.primeiroContainer.pack()

		self.segundoContainer = Frame(master)
		self.segundoContainer.pack()

		self.terceiroContainer = Frame(master)
		self.terceiroContainer.pack()

		self.quartoContainer = Frame(master)
		self.quartoContainer.pack()

		self.quintoContainer = Frame(master)
		self.quintoContainer.pack()

		self.sextoContainer = Frame(master)
		self.sextoContainer.pack()

		self.setimoContainer = Frame(master)
		self.setimoContainer.pack()

		self.oitavoContainer = Frame(master)
		self.oitavoContainer.pack()

		self.titulo = Label(self.primeiroContainer,text="Sign In")
		self.titulo.pack()

		self.nomeCLabel = Label(self.segundoContainer,text="Nome Completo")
		self.nomeCLabel.pack()
		self.erronomeC = Label(self.segundoContainer,text="",fg="red")
		self.erronomeC.pack(side=BOTTOM)

		self.nomeC = Entry(self.segundoContainer)
		self.nomeC.pack()

		self.nickLabel = Label(self.terceiroContainer,text="Nome de Usuário")
		self.nickLabel.pack()
		
		self.erronick = Label(self.terceiroContainer,text="",fg="red")
		self.erronick.pack(side=BOTTOM)

		self.nick = Entry(self.terceiroContainer)
		self.nick.pack()

		self.senhaLabel = Label(self.quartoContainer,text="Senha")
		self.senhaLabel.pack()

		self.errosenha = Label(self.quartoContainer,text="",fg="red")
		self.errosenha.pack(side=BOTTOM)

		self.senha = Entry(self.quartoContainer,show="*")
		self.senha.pack()

		self.minsenha = Label(self.quartoContainer,text="Mínimo 6 dígitos")
		self.minsenha.pack(side=RIGHT)

		self.CsenhaLabel = Label(self.quintoContainer,text="Comfirmação de Senha")
		self.CsenhaLabel.pack()

		self.erroCsenha = Label(self.quintoContainer,text="",fg="red")
		self.erroCsenha.pack(side=BOTTOM)

		self.Csenha = Entry(self.quintoContainer,show="*")
		self.Csenha.pack()

		self.enviar = Button(self.sextoContainer,text="Enviar",command=self.verificaSignin)
		self.enviar.pack()
		self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.udp.setblocking(False)
		self.dest=(HOST,PORT)

	def verificaSignin(self):
		nomeC=self.nomeC.get()
		nick=self.nick.get()
		senha=self.senha.get()
		Csenha=self.Csenha.get()
		self.erronomeC["text"]=""
		self.erronick["text"]=""
		self.errosenha["text"]=""
		self.erroCsenha["text"]=""
		ok=True
		if nomeC == "" :
			ok=False
			self.erronomeC["text"]="Campo Obrigatório"
		if nick == "" :
			ok=False
			self.erronick["text"]="Campo Obrigatório"
		if senha == "" :
			ok=False
			self.errosenha["text"]="Campo Obrigatório"
		if Csenha == "" :
			ok=False
			self.erroCsenha["text"]="Campo Obrigatório"	
		if len(senha) < 6 :
			ok=False
			self.errosenha["text"]="Senha muito curta"
		if senha != Csenha :
			ok=False
			self.erroCsenha["text"]="As senhas devem coincidir"
		if ok:
			self.stats = "signin"
			self.udp.sendto(self.stats.encode(),self.dest)

			self.udp.sendto(nomeC.encode(),self.dest)
			self.udp.sendto(nick.encode(),self.dest)
			self.udp.sendto(senha.encode(),self.dest)
			self.reply=("").encode()
			while self.reply.decode() == "":
				try:
					self.reply,self.srv = self.udp.recvfrom(1024)
				except:
					pass
			print("recebo reply:", self.reply.decode())
			if self.reply.decode() == "useralready": 
				self.erronick["text"]="Usuário já existe"
			
			if self.reply.decode() == "ok" :
				top = Toplevel()
				top.title("Sucesso")
				msg = Message(top,text="Sign In completado com sucesso")
				msg.pack()
				fechar = Button(top,text="Fechar",command=self.chamaLogin)
				fechar.pack()
				
					
			if self.reply.decode() == "fail":
				top = Toplevel()
				top.title("Oops")
				msg = Message(top,text="Sign In não completado com sucesso")
				msg.pack()
				fechar = Button(top,text="Fechar",command=top.destroy)
				fechar.pack()

	def chamaLogin(self):
		root2=Tk()
		root2.wm_title("Login")
		self.master.destroy()
		Login(root2)
		


root = Tk()
root.wm_title("Login")
Login(root)
root.mainloop()
root.destroy()
