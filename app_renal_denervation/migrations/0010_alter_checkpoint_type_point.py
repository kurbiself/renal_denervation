# Generated by Django 4.2 on 2025-04-02 15:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_renal_denervation', '0009_cathetertype_note_disease_note_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkpoint',
            name='type_point',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='points', to='app_renal_denervation.typecheckpoint', verbose_name='Тип контрольной точки'),
            preserve_default=False,
        ),
    ]
