from django.contrib import admin
from dataModel.models import *

# Register your models here.
admin.site.register(User)
admin.site.register(OriginalData)
admin.site.register(AssociationRulesWithData)
admin.site.register(AssociationRulesWithStandard)
admin.site.register(FrequentItemsetsWithData)
admin.site.register(FrequentItemsetsWithStandard)
admin.site.register(Article)