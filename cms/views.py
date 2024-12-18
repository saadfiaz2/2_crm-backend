import openpyxl
from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .models import Quotation, Lead, Source, Medium, Document, Order, Note, Activity, Folder, Archive, Contact, \
    ContactActivity, ContactNote
from .serializers import LeadSerializer, QuotationSerializer, MediumSerializer, SourceSerializer, DocumentSerializer, \
    OrderSerializer, NoteSerializer, ActivitySerializer, LeadOrderSummarySerializer, FolderSerializer, \
    ArchiveSerializer, ContactSerializer, ContactActivitySerializer, ContactNoteSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from datetime import datetime, timezone
from django.db.models import Sum, Count
from rest_framework.decorators import action
from django.core.mail import send_mail
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


class SourceViewSet(viewsets.ModelViewSet):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
    permission_classes = [IsAuthenticated]


class MediumViewSet(viewsets.ModelViewSet):
    queryset = Medium.objects.all()
    serializer_class = MediumSerializer
    permission_classes = [IsAuthenticated]


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated]


class ContactActivityViewSet(viewsets.ModelViewSet):
    queryset = ContactActivity.objects.all()
    serializer_class = ContactActivitySerializer
    permission_classes = [IsAuthenticated]


class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]


class NotesViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]


class ContactNotesViewSet(viewsets.ModelViewSet):
    queryset = ContactNote.objects.all()
    serializer_class = ContactNoteSerializer
    permission_classes = [IsAuthenticated]


# class QuotationViewSet(viewsets.ModelViewSet):
#     queryset = Quotation.objects.all()
#     serializer_class = QuotationSerializer
#     permission_classes = [IsAuthenticated]


class QuotationViewSet(viewsets.ModelViewSet):
    queryset = Quotation.objects.all()
    serializer_class = QuotationSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='by-lead/(?P<lead_id>[^/.]+)')
    def get_by_lead(self, request, lead_id=None):
        """
        Custom action to retrieve quotations by lead ID.
        """
        try:
            quotations = Quotation.objects.filter(lead_id=lead_id)
            serializer = self.get_serializer(quotations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Lead.DoesNotExist:
            return Response({'error': 'Lead not found'}, status=status.HTTP_404_NOT_FOUND)


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()


class LeadByLeadGenManagerView(generics.ListAPIView):
    serializer_class = LeadSerializer

    def get_queryset(self):
        lead_gen_manager_id = self.kwargs['lead_gen_manager_id']
        return Lead.objects.filter(lead_gen_manager_id=lead_gen_manager_id)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"detail": "No leads found for this Lead Gen Manager ID"}, status=status.HTTP_404_NOT_FOUND)


class LeadSummaryView(APIView):
    def get(self, request):
        # Get current date and year/month filter if provided
        year = request.query_params.get('year', datetime.now().year)
        month = request.query_params.get('month', datetime.now().month)

        try:
            year, month = int(year), int(month)
            leads = Lead.objects.filter(created_date__year=year, created_date__month=month)
        except ValueError:
            return Response({"error": "Invalid year or month format"}, status=400)

        # Annotate leads with total order value and order count
        lead_summary = leads.annotate(
            total_order_value=Sum('orders__total_price'),
            order_count=Count('orders')
        )

        # Serialize and return the response
        serializer = LeadOrderSummarySerializer(lead_summary, many=True)
        return Response(serializer.data)


class LeadOrdersView(APIView):
    def get(self, request, lead_id):
        # Check if the lead exists
        try:
            lead = Lead.objects.get(id=lead_id)
        except Lead.DoesNotExist:
            return Response({"error": "Lead not found"}, status=status.HTTP_404_NOT_FOUND)

        # Retrieve all orders related to the lead
        orders = Order.objects.filter(lead=lead)

        # Serialize and return the orders
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def send_email(request):
    """
    API Endpoint to send emails.
    Expected JSON Payload:
    {
        "subject": "Email Subject",
        "message": "Email body message",
        "recipient": ["recipient@example.com"]
    }
    """
    data = request.data
    subject = data.get('subject')
    message = data.get('message')
    recipient = data.get('recipient', [])

    if not subject or not message or not recipient:
        return Response({"error": "Subject, message, and recipient fields are required."},
                        status=status.HTTP_400_BAD_REQUEST)

    try:
        send_mail(
            subject,
            message,
            'crm@argonteq.com',  # From email
            recipient,  # To email
            fail_silently=False
        )
        return Response({"message": "Email sent successfully."}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FolderViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing folders.
    """
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Folder.objects.filter(users=self.request.user)


class ArchiveViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing documents.
    """
    queryset = Archive.objects.all()
    serializer_class = ArchiveSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        accessible_folders = Folder.objects.filter(users=self.request.user)
        return Archive.objects.filter(folder__in=accessible_folders)


class ArchiveByFolderNameView(APIView):
    """
    API endpoint to get all documents in a folder by folder name.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, folder_name):
        try:
            # Find the folder with the given name that the user has access to
            folder = Folder.objects.get(name=folder_name, users=request.user)

            # Get all documents in that folder
            documents = Archive.objects.filter(folder=folder)

            # Serialize the documents
            serializer = ArchiveSerializer(documents, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Folder.DoesNotExist:
            documents = Archive.objects.all()
            serializer = ArchiveSerializer(documents, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)


class ImportContacts(APIView):
    def post(self, request):
        if 'file' not in request.FILES:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        file = request.FILES['file']

        try:
            workbook = openpyxl.load_workbook(file)
            sheet = workbook.active

            # Iterate through rows
            for row in sheet.iter_rows(min_row=2, values_only=True):  # Skip header row
                first_name, last_name, title, company, email, phone_number = row
                # Check if contact already exists
                if not Contact.objects.filter(email=email).exists():
                    Contact.objects.create(
                        first_name=first_name,
                        last_name=last_name,
                        title=title,
                        company=company,
                        email=email,
                        phone_number=phone_number,
                    )

            return Response({"message": "Contacts imported successfully"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]


class ArchiveByExtensionView(APIView):
    def get(self, request, extension):
        if not extension.startswith('.'):
            extension = f'.{extension}'
        archives = Archive.objects.filter(name__icontains=extension)
        serializer = ArchiveSerializer(archives, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
