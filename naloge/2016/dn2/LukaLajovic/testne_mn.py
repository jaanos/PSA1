#tukajšne funkcije niso zares testne
#tudi ne koristijo nalogi, a med ko sem iskal pravo rešitev
#mi je pomagalo, da sem si problem razdelil na manjše
# te funkcije so mi pomagale razmišljati
# funkcija z imenom končna reši nalogo a v zelo slabem času
def vsota1dim(drevo,masa):
    predogled=[False for x in range(len(drevo))]
    poogled=[False for x in range(len(drevo))]
    vrednosti={}
    for u in range(len(drevo)):
        vrednosti[u]=0
    izbrani=0
    q=True
    while q==True:
        naslednji=None
        predogled[izbrani]=True        
        for x in drevo[izbrani]:
            if predogled[x]==False:
                naslednji=x
                break
        if naslednji==None:
            poogled[izbrani]=True
            teza_otrok=0
            nasel_sem=False
            otroci=[]
            teza_vnukov=0
            for k in drevo[izbrani]:
                if poogled[k]==False:
                    if nasel_sem==False:
                        nasel_sem=True
                        naslednji=k
                    
                if poogled[k]==True:
                    teza_otrok+=vrednosti[k]
                    for i in drevo[k]:
                        #s tem bo izbrani element sam svoj vnuk, a ker še ni bil obiskan je vredn 0
                        teza_vnukov+=vrednosti[i]
            
            vrednosti[izbrani]=max(teza_otrok,masa[izbrani]+teza_vnukov)
            if naslednji==None:
                q=False
            else:
                izbrani=naslednji
        else:
            izbrani=naslednji
            
    return vrednosti[0]

T = [[1, 2], [0, 3, 4], [0, 5], [1, 6, 7], [1, 8], [2, 9, 10], [3], [3], [4, 11], [5], [5, 12], [8], [10, 13], [12]]
w = [[6, 7, 3, 6, 8, 7, 5, 4, 5, 8, 7, 6, 2, 5],[3, 6, 2, 5, 8, 5, 9, 1, 5, 8, 3, 7, 3, 3],[8, 3, 2, 5, 7, 9, 4, 3, 7, 8, 0, 9, 3, 8],[5, 7, 3, 7, 2, 9, 4, 2, 6, 0, 9, 1, 5, 0]]


smreka=[[1],[0,2],[1,3],[2]]
bor=[[1,2],[0],[0,3,4],[2],[2]]
teza1=[[2,2,2],[2,2,2],[2,2,2],[2,2,2]]
teza2=[[2,2,2],[2,2,2],[2,2,2],[2,2,2],[2,2,2]]




#ta bo poiskusilnajti maks brez rekurzine
def iskanje_v_globino(graf,el1):
    predogled=[False for x in range(len(graf))]
    poogled=[False for x in range(len(graf))]
    izbrani=el1
    predogled[el1]=True
    q=True
    while q==True:
        naslednji=None
        predogled[izbrani]=True
        for x in graf[izbrani]:
            if predogled[x]==False:
                naslednji=x
                break
        if naslednji==None:
            poogled[izbrani]=True
            for k in graf[izbrani]:
                if poogled[k]==False:
                    naslednji=k
                    break
            if naslednji==None:
                q=False
            else:
                izbrani=naslednji
        else:
            izbrani=naslednji
    
    t=[]            
    for i in range(len(poogled)):
        if poogled[i]==False:
            t+=[i]
    return t

def brez_rekurzije(drevo,masa):
    predogled=[False for x in range(len(drevo))]
    poogled=[False for x in range(len(drevo))]
    vrednosti={}
    izbrani=0
    q=True
    while q==True:
        naslednji=None
        predogled[izbrani]=True        
        for x in drevo[izbrani]:
            if predogled[x]==False:
                naslednji=x
                break
        if naslednji==None:
            poogled[izbrani]=True
            teza=0
            nasel_sem=False
            for k in drevo[izbrani]:
                if poogled[k]==False:
                    if nasel_sem==False:
                        nasel_sem=True
                        naslednji=k
                if poogled[k]==True:
                    teza+=vrednosti[k]
            vrednosti[izbrani]=max(teza,masa[izbrani])
            if naslednji==None:
                q=False
            else:
                izbrani=naslednji
        else:
            izbrani=naslednji
            
    return max(vrednosti.values())


