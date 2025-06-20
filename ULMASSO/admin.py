from django.contrib import admin
from Intranet.models import Member,\
                            BudgetBudget,\
                            BudgetSection,\
                            BudgetProjet,\
                            BudgetLigne,\
                            BudgetOperation

admin.site.register(Member)
admin.site.register(BudgetBudget)
admin.site.register(BudgetSection)
admin.site.register(BudgetProjet)
admin.site.register(BudgetLigne)
admin.site.register(BudgetOperation)