from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path
from django.template.response import TemplateResponse
from django.utils import timezone
from django.shortcuts import get_object_or_404
from transformers import pipeline  # Import Hugging Face library

from .models import Formulaire, Rapport, Course

# Initialize the Hugging Face summarization pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
suggestion_generator = pipeline("text-generation", model="gpt2")  # You can choose a different model if needed

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

            # Retrieve the course with error handling
            course = get_object_or_404(Course, id=course_id)
            report_text = self.create_report_text(course)

            # Save the report
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
        """Generate satisfaction report text for each chapter of the course."""
        report_content = f"Rapport de satisfaction pour le cours '{course.title}'\n\n"
        report_content += "Détails par chapitre:\n"
        
        positive_comments = []  # To store positive comments for conclusion
        negative_comments = []  # To store negative comments for conclusion

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

                # Classify comments based on ratings
                for f in formulaires:
                    if f.note < 3:
                        negative_comments.append(f.contenu)  # Collect negative comments
                    else:
                        positive_comments.append(f.contenu)  # Collect positive comments
                
                if average_rating < 3:
                    report_content += (
                        f"Attention : Ce chapitre présente une note faible de {average_rating:.2f}\n"
                    )
            else:
                report_content += f"Chapitre: {chapter.title} - Aucun formulaire de satisfaction reçu.\n\n"

        # Generate conclusions based on negative and positive comments
        if negative_comments:
            summary_text_neg = " ".join(negative_comments)
            conclusion_neg = summarizer(summary_text_neg, max_length=150, min_length=50, do_sample=False)
            report_content += f"\nConclusion sur les commentaires négatifs :\n{conclusion_neg[0]['summary_text']}"

        if positive_comments:
            summary_text_pos = " ".join(positive_comments)
            conclusion_pos = summarizer(summary_text_pos, max_length=150, min_length=50, do_sample=False)
            report_content += f"\nConclusion sur les commentaires positifs :\n{conclusion_pos[0]['summary_text']}"

        # Suggestions for improving course quality based on feedback
        suggestions = self.generate_improvement_suggestions(formulaires)
        report_content += f"\nSuggestions pour améliorer la qualité des cours :\n{suggestions}"

        return report_content

    def generate_improvement_suggestions(self, formulaires):
        """Generate suggestions based on comments from the forms."""
        comments = []

        for formulaire in formulaires:
            if formulaire.note < 5:  # Low rating
                comments.append(formulaire.contenu)



        # Prepare input for the AI model
        input_text = "Voici les commentaires des utilisateurs :\n" + "\n".join(comments) + "\n\nQuelles améliorations pourraient être apportées ?"

        # Generate suggestions using AI
        suggestions = suggestion_generator(input_text, max_length=150, num_return_sequences=1)

        return suggestions[0]['generated_text'].strip()  # Return the generated suggestion