#ta ti bo vrnil graf v obliki slovarja
def naredi_graf(drevo,k):
    graf={}
    for i in range(len(drevo)):
        for j in range(k):
            graf[(i,j)]=[]
    for x in graf:
        for y in drevo[x[0]]:
            graf[x].append((y,x[1]))
        if x[1]==0:
            graf[x].append((x[0],k-1))
            if k-1!=1:
                graf[x].append((x[0],1))
        elif x[1]==k-1:
            graf[x].append((x[0],k-1))
            if k-1!=0:
                graf[x].append((x[0],k-1))
        else:
            graf[x].append((x[0],x[1]-1))
            graf[x].append((x[0],x[1]+1))            
    return graf

#vrne velikost največje neodvisne množice v drevesu
def neodvisna(drevo,teze,v=0,pred=None,upo=False):
    print("1")
    if len(drevo[v])<=1 and pred!=None:
        if upo==False:
            return teze[v]
        else:
            return 0
    else:
        A=[]
        for u in drevo[v]:
            if u!=pred:
                A+=[u]
        if upo==True:
            return sum([neodvisna(drevo,teze,x,v,False) for x in A])
        else:
            return max(teze[v]+sum([neodvisna(drevo,teze,x,v,True) for x in A]),sum([neodvisna(drevo,teze,x,v,False) for x in A]))


    
    


#vrne najdalšo neodvisno množico v drevesu
def neodvisna2(drevo,v,pred=None,upo=False):
    if len(drevo[v])<=1 and pred!=None:
        if upo==False:
            return [v]
        else:
            return []
    else:
        A=[]
        for u in drevo[v]:
            if u!=pred:
                A+=[u]
        if upo==True:
            pm=[]
            for x in A:
                pm+=neodvisna2(drevo,x,v,False)
            return pm
        else:
            pm1=[]
            for x in A:
                pm1+=neodvisna2(drevo,x,v,False)
            pm2=[v]
            for x in A:
                pm2+=neodvisna2(drevo,x,v,True)
            if len(pm1)>len(pm2):
                return pm1
            else:
                return pm2


#najde najtezjo neodvisno množico na ciklu
#največjo bi bilo neumno iskati

cilk=[[1,5],[0,2],[1,3],[2,4],[4,5],[0,4]]
teze_cikla=[1,2,3,4,5,6]
def neodvisniCikel(k,teze,v=0,prejsni=None,upo=False,upo_zac=False):
    if v==k-1:
        if upo==False and upo_zac==False:
            return teze[v]
        else:
            return 0
    else:
        if v==0:
            return max(teze[v]+neodvisniCikel(k,teze,v+1,v,True,True),neodvisniCikel(k,teze,v+1,v,False,False))
        else:
            if upo==True:
                return neodvisniCikel(k,teze,v+1,v,False,upo_zac)
            else:
                return max(teze[v]+neodvisniCikel(k,teze,v+1,v,True,upo_zac),neodvisniCikel(k,teze,v+1,v,False,upo_zac))

#ta pa vrne seznam namesto vsote

def makssum(seznami):
    maks=seznami[0]
    for x in seznami:
        if sum(x)>sum(maks):
            maks=x
    return maks


def neodvisniCikel2(k,teze,v=0,prejsni=None,upo=False,upo_zac=False):
    if v==k-1:
        if upo==False and upo_zac==False:
            return [teze[v]]
        else:
            return []
    else:
        if v==0:
            return makssum([[teze[v]]+neodvisniCikel2(k,teze,v+1,v,True,True),neodvisniCikel2(k,teze,v+1,v,False,False)])
        else:
            if upo==True:
                return neodvisniCikel2(k,teze,v+1,v,False,upo_zac)
            else:
                return makssum([[teze[v]]+neodvisniCikel2(k,teze,v+1,v,True,upo_zac),neodvisniCikel2(k,teze,v+1,v,False,upo_zac)])
                
            
#vrne vse neodvisne množice v ciklu 
def vsc(k):
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
    return vse_mn

def slovar_neodvisnih(k):
    vse=vsc(k)
    slovar={}
    
    p=vse[0][0]
    slovar[p]=[]
    for i in vse:
        if i[0]!=p:
            slovar[i[0]]=[i]
            p=i[0]
        else:
            slovar[i[0]].append(i)
    return slovar

def slovar_neodvisnih2(vse):
    slovar={}
    
    p=vse[0][0]
    slovar[p]=[]
    for i in vse:
        if i[0]!=p:
            slovar[i[0]]=[i]
            p=i[0]
        else:
            slovar[i[0]].append(i)
    return slovar    

