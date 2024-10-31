# Generated by Django 5.1.2 on 2024-10-29 02:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Exercice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paragraphe', models.TextField()),
                ('reponse1', models.CharField(max_length=100)),
                ('reponse2', models.CharField(max_length=100)),
                ('reponse3', models.CharField(max_length=100)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReponseExercice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reponse_etudiant1', models.CharField(max_length=100)),
                ('reponse_etudiant2', models.CharField(max_length=100)),
                ('reponse_etudiant3', models.CharField(max_length=100)),
                ('note', models.FloatField(blank=True, null=True)),
                ('date_reponse', models.DateTimeField(auto_now_add=True)),
                ('exercice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exercices.exercice')),
            ],
        ),
    ]