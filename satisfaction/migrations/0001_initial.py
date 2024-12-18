# Generated by Django 4.2 on 2024-10-25 13:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Formulaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chapitre', models.CharField(max_length=255)),
                ('contenu', models.TextField()),
                ('date_remplissage', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Rapport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contenu_rapport', models.TextField()),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('formulaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rapports', to='satisfaction.formulaire')),
            ],
        ),
    ]