def dovoljene(mnozica,vse):
    slo=slovar_neodvisnih2(vse)
    k=len(slo)
    mozne=[]
    for i in range(k):
        if i  not in mnozica:
            mozne.append(i)
    
    dov=[[]]
    s=[]
    for i in mozne:
        s+=slo[i]
    for x in s:
        u=False
        for y in x:
            v=False
            for z in mnozica:
                if z==y:
                    v=True
                    u=True
                    break
            if v==True:
                break
        if u==False:
            dov.append(x)
    return dov


# ko izberemo eno neodvisno množico nas zanima katere so druge neodvisne množice, ki so neodvisne od nje



def dovoljene1(mnozica,vse):
    dov=[[]]
    for x in vse:
        u=False
        for y in x:
            v=False
            for z in mnozica:
                if z==y:
                    v=True
                    u=True
                    break
            if v==True:
                break
        if u==False:
            dov.append(x)
    return dov
           
o=vsc(7)    
g=o[4]
print("mitril")
print(dovoljene(g,o))
print("gimli")
 

#zdaj bom naredil najtežjo za drevo in cikl dolžine 2
#cikl dolžine dva ima 3 neodvisne množice prvi element, drugi element in prazno množico
def n2c(drevo,teze,v=0,pred=None,upo=[False,False]):
    #print(str(teze[0][v])+"marlon brando"+str(teze[1][v]))
    #print(upo)
    #print("on the waterfront")    
    if len(drevo[v])<=1 and pred!=None:
        if upo==[False,True]:
            return teze[0][v]
        elif upo==[True,False]:
            return teze[1][v]
        else:
            return max(teze[0][v],teze[1][v])
    else:
         A=[]
         for u in drevo[v]:
            if u!=pred:
                A+=[u]       
         if upo==[False,True]:
            return max(teze[0][v]+sum([n2c(drevo,teze,x,v,[True,False]) for x in A]),sum([n2c(drevo,teze,x,v,[False,False]) for x in A]))
         elif upo==[True,False]:
            return max(teze[1][v]+sum([n2c(drevo,teze,x,v,[False,True]) for x in A]),sum([n2c(drevo,teze,x,v,[False,False]) for x in A]))
         else:
            return max(teze[0][v]+sum([n2c(drevo,teze,x,v,[True,False]) for x in A]),teze[1][v]+sum([n2c(drevo,teze,x,v,[False,True]) for x in A]),sum([n2c(drevo,teze,x,v,[False,False]) for x in A]))





        



    

#vrne težo najtežje neodvisne množice
cipresa=[[1,2],[0],[0,3],[2]]
teza_ciprese=[[1,2,3,4],[4,3,2,1]]
tisa=[[1],[0,2],[1,3],[2]]
#print("botr trojka je bedn")
#print(n2c(cipresa,teza_ciprese))
#print("apocalypse now")
#print(n2c(tisa,teza_ciprese))

        

jelsa=[[1],[0,2],[1,3],[2,4],[3,5],[4]]

teza_jelse=[1,2,3,4,5,6]

bor=[[1,2],[0],[0,3,4],[2],[2,5],[4,6,7],[5],[5]]

teza_bora=[10,20,30,40,50,60,70,80,90,100]
print(neodvisniCikel2(10,teza_bora))
print(neodvisniCikel(10,teza_bora))
#print(neodvisna(jelsa,teza_jelse,1))
#print(neodvisna2(jelsa,0))
#print(neodvisna2(bor,0))
#teza_bora=[10,20,30,40,50]
#print(neodvisna(bor,teza_bora,4))
print("pikaso")
print(brez_rekurzije(bor,teza_bora))    
om=naredi_graf(smreka,3)
rom=naredi_graf(bor,3)


#sedaj naredim končno rešitev za naš problem


hrast=[[1,2],[0,3,4],[0],[1,5,6],[1],[3],[3]]
hrastova_teza=[[1,55,1,99,1,1,1],[1,2,3,4,5,6,7],[7,6,5,4,3,2,1]]
vsota_hrasta=sum(hrastova_teza[0])+sum(hrastova_teza[1])+sum(hrastova_teza[2])
vsa=vsc(3)

