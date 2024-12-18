from django.contrib import admin
from .models import Lead, Quotation, Source, Medium, Document, Order, Note, Activity, Folder, Archive, Contact

admin.site.register(Source)
admin.site.register(Medium)
admin.site.register(Lead)
admin.site.register(Quotation)
admin.site.register(Document)
admin.site.register(Order)
admin.site.register(Note)
admin.site.register(Activity)
admin.site.register(Folder)
admin.site.register(Contact)
admin.site.register(Archive)
