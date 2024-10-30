# Generated by Django 4.2 on 2024-10-25 14:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Course', '0001_initial'),
        ('satisfaction', '0002_formulaire_note_formulaire_type_formulaire_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='rapport',
            name='course',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='rapports', to='Course.course'),
        ),
    ]