jablana=[[1],[0,2],[1,3],[2,4],[3]]
teza_jabolka=[[1,2,3,4,5],[5,4,3,2,1],[1,2,3,4,5]]
def konc(vse,drevo,teze,v=0,pred=None,upo=[]):
    if len(drevo[v])<=1 and pred!=None:
        d=dovoljene(upo,vse)
        u=[]        
        for x in d:
            c=0
            for y in x:
                c+=teze[y][v]
            u+=[c]
        return max(u)
    else:
        # d so vse neodvisne dovoljene na ciklu tega voszlipča
        d=dovoljene(upo,vse)
        #print("slavoj žižek")
        #print(upo)
        #print(d)
        A=[]
        for u in drevo[v]:
            if u!=pred:
                A+=[u]
        # možne so vse ki neodvisne na tem
        mozne=[]        
        for x in d:
            #vrednost tež na neodvisni množici tega cikla
            moja_vred=0
            for s in x:
                moja_vred+=teze[s][v]
            u=0
            for y in A:
                u+=konc(vse,drevo,teze,y,v,x)
            mozne.append(u+moja_vred)
        #print(mozne)
        return max(mozne)


#print(konc(vsa,hrast,hrastova_teza))
#print(konc(vsc(1),jablana,teza_jabolka))
#print(konc(vsc(2),jablana,teza_jabolka))


#print("rasoherina")    
#print(konc(vsc(3),jablana,teza_jabolka))
#print("radama 2")
#print(konc(vsc(4),T,w))

print("antananarivo")    

def konc2(vse,drevo,teze,v=0,pred=None,upo=[]):
    if len(drevo[v])<=1 and pred!=None:
        d=dovoljene(upo,vse)
        u=[]
        vsota=0
        maksi=[]
        #print(v)
        for x in d:
            c=0
            for y in x:
                c+=teze[y][v]
            if c>vsota:
                vsota=c
                maksi=x
        s=[]
        for r in maksi:
            s+=[(r,v)]
        return s
    else:
        #print(v)
        d=dovoljene(upo,vse)
        A=[]
        for u in drevo[v]:
            if u!=pred:
                A+=[u]
        mozne=[]

        for x in d:
            njena_mnozica=[]
            for f in x:
                njena_mnozica+=[(f,v)]    
            for y in A:
                njena_mnozica+=konc2(vse,drevo,teze,y,v,x)
            mozne.append(njena_mnozica)
        #print(mozne)    
        maksi=mozne[0]        
        vsota=0
        #print(maksi)
        for x in maksi:
            #print(x)
            vsota+=teze[x[0]][x[1]]
        for k in mozne:
            t=0
            for i in k:
                t+=teze[i[0]][i[1]]
            if t>vsota:
                vsota=t
                maksi=k
        return maksi        


#t=konc2(vsc(4),T,w)
#g=0
#for i in t:
#    g+=w[i[0]][i[1]]
#print(t)
#print(g)
#print(konc(vsc(4),T,w))
#print(konc2(vsc(3),jablana,teza_jabolka))            

