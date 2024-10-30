from django import forms
from .models import Formulaire, Rapport, Course
from transformers import pipeline
import google.generativeai as genai

# Initialize Hugging Face summarizer
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
genai.configure(api_key="AIzaSyCXmHskLc0MkTDGtK0q_G2mLPieiuAXiXs")

class FormulaireForm(forms.ModelForm):
    class Meta:
        model = Formulaire
        fields = ['chapitre', 'contenu', 'type_formulaire', 'note', 'utilisateur']
        widgets = {
            'chapitre': forms.Select(attrs={'class': 'form-control'}),
            'contenu': forms.Textarea(attrs={'class': 'form-control'}),
            'type_formulaire': forms.Select(attrs={'class': 'form-control'}),
            'note': forms.Select(attrs={'class': 'form-control'}),
            'utilisateur': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'chapitre': 'Chapitre associé',
            'contenu': 'Contenu du retour',
            'type_formulaire': 'Type de formulaire',
            'note': 'Note',
            'utilisateur': 'Utilisateur',
        }

class RapportForm(forms.ModelForm):
    class Meta:
        model = Rapport
        fields = ['course', 'formulaire', 'contenu_rapport']
        widgets = {
            'contenu_rapport': forms.Textarea(attrs={'placeholder': 'Résumé du rapport ici...', 'readonly': 'readonly'}),
        }
        labels = {
            'course': 'Cours associé',
            'formulaire': 'Formulaire lié',
            'contenu_rapport': 'Contenu du rapport',
        }

    def __init__(self, *args, **kwargs):
        super(RapportForm, self).__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.all()
        self.fields['formulaire'].queryset = Formulaire.objects.all()

    def generate_report(self, course, formulaire):
        report_content = f"Rapport de satisfaction pour le cours '{course.title}'\n\nDétails par chapitre:\n"
        positive_comments = []
        negative_comments = []

        formulaires = Formulaire.objects.filter(chapitre__in=course.chapters.all())
        
        if formulaires.exists():
            for f in formulaires:
                average_rating = sum(f.note for f in formulaires) / formulaires.count()
                comments = "\n".join(f" - {f.contenu}" for f in formulaires)

                chapter_text = (
                    f"Chapitre: {f.chapitre.title}\n"
                    f"Note moyenne: {average_rating:.2f}\n"
                    f"Commentaires:\n{comments}\n\n"
                )

                report_content += chapter_text

                if f.note < 3:
                    negative_comments.append(f.contenu)
                else:
                    positive_comments.append(f.contenu)

            if negative_comments:
                summary_text_neg = " ".join(negative_comments)
                conclusion_neg = summarizer(summary_text_neg, max_length=150, min_length=50, do_sample=False)
                report_content += f"\nConclusion sur les commentaires négatifs :\n{conclusion_neg[0]['summary_text']}"

            if positive_comments:
                summary_text_pos = " ".join(positive_comments)
                conclusion_pos = summarizer(summary_text_pos, max_length=150, min_length=50, do_sample=False)
                report_content += f"\nConclusion sur les commentaires positifs :\n{conclusion_pos[0]['summary_text']}"

            suggestions = self.generate_improvement_suggestions(negative_comments)
            report_content += f"\nSuggestions pour améliorer la qualité des cours :\n{suggestions}"

        return report_content

    def generate_improvement_suggestions(self, negative_comments):
        if not negative_comments:
            return "Aucune suggestion d'amélioration nécessaire."

        input_text = "Voici les commentaires négatifs des utilisateurs :\n" + "\n".join(negative_comments) + "\n\nQuelles améliorations pourraient être apportées ?"
        
        try:
            generation_config = {
                "temperature": 0.7,
                "top_p": 0.95,
                "top_k": 64,
                "max_output_tokens": 300,
                "response_mime_type": "text/plain",
            }

            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                generation_config=generation_config,
                system_instruction="Vous êtes un assistant d'IA pour améliorer les retours d'expérience.",
            )

            chat_session = model.start_chat(history=[{"role": "user", "parts": [input_text]}])
            response = chat_session.send_message(input_text)

            return response.text.strip()
        except Exception as e:
            return f"Erreur lors de la génération des suggestions : {str(e)}"
