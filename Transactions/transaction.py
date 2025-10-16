from fastapi import FastAPI
import threading
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from DB import models


app = FastAPI()



dico_accounts = {"Ouali": 500, "Strauss": 200, "Lenny": 100000, "Raphael": 1000}
annule = False

def attendre_annulation():
    global annule
    reponse = input("Tapez 'annuler' pour annuler la transaction (5 secondes)... ")
    if reponse.lower() == "annuler":
        annule = True

def transferer_argent():
        global annule
        annule = False

        envoyeur = input("qui etes vous ?")
        while envoyeur not in dico_accounts :
            print("Rentrez un vrai nom !!!!!")
            envoyeur = input("qui etes vous ?")

        destinataire = input("qui est le destinataire?")
        while destinataire not in dico_accounts :
            print("Rentrez un vrai nom !!!!!")
            destinataire = input("qui est le destinataire?")

        montant = input("combien d'argent voulez vous transférer?")

        if  not str(montant).replace('.', '', 1).isdigit() or dico_accounts[envoyeur] <= float(montant) or float(montant) <= 0 or dico_accounts[destinataire] == dico_accounts[envoyeur]:
            print("Rentrez un vrai montant !!!!!")
            montant = input("combien d'argent voulez vous transférer?")

        print(f"Le solde actuel de {envoyeur} est de {dico_accounts[envoyeur]}")
        print(f"Le solde actuel de {destinataire} est de {dico_accounts[destinataire]}")
        print(f"un virement de {montant}€ va etre fais du compte de {envoyeur} au compte de {destinataire} ")

        thread = threading.Thread(target=attendre_annulation)
        thread.start()
        thread.join(timeout=5)

        if annule:
            print("La transaction a été annulée !")
            print(f"Le montant de {montant}€ n'a pas été transféré.")
            print(f"Le solde actuel de {envoyeur} est de {dico_accounts[envoyeur]}")
            print(f"Le solde actuel de {destinataire} est de {dico_accounts[destinataire]}")
        else:
            dico_accounts[envoyeur] -= float(montant)
            dico_accounts[destinataire] += float(montant)
            print("Temps écoulé. Transaction validée.")
            print(f"Le montant de {montant}€ a été transféré de {envoyeur} à {destinataire}")
            print(f"Le solde actuel de {envoyeur} est de {dico_accounts[envoyeur]}")
            print(f"Le solde actuel de {destinataire} est de {dico_accounts[destinataire]}")

#transferer_argent()


def add_money():

    compte_bancaire_utilisateur_connecté = input("qui etes vous ?")
    while compte_bancaire_utilisateur_connecté not in dico_accounts:
        compte_bancaire_utilisateur_connecté = input("qui etes vous ?")
    solde_initial = dico_accounts[compte_bancaire_utilisateur_connecté]

    montant_voulu = input("combien d'argent voulez vous transférer?")
    while int(montant_voulu) < 0 :
        montant_voulu = input("combien d'argent voulez vous transférer?")


    dico_accounts[compte_bancaire_utilisateur_connecté] += int(montant_voulu)

    print(f"Votre solde etait de {solde_initial}€.Actuellement, il est de {dico_accounts[compte_bancaire_utilisateur_connecté]}€")

#add_money()