a=[[1, 46, 47, 48], [0, 2, 28, 40, 44], [1, 3, 21, 25, 27], [2, 4, 20], [3, 5, 6, 12, 16, 18, 19], [4], [4, 7, 8, 9], [6], [6], [6, 10], [9, 11], [10], [4, 13], [12, 14], [13, 15], [14], [4, 17], [16], [4], [4], [3], [2, 22], [21, 23], [22, 24], [23], [2, 26], [25], [2], [1, 29, 33], [28, 30, 31], [29], [29, 32], [31], [28, 34, 36, 38, 39], [33, 35], [34], [33, 37], [36], [33], [33], [1, 41, 42], [40], [40, 43], [42], [1, 45], [44], [0], [0], [0]]
b=[[4, 6, 0, 5, 15, 17, 18, 19, 10, 13, 6, 3, 1, 6, 0, 7, 18, 0, 7, 11, 6, 18, 11, 12, 3, 16, 4, 20, 0, 12, 7, 20, 14, 5, 14, 20, 2, 19, 6, 17, 11, 11, 5, 5, 10, 17, 18, 12, 19], [17, 17, 14, 9, 15, 12, 5, 19, 13, 9, 2, 6, 0, 18, 10, 13, 10, 20, 5, 6, 12, 16, 19, 14, 14, 8, 12, 19, 18, 13, 18, 17, 19, 15, 11, 17, 18, 13, 10, 18, 2, 7, 2, 7, 11, 13, 17, 12, 4], [15, 13, 17, 13, 8, 16, 8, 18, 8, 0, 4, 7, 17, 11, 9, 9, 11, 18, 13, 15, 8, 16, 5, 4, 9, 8, 11, 16, 6, 9, 0, 13, 6, 3, 16, 14, 4, 7, 13, 16, 17, 12, 18, 11, 16, 10, 18, 5, 0], [18, 0, 1, 4, 20, 8, 7, 17, 19, 20, 13, 15, 4, 7, 9, 0, 10, 9, 2, 0, 5, 5, 15, 5, 9, 6, 0, 7, 11, 3, 7, 0, 1, 20, 17, 6, 0, 16, 0, 13, 16, 17, 12, 18, 0, 15, 19, 19, 20], [12, 9, 15, 3, 17, 19, 2, 3, 0, 11, 10, 11, 4, 16, 19, 3, 17, 1, 19, 16, 13, 4, 1, 14, 10, 13, 4, 16, 19, 15, 16, 10, 17, 10, 2, 2, 9, 3, 19, 3, 5, 3, 11, 17, 11, 8, 19, 5, 10], [1, 15, 18, 5, 0, 17, 17, 17, 13, 0, 17, 7, 11, 18, 14, 14, 5, 11, 14, 15, 18, 18, 3, 5, 20, 10, 12, 6, 20, 13, 1, 14, 20, 17, 0, 13, 17, 12, 12, 19, 13, 19, 9, 20, 13, 1, 9, 4, 10], [16, 20, 12, 6, 18, 12, 9, 17, 8, 20, 0, 18, 0, 19, 0, 17, 6, 14, 16, 3, 1, 19, 8, 19, 12, 19, 17, 17, 0, 11, 15, 13, 8, 13, 17, 0, 20, 9, 10, 7, 1, 8, 8, 17, 18, 12, 13, 15, 8], [15, 11, 13, 7, 10, 14, 0, 17, 18, 6, 16, 19, 10, 3, 20, 11, 2, 14, 8, 8, 15, 16, 19, 11, 5, 3, 18, 19, 5, 4, 7, 3, 18, 2, 5, 9, 12, 13, 3, 13, 14, 3, 16, 7, 18, 14, 9, 8, 15], [17, 18, 15, 10, 0, 19, 0, 16, 17, 1, 4, 13, 17, 3, 13, 9, 16, 20, 1, 3, 8, 12, 13, 6, 5, 19, 12, 13, 4, 4, 1, 4, 6, 9, 9, 5, 20, 0, 13, 9, 10, 13, 17, 15, 4, 11, 11, 20, 2], [9, 9, 2, 19, 2, 15, 7, 6, 17, 19, 10, 3, 19, 0, 1, 11, 17, 3, 17, 10, 4, 4, 17, 19, 16, 11, 14, 17, 20, 10, 9, 11, 10, 16, 8, 0, 19, 5, 9, 7, 9, 7, 2, 1, 15, 0, 9, 11, 17]]


c=[[1], [0, 2, 5, 15], [1, 3, 4], [2], [2], [1, 6, 13], [5, 7], [6, 8, 10, 12], [7, 9], [8], [7, 11], [10], [7], [5, 14], [13], [1]]
d=[[6, 0, 9, 1, 0, 12, 19, 0, 5, 1, 5, 10, 14, 10, 5, 9], [14, 17, 2, 6, 13, 9, 2, 3, 1, 9, 0, 6, 4, 15, 1, 2], [6, 0, 18, 5, 1, 15, 2, 7, 6, 13, 4, 19, 1, 2, 0, 11], [7, 19, 4, 7, 17, 13, 20, 1, 8, 6, 12, 3, 16, 8, 2, 13], [8, 11, 11, 2, 13, 1, 14, 4, 14, 6, 7, 13, 15, 9, 3, 5], [11, 8, 20, 17, 18, 20, 19, 8, 20, 14, 14, 14, 7, 1, 8, 0], [16, 10, 5, 20, 14, 0, 0, 20, 6, 11, 14, 6, 12, 13, 4, 18]]

#print(konc2(vsc(4),c,d))

vrsta=[[1]]
zac=1
velikost=30
teza_vrste=[(velikost+1)*[1],(velikost+1)*[1]]
while zac<velikost:
    vrsta+=[[zac-1,zac+1]]
    zac+=1
    teza_vrste+=[[1,1]]
vrsta+=[[velikost-1]]

resi=konc(vsc(1),vrsta,teza_vrste)
print("mapotu")
print(resi)
#print(konc(vsc(4),T,w))
#print(konc2(vsc(10),a,b))


