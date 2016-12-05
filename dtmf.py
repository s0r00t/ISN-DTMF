import sys
import wave
import math

#TODO LIST :
#-implémenter lettres (réécrire la vérif de l'input, l'objet dtmf et son utilisation)
#-rendre le son plus propre :
	#- fade in/out (moduler l'ampli durant la génération)
	#- des vraies pauses (j'ai pas trouvé comment :/)
#refactoriser le code
#-gui?

#0 1 2 3 4 5 6 7 8 9
#letters not implemnted
dtmf = [(1336,941),(1209,697),(1336,697),(1477,697),(1209,770),(1336,770),(1477,770),(1209,852),(1336,852),(1477,852)]
final_snd = []

#le nombre demandé est une string car d'après le standard DTMF il peut contenir les lettres de A à D
nb = str(input("Dial: "))
if nb != "502007" and len(nb) > 10:
		print("Too long!")
		sys.exit(1)

duree = 0.1 #nombres de secondes pour un chiffre du numéro
#note : la durée de la pause entre 2 tonalités = duree/2
f = 8000 #fréquence de sample
amp = 127.5 #255/2
#duree*len(nb)*f = nombre total de samples pour les tonalités
#(duree/2*f)*len(nb) = nombre total de samples pour les pauses
spl = int(duree*len(nb)*f+(duree/2*f)*len(nb)) #duree totale en samples
print("Samples: "+str(spl))
print("Generating...")
for i in nb:
		for j in range(0,int(duree*f)):
				res = int(amp+63*math.sin((2*math.pi*(dtmf[int(i)][0])/f)*j)+63*math.sin((2*math.pi*(dtmf[int(i)][1])/f)*j))
				final_snd.append(wave.struct.pack("B",res))
		for k in range(0,int(duree/2*f)):
		 	final_snd.append(wave.struct.pack("B",0))

#NOTE : pourquoi utiliser une liste pour produire le fichier final?
#parce qu'on appelle writeframes une seule fois, ce qui réduit le temps de génération du fichier
with wave.open(nb+".wav", "w") as snd:
	#nombre de canaux, taille d'encodage, fréquence, nombre de samples
	snd.setparams((1,1,f,spl,"NONE","not compressed"))
	snd.writeframes(b''.join(final_snd))