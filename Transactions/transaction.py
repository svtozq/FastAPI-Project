


from fastapi import FastAPI
app = FastAPI()

validation = True

def annulation_transfert():
    validation = False

dico_accounts = {"Ouali": 500, "Strauss": 200, "Lenny": 100000, "Raphael": 1000}

def transferer_argent():

    if validation == True:

        envoyeur = input("qui etes vous ?")
        while envoyeur not in dico_accounts :
            envoyeur = input("qui etes vous ?")

        destinataire = input("qui est le destinataire?")
        while destinataire not in dico_accounts :
            destinataire = input("qui est le destinataire?")

        montant = input("combien d'argent voulez vous transférer?")
        if dico_accounts[envoyeur] <= int(montant) or int(montant) < 0 or dico_accounts[destinataire] == dico_accounts[envoyeur]:
            montant = input("combien d'argent voulez vous transférer?")

        print(f"Le solde actuel de {envoyeur} est de {dico_accounts[envoyeur]}")
        print(f"Le solde actuel de {destinataire} est de {dico_accounts[destinataire]}")

        dico_accounts[envoyeur] -= int(montant)
        dico_accounts[destinataire] += int(montant)


        print(f"Le montant de {montant}€ a été transféré de {envoyeur} à {destinataire}")
        print(f"Le solde actuel de {envoyeur} est de {dico_accounts[envoyeur]}")
        print(f"Le solde actuel de {destinataire} est de {dico_accounts[destinataire]}")

    else:
        print("Transfers annulé")

transferer_argent()



