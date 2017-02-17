# -*- coding: utf-8 -*-
def vse_neodvisne_na_ciklu(k):
    vse_mn=[]
    for i in range(k):
        ijeva_mn=[[i]]
        for j in range(i+1,k):
            if abs(i-j)!=1:
                u=[]
                for x in ijeva_mn:
                    if abs(x[-1]-j)!=1 and i!=0:
                        z=x.copy()
                        z+=[j]
                        u.append(z)
                    elif i==0 and abs(x[-1]-j)!=1 and j!=k-1:
                        z=x.copy()
                        z+=[j]
                        u.append(z)                        
                ijeva_mn+=u
        vse_mn+=ijeva_mn
    return [[]]+vse_mn


    


#vrne vse neodvisne množice v komplementu od neke izbrene množice
#deluje v len(množica)*len(vse)
#načeloma mora sprejeti vse neodvisne množice in množico katere komplement iščemo
def komplemente(mnozica,vse):
    dov=[0]
    for x in range(1,len(vse)):
        u=False
        for y in vse[x]:
            v=False
            for z in mnozica:
                if z==y:
                    v=True
                    u=True
                    break
            if v==True:
                break
        if u==False:
            #print(vse[x])
            dov.append(x)
    return dov
            

#vse bo množica vseh neodvisnih na ciklu dolžine 2
# vrednosti bo oblike 
#

#algoritem bo pogledal za vsek element drevesa in vsako neodvisnopodmnožico 
# cikla kakšna je največja vrednost
#v vrednosti bo za vsako vozlišče shranil njegovo maksimalno težo ob vsaki neodvisni podmnožici
#če izberem neko podmnožico shrani največjo vrednost za drevo pod njim
# funkcija gre po drevesu z iskanjem v globino
def neodvisna(drevo,teze):
    vse=vse_neodvisne_na_ciklu(len(teze))
    predogled=[False for x in range(len(drevo))]
    poogled=[False for x in range(len(drevo))]
    vrednosti={}
    #ključi bodo elementi drevesa vrednosti pa bodo indeksi neodvisnih mn
    elementi={}
    for i in range(len(drevo)):
        om={}
        kom={}
        for j in range(len(vse)):
            om[j]=0
            kom[j]=[]
        vrednosti[i]=om
        elementi[i]=kom
    izbrani=0
    isci=True
    while isci==True:
        #print(izbrani)
        naslednji=None
        predogled[izbrani]=True        
        for x in drevo[izbrani]:
            if predogled[x]==False:
                naslednji=x
                break  
      
        if naslednji==None:
            poogled[izbrani]=True
            predhodniki=[]
            nasel_naslednika=False
            for x in drevo[izbrani]:
                if poogled[x]==True:
                    predhodniki.append(x)
                if poogled[x]==False and nasel_naslednika==False:
                    nasel_naslednika=True
                    naslednji=x
            if len(predhodniki)==0:
                
                #če sem v listu si zabeležim vse možne vrednosti mojih podmnožic
                for i in range(len(vse)):
                    teza_mnozice=0
                    for j in vse[i]:
                        teza_mnozice+=teze[j][izbrani]
                    vrednosti[izbrani][i]=teza_mnozice
                    elementi[izbrani][i]=[(i,izbrani)]
            else:
                for i in range(len(vse)):
                    teza_mnozice=0
                    if len(vse[i])!=0:
                        for j in vse[i]:
                            teza_mnozice+=teze[j][izbrani]

                    komp=komplemente(vse[i],vse)

                    maks=0
                    #za el v slovar elementi greš
                    za_el=[]
                    for el in predhodniki:
                        mali_maks=0
                        mali_el=0
                        for mn in komp:
                            if vrednosti[el][mn]>mali_maks:
                                mali_maks=vrednosti[el][mn]
                                mali_el=mn
                        za_el+=[mali_el]
                        maks+=mali_maks    
                    tt=[]
                    for t in range(len(predhodniki)):
                        tt+=elementi[predhodniki[t]][za_el[t]]
                    elementi[izbrani][i]=[(i,izbrani)]+tt
                    vrednosti[izbrani][i]=teza_mnozice+maks            
            if naslednji==None:
                isci=False
            else:
                izbrani=naslednji
        else:
            izbrani=naslednji

    m=0
    skupna_masa=0
    for i in vrednosti[0]:
        if vrednosti[0][i]>skupna_masa:
            m=i
            skupna_masa=vrednosti[0][i]
    rezultat=[]
    for x in elementi[0][m]:
        for y in vse[x[0]]:
            rezultat+=[(y,x[1])]
    return (skupna_masa,rezultat)
def maxCycleTreeIndependentSet(T, w):
    """
    Najtežja neodvisna množica
    v kartezičnem produktu cikla C_k in drevesa T z n vozlišči,
    kjer ima tabela tež w dimenzije k×n (k >= 2).

    Vrne par (c, s), kjer je c teža najdene neodvisne množice,
    s pa je seznam vozlišč v neodvisni množici,
    torej seznam parov oblike (i, u) (0 <= i <= k-1, 0 <= u <= n-1).
    """
    n = len(T)
    assert all(len(r) == n for r in w), \
        "Dimenzije tabele tež ne ustrezajo številu vozlišč v drevesu!"
    assert all(all(u in T[v] for v in a) for u, a in enumerate(T)), \
        "Podani graf ni neusmerjen!"
    k = len(w)
    assert k >= 2, "k mora biti vsaj 2!"
    if n == 0:
        return (0, [])
    #raise NotImplementedError("Naredi sam!")
    return neodvisna(T,w)
