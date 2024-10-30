# utils.py

import unicodedata
import re
from fuzzywuzzy import fuzz

def normalize_text(text):
    """Normalise le texte en supprimant les accents, les espaces, et en le convertissant en minuscules."""
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    text = text.lower()
    text = re.sub(r'\s+', '', text)
    return text

def valider_reponse(reponse_etudiant, reponse_attendue, seuil_similarite=80):
    """
    Compare la réponse de l'étudiant à la réponse attendue avec une tolérance de similarité.
    
    Parameters:
        - reponse_etudiant: La réponse fournie par l'étudiant.
        - reponse_attendue: La réponse correcte attendue.
        - seuil_similarite: Le seuil minimum de similarité pour valider la réponse.

    Returns:
        - True si la similarité est égale ou supérieure au seuil.
        - False sinon.
    """
    reponse_etudiant_normalized = normalize_text(reponse_etudiant)
    reponse_attendue_normalized = normalize_text(reponse_attendue)
    similarity_score = fuzz.ratio(reponse_etudiant_normalized, reponse_attendue_normalized)
    return similarity_score >= seuil_similarite
