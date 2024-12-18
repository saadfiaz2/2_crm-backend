from django.urls import path, include
from rest_framework.routers import DefaultRouter

from projects.views import DocumentViewSet
from .views import LeadViewSet, QuotationViewSet, SourceViewSet, MediumViewSet, OrderViewSet, NotesViewSet, \
    ActivityViewSet, LeadSummaryView, LeadOrdersView, send_email, FolderViewSet, ArchiveViewSet, \
    ArchiveByFolderNameView, ImportContacts, ContactViewSet, ArchiveByExtensionView, ContactActivityViewSet, \
    ContactNotesViewSet

router = DefaultRouter()

router.register(r'sources', SourceViewSet)
router.register(r'mediums', MediumViewSet)
router.register(r'leads', LeadViewSet)
router.register(r'quotations', QuotationViewSet)
router.register(r'documents', DocumentViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'activity', ActivityViewSet)
router.register(r'contact-activity', ContactActivityViewSet)
router.register(r'notes', NotesViewSet)
router.register(r'contact-notes', ContactNotesViewSet)
router.register(r'folders', FolderViewSet)
router.register(r'archive', ArchiveViewSet)
router.register(r'contact', ContactViewSet)




urlpatterns = [
    path('', include(router.urls)),
    path('lead-summary/', LeadSummaryView.as_view(), name='lead-summary'),
    path('leads/<int:lead_id>/orders/', LeadOrdersView.as_view(), name='lead-orders'),
    path('send-email/', send_email, name='send_email'),
    path('folders/<str:folder_name>/archive/', ArchiveByFolderNameView.as_view(), name='documents-by-folder-name'),
    path('import-contacts/', ImportContacts.as_view(), name='import_contacts'),
    path('archives/extension/<str:extension>/', ArchiveByExtensionView.as_view(), name='archive-by-extension'),

]
