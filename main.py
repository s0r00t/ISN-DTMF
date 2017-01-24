#TODO:
#  -peaufiner la GUI
#  -implémenter menu secret?
from tkinter import *
#NOTE: même avec ttk tkinter reste dégueulasse sous linux. à étudier
from tkinter.ttk import *
from dtmf import convertDTMF
from wave import open

dialWindow = Tk()
dialWindow.title("DTMF Dialer")
#NOTE: le nombre demandé est une string car d'après le standard DTMF il peut contenir les lettres de A à D
number = StringVar()
#définition des styles des différents widgets
#les boutons de numérotation
Style(dialWindow).configure("Dial.TButton", padding=5)
#le numéro qui va être "appelé"
Style(dialWindow).configure("Nummern.TLabel", font="serif 20")
#le bouton d'appel
Style(dialWindow).configure("Call.TButton", background="white", font="serif 30", width=3, foreground="green")
#le bouton pour raccrocher
Style(dialWindow).configure("Hang.TButton", background="white", font="serif 30", width=3, foreground="red")

def appendNumber(digit):
	"""
	"Callback" appelée dès qu'un bouton de composition est pressé.
	"""
	global number
	if len(number.get()) < 10:
		number.set(number.get()+digit)

def dialNumber():
	"""
	Convertit le numéro donné en tonalités DTMF avec l'aide des fonctions définies
	dans dtmf.py.
	"""
	nb = number.get()
	if nb == '': return #on évite de créer un fichier vide si il n'y a pas de numéro
	finalList, spl = convertDTMF(nb, f, duree, amp)
	#NOTE: pourquoi utiliser une liste afin de stocker les signaux?
	#parce qu'ainsi writeframes n'est appelé qu'une seule fois, et cela
	#accélère beaucoup la vitesse de traitement.
	with open(nb+".wav", "w") as snd:
		#nombre de canaux, taille d'encodage, fréquence, nombre de samples 
		#(les deux derniers paramètres désactivent la compression)
		snd.setparams((1,1,f,spl,"NONE","not compressed"))
		snd.writeframes(b''.join(finalList))
	number.set('') #on réinitialise le numéro

#le numéro en train d'être composé
Label(dialWindow, textvariable=number, style="Nummern.TLabel").grid(row=0, column=0, columnspan=10)

#les touches du clavier
DTMFKey = ['1','2','3','4','5','6','7','8','9','*','0','#']
#cette variable permet d'utiliser DTMFKey par groupes de 3
start = 0 
#pour chaque ligne...
for i in range(1, 5):
	#...et chaque colonne
	for j in range(3):
		digit = DTMFKey[start+j]
		#l'usage d'une fonction lambda permet d'appeler une fonction et de préciser ses paramètres
		#digit=digit permet de définir l'argument de la fonction comme étant le numéro du bouton
		digitBut = Button(dialWindow, text=digit, width=10, style="Dial.TButton", command=lambda digit=digit: appendNumber(digit))
		digitBut.grid(row=i,column=j)
	start = start+3

duree = 0.1 #nombres de secondes pour un chiffre du numéro
#note : la durée de la pause entre 2 tonalités = duree/2
f = 8000 #fréquence de sample
amp = 127.5 #255/2

Button(dialWindow, text='✆', style="Call.TButton", command=dialNumber).grid(row=5,column=0)
Button(dialWindow, text='☎', style="Hang.TButton", command=lambda: number.set('')).grid(row=5,column=2)

dialWindow.mainloop()
