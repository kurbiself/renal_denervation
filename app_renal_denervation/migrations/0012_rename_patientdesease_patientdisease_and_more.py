# Generated by Django 4.2 on 2025-05-23 18:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_renal_denervation', '0011_alter_metric_shortname_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PatientDesease',
            new_name='PatientDisease',
        ),
        migrations.AlterField(
            model_name='medicine',
            name='active_ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medicines', to='app_renal_denervation.activeingredient', verbose_name='Активное вещество'),
        ),
        migrations.AlterField(
            model_name='metricstemplates',
            name='metric_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='metrics_templates', to='app_renal_denervation.metric', verbose_name='Показатель'),
        ),
        migrations.RemoveField(
            model_name='metricvalue',
            name='value_qualitative_id',
        ),
        migrations.AddField(
            model_name='metricvalue',
            name='value_qualitative_id',
            field=models.ForeignKey(default=2014, on_delete=django.db.models.deletion.CASCADE, to='app_renal_denervation.variantqualitative', verbose_name='Значение качественногоо признака'),
            preserve_default=False,
        ),
    ]
