from collections import Counter
import csv
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import requests

#Variables

phrase_exemple = "Ce texte peut contenir des mots qui se répètent pour tester le nombre de mots"
mots_parasites = ["le", "la", "les", "de", "du", "des", "un", "une", "deux", "trois",
    "quatre", "cinq", "six", "sept", "huit", "neuf", "dix", "et", "ou",
    "car", "avec", "pour", "dans", "sur", "sous", "par", "entre", "vers",
    "ainsi", "mais", "donc", "or", "ni", "si", "que", "qui", "quoi", "où",
    "quand", "comment", "en", "ça", "ce", "se", "ces", "ceux", "cette", "cet", "mon", "ton", "son", "mes", "tes", "ses"
]
chemin_csv_parasite = 'parasite.csv'
html = "<p>Ceci est un exemple de <strong>texte</strong> avec des balises HTML.</p>"
valeurs = []
urls_dans_dmn = []
urls_hors_dmn = []
liens_entrants, liens_sortants = [], []

url_audite = input("Entrez l'URL de la page à auditer : ")


#Fonction - Étape 1

def analyser_texte(texte):
    """fonction qui prend en paramètre un texte et qui retourne une liste/dictionnaires de l'ensemble des mots présents dans le texte avec leur occurrence"""
    texte = texte.lower().split()
    occurrences = Counter(texte)
    mots_tries = sorted(occurrences.items(), key=lambda x: x[1], reverse=True)
    return mots_tries

resultat = analyser_texte(phrase_exemple)

#Afficher le résultat Étape 1
#for mot, occurrence in resultat:
#    print(f"{mot}: {occurrence}")

#Fonction - Étape 2
    
def filtrer_mots_parasites(occurrences, mots_parasites):
    """fonction qui prend en paramètre la structure de données précédentes, 
    ainsi qu'une liste de mots parasites et qui retourne la structure de données privées des mots de la liste parasite"""
    occurrences_filtrees = [(mot, occurrence) for mot, occurrence in occurrences if mot not in mots_parasites]
    return occurrences_filtrees

resultat_filtre = filtrer_mots_parasites(resultat, mots_parasites)

#Afficher le résultat Étape 2
#for mot, occurrence in resultat_filtre:
#   print(f"{mot}: {occurrence}")

#Fonction - Étape 3

def mots_parasites_csv(chemin_fichier_csv):
    """fonction qui récupère les mots parasite dans un fichier parasite.csv et retourne une liste des ses mots"""
    with open(chemin_fichier_csv, 'r', encoding='ISO-8859-1') as fichier_csv:
            lecture_csv = csv.reader(fichier_csv)
            for ligne in lecture_csv:
                mot_parasite = ligne[0].strip()
                mots_parasites.append(mot_parasite)
    return mots_parasites

liste_csv = mots_parasites_csv(chemin_csv_parasite)

#Afficher le résultat Étape 3
#print("Les mots parasites :", liste_csv)

#Fonctions - Étape 4 

#print("Résultat mots cles les plus importants de la page :")
#for mot, occurrence in resultat_filtre:
#    print(f"{mot}: {occurrence}")

#Fonctions - Étape 5

def sans_balises_html(texte_html):
    """fonction qui prend en paramètre une chaine de caractère au format html et renvoie le même texte mais sans les balises html"""
    soup = BeautifulSoup(texte_html, 'html.parser')
    texte = soup.get_text(separator=' ')
    return texte
 
sans_balises = sans_balises_html(html)

#Afficher le résultat Étape 5
print("Texte sans les balise HTML :", sans_balises)

#Fonctions - Étape 6 et 7

def extraire_valeurs_attribut(html, balise, valeur_attribut):
    """fonction qui prend en paramètre une chaine de caractère, le nom d'une balise, le nom d'un attribut"""
    soup = BeautifulSoup(html, 'html.parser')
    balises = soup.find_all(balise)

        # Extraire les valeurs de l'attribut spécifié pour chaque balise
    for balise in balises:
            valeurs.append(balise.get(valeur_attribut))
    return valeurs

#Exemple
#html_exemple = """
#<html>
#    <body>
#        <a href="https://example.com">Lien 1</a>
#    </body>
#</html>
#"""
#récupérer les valeurs des attributs "href" des balises "a"
#resultat = extraire_valeurs_attribut(html_exemple, 'a', 'href')
#print("Valeurs des attributs 'href' :", resultat)

#Fonction - Étape 8

def ext_nom_dmn(url):
    """fonction qui prend en paramètre une url et qui extrait le nom de domaine"""
    sup_url = urlparse(url)
    nom_dmn = sup_url.netloc
    return nom_dmn

#zxemple
#url = "https://arthur-guilet.fr/index"
#dmn_resultat = ext_nom_dmn(url)
#affiche le domaine
#print("le nom de domaine de l'url  :",dmn_resultat)

#fonction - Étape 9

def url_par_dmn(nom_dmn, liste_urls):
    """fonction prenant en paramètre une chaine de caractère représentant un nom de domaine, 
       et une liste de valeurs qui sont des url et qui retourne deux listes 
       avec les url qui font partie du domaine et ceux qui n'en font pas partie"""
    
    for url in liste_urls:
        dmn_url = ext_nom_dmn(url)
        if dmn_url == nom_dmn:
            urls_dans_dmn.append(url)
        else:
            urls_hors_dmn.append(url)
    return urls_dans_dmn, urls_hors_dmn

#test 
#nom_dmn_exemple = "arthur-guilet.fr"
#liste_urls_exemple = [
#    "https://arthur-guilet.fr/index",
#    "https://test.com/entreprise",
#]
#urls_dans_dmn, urls_hors_dmn = url_par_dmn(nom_dmn_exemple, liste_urls_exemple)
#print("dans le domaine : ", urls_dans_dmn)
#print("hors du domaine : ", urls_hors_dmn)

#fonction  etape 10

def recupere_html_de_url(url):
    """fonction qui ouvre une page html depuis une url et récupère le texte HTML qui la compose"""
    recupere = requests.get(url)
    return recupere.text
      
#test sur mon portfolio
#url_exemple = "https://arthur-guilet.fr"
#html_page = recupere_html_de_url(url_exemple)
#print("HTML de ma page :", html_page)

#fonction  Étape 11

def audit_page(url):
   
    texte_html = recupere_html_de_url(url)
    if texte_html:
        txt_s_balises = sans_balises_html(texte_html)
        nom_dmn = ext_nom_dmn(url)
        resultat = analyser_texte(txt_s_balises)
        mots_parasites = mots_parasites_csv('parasite.csv')
        resultat_filtre = filtrer_mots_parasites(resultat, mots_parasites)
        mots_cles = resultat_filtre[:3]
       
        if nom_dmn:
            liens_entrants, liens_sortants = url_par_dmn(nom_dmn, extraire_valeurs_attribut(texte_html, 'a', 'href'))
        balises_alt_presentes = any('alt' in balise.attrs for balise in BeautifulSoup(texte_html, 'html.parser').find_all('img'))

        print(f"Les 3 premières occurrences : {mots_cles}")
        print(f"Nombre de liens entrants : {len(liens_entrants)}")
        print(f"Nombre de liens sortants : {len(liens_sortants)}")
        print(f"Nombre de balises 'alt' pour les images : {balises_alt_presentes}")

#test final
audit_page(url_audite)




