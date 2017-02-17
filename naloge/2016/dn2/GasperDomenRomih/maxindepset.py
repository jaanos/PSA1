from .utils import directet_tree
import sys
import random
import time
sys.setrecursionlimit(10000)

def maxIndependentSet(T, w):
	"""
	Najtežja neodvisna množica
	v kartezičnem produktu cikla C_k in drevesa T z n vozlišči,
	kjer ima tabela tež w dimenzije kxn (k >=2).

	Vrne par (c, s), kjer je c teža najdene neodvisne množice,
	s pa je seznam vozlišč v neodvisni množici,
	torej seznam parov oblike (i, u) (0 <= i <= k-1, 0 <= u <= n-1).
	"""
	n = len(T)

	assert all(len(r) == n for r in w), \
		"Dimenzije tabele tež ne ustrezajo številu vozlišč v drevesu!"
	assert all(all(u in T[v] for v in a) for u, a in enumerate(T)), \
		"Podani graf ni neusmerjen"

	k = len(w)
	podmnozice = {}
	ustrezne = {}
	slovar_utezi = {}	
	#vse podmnožice cikla, kjer poljubna 2 elementa nista sosednja, predstavljene v
	#obliki binarnega zapisa dolžine k
	for i in range (2**k):
		binary = bin(i)[2:].zfill(k)
		podmnozica = list(map(int, binary)) #seznam ničel in enic
		veljavna = True

		#preverimo, če sta dve enici zapored -> v kartezičnem produktu bosta sosednji,
		#sepravi ta podmnožica cikla ni ustrezna
		for j in range(len(binary) - 1):
			if podmnozica[j] == podmnozica[j+1] == 1:
				veljavna = False
				break

		#preverimo še prvi in zadnji element
		if podmnozica[0] == podmnozica[-1] == 1:
			veljavna = False

		#če je podmnožica veljavna jo dodamo v slovar, kjer je ključ desetiško število,
		#ki predstavlja to množico
		if veljavna:
			podmnozice[i]= podmnozica

	#za vsako podmnozico določimo, nje ustrezne podmnožice tj. na istem mestu nimata enice
	for i in podmnozice:
		ustrezne[i] = []
		for j in podmnozice:
			if i & j == 0:				
				ustrezne[i].append(j)

	#za vsak ustrezen cikel ter vozlisce v dreveru T dolocimo njuno tezo
	for i in ustrezne:
		for j in range(n):
			teza = 0
			for l in range(k):				
				teza += podmnozice[i][l]*w[l][j]			
			slovar_utezi[(i,j)] = teza

	T = directet_tree(T)
	
	#v memo si bomo shranjevali vmesne rezultate
	memo = dict()

	def recursive_max_subset(vozlisce, cikel):
		#zaustavitveni pogoj rekurzije: če par (vozlisce, cikel) že pojavlja v memo,
		#vrnemo pripadajočo vrednost
		if (vozlisce, cikel) in memo:
			return memo[(vozlisce, cikel)]
		#seznam vozlišč v najtežji množici
		vozlisca = []

		#teža najtežje množice(na začetku 0)
		maks_teza = 0

		#na vsakem vozlišču bomo pregledali, vse cikle, ki ustrezajo podanemu ciklu(cikel),
		#ter za vsak tak cikel izračunali največjo težo podmnožice za vsakega od potomcev podanega vozlisca(vozlisce)
		for ustrezen in ustrezne[cikel]:
			
			teza = slovar_utezi[(ustrezen, vozlisce)]

			#vozlišča, ki jih dobimo za trenutni cikel in potomce od vozlisce			
			tmp_vozl = [(vozlisce, ustrezen)]


			for u in T[vozlisce]:
				#rekurzivno izračunamo največjo težo ter vozlišča za trenutnega potomca u ter cikel ustrezen
				teza_c, vozlisca_c = recursive_max_subset(u, ustrezen)

				#povečamo težo, ter dodamo vozlišča
				teza += teza_c
				tmp_vozl += list(vozlisca_c)

			#če je teža večja, kot trenutno največja izračunana teža, jo posodobimo
			if teza > maks_teza:
				maks_teza = teza

				#vozlišča moramo kopirati, da nam ne ostane pointer na vmesne rezultate
				vozlisca = tmp_vozl[:]

		#na koncu si trenutni rezultat shranimo v slovar, skladno z namigom seznam spremenimo v frozenset
		frozen = frozenset(vozlisca)
		memo[(vozlisce, cikel)] = (maks_teza, frozen)

		return (maks_teza, frozen)

	#maksimalno težo bomo dobil, če pregledamo celo drevo ter vse možne cikle,
	#to bomo dosegli ravno, če začnemo v korenu drevesa, ter z ničelnim ciklom(0), saj so z njega vsi ustrezni
	maks_teza, vozlisca_c = recursive_max_subset(0,0)

	#kot rezultat dobimo težo ter seznam parov vozlišč, pri tem v paru (v, c) v predstavlja
	#vozlišče iz drevesa, c pa desetiški zapis podmnožice cikla. To popravimo na sledeč način:
	vozlisca = []
	for v, cikel in vozlisca_c:
		for j in range(k):
			if podmnozice[cikel][j] == 1:
				vozlisca.append((j, v))


	return maks_teza, vozlisca






