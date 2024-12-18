# Generated by Django 4.2 on 2024-10-27 13:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('satisfaction', '0004_formulaire_utilisateur_alter_rapport_course'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formulaire',
            name='utilisateur',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='formulaires', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='rapport',
            name='formulaire',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rapports', to='satisfaction.formulaire'),
        ),
    ]
