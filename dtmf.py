import wave
from math import sin, pi

#variable qui associe un chiffre/une lettre à deux fréquences
dtmf = {
	'1': (1209,697),
	'2': (1336,697),
	'3': (1477,697),
	'A': (1633,697),
	'4': (1209,770),
	'5': (1336,770),
	'6': (1477,770),
	'B': (1633,770),
	'7': (1209,852),
	'8': (1336,852),
	'9': (1477,852),
	'C': (1633,852),
	'*': (1209,941),
	'0': (1336,941),
	'#': (1477,941),
	'D': (1633,941),
}

def genWave(j, freq0, freq1, freq2, amp):
	#ux = 2 * pi * (freqx/freq0)
	u1 = 2 * pi * (freq1/freq0)
	u2 = 2 * pi * (freq2/freq0)
	#résultat = amplitude + 63*sin(u1*j) + 63*sin(u2*j) 
	return int(amp + 63*sin(u1*j) + 63*sin(u2*j))

def convertDTMF(number, freq, duree, amp):
	finalSND = [] #les samples seront placés dedans
	splTon = duree*len(number)*freq #nombre total de samples pour les tonalités
	splPoz = (duree/2*freq)*len(number) #nombre total de samples pour les pauses
	spl = int(splTon+splPoz) #duree totale en samples
	for i in number: #pour chaque chiffre
		for j in range(0,int(duree*freq)): #pour chaque sample
				freq1 = dtmf[i][0] #on prend la première valeur associée au chiffre
				freq2 = dtmf[i][1] #et la seconde
				res = genWave(j, freq, freq1, freq2, amp)
				finalSND.append(wave.struct.pack("B",res))
		for k in range(0,int(duree/2*freq)):
		 	finalSND.append(wave.struct.pack("B",0))
	return finalSND, spl