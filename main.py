import wave
from dtmf import convertDTMF

#TODO LIST :
#-rendre le son plus propre :
	#- fade in/out (moduler l'ampli durant la génération)
	#- des vraies pauses (j'ai pas trouvé comment :/)
#refactoriser genWave?
#-gui?

#le nombre demandé est une string car d'après le standard DTMF il peut contenir les lettres de A à D
nb = str(input("Dial: "))

duree = 0.1 #nombres de secondes pour un chiffre du numéro
#note : la durée de la pause entre 2 tonalités = duree/2
f = 8000 #fréquence de sample
amp = 127.5 #255/2

print("Generating...")
finalList, spl = convertDTMF(nb, f, duree, amp)
#NOTE : pourquoi utiliser une liste pour produire le fichier final?
#parce qu'on appelle writeframes une seule fois, ce qui réduit le temps de génération du fichier
with wave.open(nb+".wav", "w") as snd:
	#nombre de canaux, taille d'encodage, fréquence, nombre de samples
	snd.setparams((1,1,f,spl,"NONE","not compressed"))
	snd.writeframes(b''.join(finalList))