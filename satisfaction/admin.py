from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path
from django.template.response import TemplateResponse
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import Formulaire, Rapport, Course

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

            course = get_object_or_404(Course, id=course_id)
            report_text = self.create_report_text(course)
            conclusion_text = self.generate_conclusion_text(course)  # Utilisation de l'IA pour générer la conclusion

            Rapport.objects.create(
                course=course,
                contenu_rapport=report_text + "\n\nConclusion:\n" + conclusion_text,
                date_creation=timezone.now()
            )

            self.message_user(request, "Rapport généré avec succès.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        context = {'courses': Course.objects.all()}
        return TemplateResponse(request, 'admin/generate_report.html', context)

    def create_report_text(self, course):
        report_content = f"Rapport de satisfaction pour le cours '{course.title}'\n\n"
        report_content += "Détails par chapitre:\n"
        
        for chapter in course.chapters.all():
            formulaires = Formulaire.objects.filter(chapitre=chapter)
            if formulaires.exists():
                average_rating = sum(f.note for f in formulaires) / formulaires.count()
                total_responses = formulaires.count()
                comments = "\n".join(f" - {f.contenu}" for f in formulaires)

                report_content += (
                    f"Chapitre: {chapter.title}\n"
                    f"Note moyenne: {average_rating:.2f}\n"
                    f"Total des réponses: {total_responses}\n"
                    f"Commentaires:\n{comments}\n\n"
                )

                if average_rating < 3:
                    report_content += (
                        f"Attention : Ce chapitre présente une note faible de {average_rating:.2f}\n"
                    )
            else:
                report_content += f"Chapitre: {chapter.title} - Aucun formulaire de satisfaction reçu.\n\n"

        return report_content

    def generate_conclusion_text(self, course):
        """
        Génère une conclusion synthétique du rapport de satisfaction.
        Utilisez une IA pour identifier les points forts et faibles du cours.
        """
        low_rating_chapters = []
        high_rating_chapters = []

        for chapter in course.chapters.all():
            formulaires = Formulaire.objects.filter(chapitre=chapter)
            if formulaires.exists():
                average_rating = sum(f.note for f in formulaires) / formulaires.count()
                if average_rating < 3:
                    low_rating_chapters.append(chapter.title)
                elif average_rating >= 4:
                    high_rating_chapters.append(chapter.title)

        conclusion = "Après analyse des retours, voici les principales observations :\n\n"

        if high_rating_chapters:
            conclusion += (
                "Points forts : Les chapitres suivants ont reçu des retours très positifs : "
                + ", ".join(high_rating_chapters) + ".\n"
            )
        
        if low_rating_chapters:
            conclusion += (
                "Points à améliorer : Les chapitres suivants ont été notés de manière moins favorable : "
                + ", ".join(low_rating_chapters) + ".\n"
            )
        
        if not high_rating_chapters and not low_rating_chapters:
            conclusion += "Les notes sont globalement moyennes, sans chapitre particulièrement élevé ou faible."

        return conclusion
