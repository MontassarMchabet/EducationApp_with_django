from django.contrib import admin 
from django.http import HttpResponseRedirect
from django.urls import path
from django.template.response import TemplateResponse
from django.utils import timezone
from django.shortcuts import get_object_or_404
from transformers import pipeline  # Import de la bibliothèque Hugging Face
import os
import google.generativeai as genai  # Import du client Google Generative AI

from .models import Formulaire, Rapport, Course

# Initialiser le pipeline de résumés de Hugging Face
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Initialiser le client Google Generative AI avec une clé API (à remplacer par la vôtre)
genai.configure(api_key="AIzaSyCXmHskLc0MkTDGtK0q_G2mLPieiuAXiXs")

@admin.register(Formulaire)
class FormulaireAdmin(admin.ModelAdmin):
    list_display = ('chapitre', 'date_remplissage', 'type_formulaire', 'note')
    search_fields = ('chapitre__title',)
    list_filter = ('type_formulaire',)

@admin.register(Rapport)
class RapportAdmin(admin.ModelAdmin):
    list_display = ('course', 'date_creation')
    search_fields = ('course__title',)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('generate-report/', self.admin_site.admin_view(self.generate_report_view), name='generate-report'),
        ]
        return custom_urls + urls

    def generate_report_view(self, request):
        if request.method == 'POST':
            course_id = request.POST.get('course_id')
            if not course_id:
                self.message_user(request, "Veuillez sélectionner un cours pour générer le rapport.", level="error")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            # Récupérer le cours avec une gestion d'erreur
            course = get_object_or_404(Course, id=course_id)
            report_text = self.create_report_text(course)

            # Enregistrer le rapport
            Rapport.objects.create(
                course=course,
                contenu_rapport=report_text,
                date_creation=timezone.now()
            )

            self.message_user(request, "Rapport généré avec succès.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        context = {'courses': Course.objects.all()}
        return TemplateResponse(request, 'admin/generate_report.html', context)

    def create_report_text(self, course):
        """Génère le texte du rapport de satisfaction pour chaque chapitre du cours."""
        report_content = f"Rapport de satisfaction pour le cours '{course.title}'\n\n"
        report_content += "Détails par chapitre:\n"
        
        positive_comments = []  # Stocker les commentaires positifs pour la conclusion
        negative_comments = []  # Stocker les commentaires négatifs pour la conclusion

        for chapter in course.chapters.all():
            formulaires = Formulaire.objects.filter(chapitre=chapter)
            if formulaires.exists():
                average_rating = sum(f.note for f in formulaires) / formulaires.count()
                total_responses = formulaires.count()
                comments = "\n".join(f" - {f.contenu}" for f in formulaires)

                chapitre_text = (
                    f"Chapitre: {chapter.title}\n"
                    f"Note moyenne: {average_rating:.2f}\n"
                    f"Total des réponses: {total_responses}\n"
                    f"Commentaires:\n{comments}\n\n"
                )

                report_content += chapitre_text

                # Classer les commentaires en fonction des notes
                for f in formulaires:
                    if f.note < 3:
                        negative_comments.append(f.contenu)  # Commentaires négatifs
                    else:
                        positive_comments.append(f.contenu)  # Commentaires positifs
                
                if average_rating < 3:
                    report_content += (
                        f"Attention : Ce chapitre présente une note faible de {average_rating:.2f}\n"
                    )
            else:
                report_content += f"Chapitre: {chapter.title} - Aucun formulaire de satisfaction reçu.\n\n"

        # Générer des conclusions basées sur les commentaires négatifs et positifs
        if negative_comments:
            summary_text_neg = " ".join(negative_comments)
            conclusion_neg = summarizer(summary_text_neg, max_length=150, min_length=50, do_sample=False)
            report_content += f"\nConclusion sur les commentaires négatifs :\n{conclusion_neg[0]['summary_text']}"

        if positive_comments:
            summary_text_pos = " ".join(positive_comments)
            conclusion_pos = summarizer(summary_text_pos, max_length=150, min_length=50, do_sample=False)
            report_content += f"\nConclusion sur les commentaires positifs :\n{conclusion_pos[0]['summary_text']}"

        # Suggestions pour améliorer la qualité du cours
        suggestions = self.generate_improvement_suggestions(negative_comments, formulaires)
        report_content += f"\nSuggestions pour améliorer la qualité des cours :\n{suggestions}"

        return report_content

    def generate_improvement_suggestions(self, negative_comments, formulaires):
        """Génère des suggestions basées sur les commentaires négatifs des formulaires."""
        if not negative_comments:
            return "Aucune suggestion d'amélioration nécessaire."

        # Préparer le texte d'entrée pour Google Generative AI
        input_text = "Voici les commentaires négatifs des utilisateurs :\n" + "\n".join(negative_comments) + "\n\nQuelles améliorations pourraient être apportées ?"

        # Inclure des détails supplémentaires pour guider l'IA
        additional_context = (
            "Les utilisateurs se sont plaints de :\n"
            "- Difficultés de compréhension\n"
            "- Manque de matériel de soutien\n"
            "- Structure des cours peu claire\n"
            "- Feedback insuffisant sur les performances\n\n"
            "Veuillez fournir des suggestions spécifiques pour chaque problème."
        )

        input_text += additional_context

        # Utiliser Google Generative AI pour générer des suggestions d'amélioration
        try:
            # Configurer la génération
            generation_config = {
                "temperature": 0.7,
                "top_p": 0.95,
                "top_k": 64,
                "max_output_tokens": 300,
                "response_mime_type": "text/plain",
            }

            # Démarrer un modèle génératif
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",  # Remplacez par votre modèle
                generation_config=generation_config,
                system_instruction="Vous êtes un assistant d'IA pour améliorer les retours d'expérience.",
            )

            # Démarrer une session de chat pour obtenir une réponse
            chat_session = model.start_chat(
                history=[{"role": "user", "parts": [input_text]}]
            )
            response = chat_session.send_message(input_text)

            return response.text.strip()  # Retourne les suggestions générées
        except Exception as e:
            return f"Erreur lors de la génération des suggestions avec Google Generative AI : {str(e)}"
