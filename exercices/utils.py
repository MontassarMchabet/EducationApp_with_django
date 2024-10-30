# utils.py

import unicodedata
import re
from fuzzywuzzy import fuzz
from nltk.corpus import wordnet


def normalize_text(text):
    """Normalise le texte en supprimant les accents, les espaces, et en le convertissant en minuscules."""
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    text = text.lower()
    text = re.sub(r'\s+', '', text)
    return text


def obtenir_synonymes(mot):
    """Renvoie une liste de synonymes pour le mot donné."""
    synonymes = set()
    for syn in wordnet.synsets(mot, lang='fra'):  # Spécifiez 'fra' pour le français
        for lem in syn.lemmas('fra'):  # Obtenez les lemmes en français
            synonymes.add(lem.name())  # Ajoute le synonyme à l'ensemble
    return list(synonymes)


def valider_reponse(reponse_etudiant, reponse_attendue, seuil_similarite=80):
    """
    Compare la réponse de l'étudiant à la réponse attendue avec une tolérance de similarité.
    
    Parameters:
        - reponse_etudiant: La réponse fournie par l'étudiant.
        - reponse_attendue: La réponse correcte attendue.
        - seuil_similarite: Le seuil minimum de similarité pour valider la réponse.

    Returns:
        - True si la similarité est égale ou supérieure au seuil, ou si une réponse synonyme est donnée.
        - False sinon.
    """
    reponse_etudiant_normalized = normalize_text(reponse_etudiant)
    reponse_attendue_normalized = normalize_text(reponse_attendue)

    # Vérifiez la similarité
    similarity_score = fuzz.ratio(reponse_etudiant_normalized, reponse_attendue_normalized)

    # Vérifiez si la réponse de l'étudiant est un synonyme de la réponse attendue
    synonymes_attendus = obtenir_synonymes(reponse_attendue_normalized)

    # Normalisez les synonymes pour la comparaison
    synonymes_attendus_normalized = [normalize_text(syn) for syn in synonymes_attendus]

    return similarity_score >= seuil_similarite or reponse_etudiant_normalized in synonymes_attendus_normalized


# affiche dans le terminal les synnonymes d'un mot
def obtenir_synonymess(mot):
    """Retourne une liste de synonymes pour un mot donné."""
    synonymes = set()
    for syn in wordnet.synsets(mot):
        for lem in syn.lemmas():
            synonymes.add(lem.name())  # Ajoute le nom du lemme
    return list(synonymes)
