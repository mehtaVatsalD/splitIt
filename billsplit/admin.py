from django.contrib import admin
from .models import Group, GroupAllocation, Bill, BillSharer, Transaction, RequestSettlement, SetteledTransaction

# Register your models here.
admin.site.register(Group)
admin.site.register(GroupAllocation)
admin.site.register(Bill)
admin.site.register(BillSharer)
admin.site.register(Transaction)
admin.site.register(RequestSettlement)
admin.site.register(SetteledTransaction)
