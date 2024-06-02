#carlos lozano alemañy
import threading
import time
import random

#Estats que ens serviran per aconseguir la concurrència entre els processos
class EstatsJutge:
    DAFORA = 0      #si està dafora del jutjat
    DINS = 1        #si està dins el jutjat
    DESAPAREGUT = 2 #si ha partit dels tribunals
    DESCANSA = 4

class Principal:
    def __init__(self):
        #Variables per conrolar el nombre de persones a cada moment
        self.sospitosos = 20
        self.N_fitxats = 0
        self.N_declarats = 0
        self.N_entrats = 0
        #Estat inicial del jutge
        self.status = EstatsJutge.DAFORA
        #Semàfors
        self.Sala = threading.Semaphore(1)
        self.tots_fitxats = threading.Semaphore(0)
        self.a_declarar = threading.Semaphore(0)
        self.tots_declarats = threading.Semaphore(0)
        self.veredicte_sospitosos = threading.Semaphore(0)
        self.veredicte_sospitosos_restants = threading.Semaphore(0)

    def inicio(self):
        #Tots els noms dels personatges
        noms = ["Deadshot", "Harley Quinn", "Penguin"
                , "Riddler", "Bane", "Talia al Ghul"
                , "Ra's al Ghul", "Deathstroke", "Clayface"
                , "Killer Croc", "Catwoman","Posion Ivy"
                , "Mr. Freeze", "Jason Todd", "Hush"
                ,"Hugo Strange","Joker", "Mad Hatter"
                ,"Scarecrow", "Two-face"]
        
        print("La policia de Gotham ha detingut a "+ str(self.sospitosos) + " sospitosos ")
        print("El jutge prendrà declaració als qui pugui ")
        #Creació dels fils
        threads = []
        threads.append(threading.Thread(target=self.jutge_Dredd))
        for i in range(self.sospitosos):
            threads.append(threading.Thread(target=self.sospitos, args=(noms[i],)))
        #Llançament dels fils
        for thread in threads:
            thread.start()
        #Esperar a que acabin els fils
        for thread in threads:
            thread.join()
        #FI
        print("--------------------------------------------------SIMULACIÓ ACABADA ")
    
    #PROCÉS JUTGE
    def jutge_Dredd(self):
        time.sleep(random.randint(1,3))        
        print("----> Jutge Dredd: Jo som la llei!")
        #Prova a entrar dins la sala
        time.sleep(random.randint(1,3))        
        self.Sala.acquire()
        #Entra a la sala
        self.status = EstatsJutge.DINS
        print("----> Jutge Dredd: Som a la sala, tanqueu porta!")
        #Si el jutjat està buit el jutge desapareixerà de la sala
        if self.N_entrats == 0:
            self.status = EstatsJutge.DESAPAREGUT
            self.Sala.release()
            print("----> Jutge Dredd: Si no hi ha ningú me'n vaig!")
        else:
        #Si hi ha gent al jutjat farà el procediment pertinent
            print("----> Jutge Dredd: Fitxeu als sospitosos presents")
            self.tots_fitxats.acquire()#Espera a que tots estiguin fitxats per poder prendre declaració
            print("----> Jutge Dredd: Preniu declaració als presents")
            self.a_declarar.release()#Avisa als sospitosos de que poden declarar
            self.tots_declarats.acquire()#Espera a que tots hagin declarat per obtenir un veredicte
            print("----> Judge Dredd: Podeu abandonar la sala tots a l'asil!")
            self.veredicte_sospitosos.release()#Avisa als sospitosos del veredicte pres
        #Aleshores s'en va cap a cases
        print("----> Jutge Dredd: La justícia descansa, demà prendré declaració als sospitosos que queden")
        self.status = EstatsJutge.DESAPAREGUT
        self.veredicte_sospitosos_restants.release() #Avisa als sospitosos de que no els prendrà declaració avui
        self.Sala.release()#S'envà de la sala

    #PROCÉS SOSPITÓS   
    def sospitos(self, nom):
        time.sleep(random.randint(1,3))
        print(nom + ": Som innocent!")
        time.sleep(random.randint(1,3))
        #Si el jutge ha desaparegut es queixarà per no haver pogut declarar
        if self.status == EstatsJutge.DESAPAREGUT:
            print(nom + ": No és just vull declarar! Som innocent!")
        else:
        #Si d'altra banda el jutge segueix als tribunals aleshores:
            #Si el jutge està dins la sala el sospitós no podrà entrar
            if self.status == EstatsJutge.DINS:
                #Els sospitosos que no han entrat esperaràn a que el jutge prengui una decisió sobree aquests
                self.veredicte_sospitosos_restants.acquire()
                print(nom+ ": No és just vull declarar! Som innocent!")
                self.veredicte_sospitosos_restants.release() 
            else:
                #Si el jutge es troba als tribunals però fora del jutjat el sospitós podrà entrar
                if self.status == EstatsJutge.DAFORA:
                    self.Sala.acquire()
                    self.N_entrats += 1
                    print(nom + " Entra al jutjat. Sospitosos: " + str(self.N_entrats))
                    self.Sala.release()
                    time.sleep(random.randint(1,3))
                    #El sospitós pot ser fitxat una vegada ha entrat
                    self.N_fitxats += 1
                    print(nom + " fitxa. Fitxats: " + str(self.N_fitxats))
                #Si s'han fitxat a tots aleshores avisam al jutge
                if(self.N_fitxats == self.N_entrats):
                    self.tots_fitxats.release()
                time.sleep(random.randint(1,3))
                #Esperam a que el jutge ens prengui declaració
                self.a_declarar.acquire()
                self.N_declarats += 1
                print(f"{nom} declara. Declaracions: {self.N_declarats}")
                self.a_declarar.release()
                #Si tots han declarat avisam al jutge
                if(self.N_declarats == self.N_fitxats):
                    self.tots_declarats.release()
                #Esperam a que el jutge hagi pres una decisió
                self.veredicte_sospitosos.acquire()
                print(nom + " entra a l'Asil d'Arkham")
                self.veredicte_sospitosos.release()
if __name__ == "__main__":
    Principal().inicio()

        