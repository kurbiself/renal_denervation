from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Patient)
admin.site.register(PatientDesease)
admin.site.register(Disease)
admin.site.register(Hospital)
admin.site.register(TypeCheckPoint)
admin.site.register(CheckPoint)
admin.site.register(Medicine)
admin.site.register(TreatmentDrug)
admin.site.register(SurgicalOperation)
admin.site.register(AblationSite)
admin.site.register(Unit)
admin.site.register(PharmacologicalGroup)
admin.site.register(ActiveIngredient)
admin.site.register(CatheterType)
admin.site.register(Metric)
admin.site.register(VariantQualitative)
admin.site.register(ResearchTemplate)
admin.site.register(MetricsTemplates)
admin.site.register(Research)
admin.site.register(MetricValue)
