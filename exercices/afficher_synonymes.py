import nltk
from utils import obtenir_synonymes  # Utilisez la fonction correcte depuis utils.py

# Téléchargez les ressources de NLTK une seule fois
nltk.download('wordnet')

def main():
    # Obtenir et afficher les synonymes du mot "grand"
    synonymes = obtenir_synonymes("grand")  # Assurez-vous que le mot est en français
    print("Synonymes de 'grand':", synonymes)

    synonymes = obtenir_synonymes("petit")  # Assurez-vous que le mot est en français
    print("Synonymes de 'grand':", synonymes)

    synonymes = obtenir_synonymes("homme")  # Assurez-vous que le mot est en français
    print("Synonymes de 'grand':", synonymes)

if __name__ == "__main__":
    main()
