import string

#FONCTIONS

def fontion_correspondance(mot_entre):
    mot_entre=mot_entre.lower()
    if mot_entre=="finale" or mot_entre=="final":
        mot="final"
    if mot_entre=="match pour la troisième place" or  mot_entre=="play-off for third place" or  mot_entre=="match for 3rd place" or mot_entre=="MATCH FOR 3RD PLACE":
        mot="MATCH FOR 3RD PLACE"
    if mot_entre=="demi-finales" or mot_entre== "semi-final" or mot_entre=="SEMIFINALS":
        mot="SEMIFINALS"
    if mot_entre=="quarts de finale" or mot_entre== "quarter-final" or mot_entre=="quarterfinals" or mot_entre=="quarter Finals" or mot_entre=="QUARTER FINAL":
        mot="QUARTER FINAL"
    if mot_entre=="huitièmes de finale" or mot_entre=="round of 16" or mot_entre=="round of sixteen":
        mot="round of sixteen"
    if mot_entre=="ger" or mot_entre=="frg" or mot_entre=="république fédérale d'allemagne":
        mot="ger"
    if mot_entre=="russie" or mot_entre=="urs":
        mot="russia"
    return mot

def fonction_pays(nom_pays):
    nom_pays=nom_pays.lower()
    nom_final=nom_pays[0:3]
    return nom_final

def traduction_pays(nom_pays):
    nom_pays=nom_pays.lower()
    if nom_pays=="allemagne":
        pays_final="germany"
    if nom_pays=="angleterre":
        pays_final="england"
    
    return pays_final

def main():
    return None

if __name__ == '__main__':
    main()