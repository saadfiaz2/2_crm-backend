from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Lead, Quotation, Source, Medium, Document, Order, Note, Activity, Folder, Archive, Contact, \
    ContactActivity, ContactNote


class LeadOrderSummarySerializer(serializers.ModelSerializer):
    total_order_value = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    order_count = serializers.IntegerField(read_only=True)
    created_date = serializers.SerializerMethodField()

    class Meta:
        model = Lead
        fields = ['id', 'name', 'created_date', 'total_order_value', 'order_count', 'status']

    def get_created_date(self, obj):
        return obj.created_date.strftime('%d-%m-%Y')


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = '__all__'


class MediumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medium
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'


class ActivitySerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Activity
        fields = ['id', 'created_at', 'user', 'text', 'lead']


class QuotationSerializer(serializers.ModelSerializer):
    approved_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    lead = serializers.PrimaryKeyRelatedField(queryset=Lead.objects.all(), write_only=True)
    approved_by_username = serializers.CharField(source='approved_by.username', read_only=True)

    class Meta:
        model = Quotation
        fields = ['id', 'customer_name', 'payment_list', 'approved_by', 'approved_by_username', 'payment_duration',
                  'created_at', 'lead']


class LeadSerializer(serializers.ModelSerializer):
    # Foreign key fields
    source_id = serializers.PrimaryKeyRelatedField(queryset=Source.objects.all(), source='source', write_only=True)
    medium_id = serializers.PrimaryKeyRelatedField(queryset=Medium.objects.all(), source='medium', write_only=True)
    assigned_to_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='assigned_to',
                                                        write_only=True)
    account_executive_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='account_executive',
                                                              write_only=True)
    sdr_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='sdr', write_only=True)
    lead_gen_manager_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='lead_gen_manager',
                                                             write_only=True)

    # Read-only fields for displaying related names
    source = serializers.CharField(source='source.name', read_only=True)
    medium = serializers.CharField(source='medium.name', read_only=True)
    assigned_to = serializers.CharField(source='assigned_to.username', read_only=True)
    account_executive = serializers.CharField(source='account_executive.username', read_only=True)
    sdr = serializers.CharField(source='sdr.username', read_only=True)
    lead_gen_manager = serializers.CharField(source='lead_gen_manager.username', read_only=True)
    created_date = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)

    # Document and Note fields
    lead_documents = serializers.ListField(child=serializers.FileField(), write_only=True, required=False)
    documents = DocumentSerializer(many=True, read_only=True)
    notes = NoteSerializer(many=True, read_only=True)
    activities = ActivitySerializer(many=True, read_only=True)

    class Meta:
        model = Lead
        fields = [
            'id', 'source_id', 'medium_id', 'assigned_to_id', 'account_executive_id', 'sdr_id', 'lead_gen_manager_id',
            'source', 'medium', 'assigned_to', 'account_executive', 'sdr', 'lead_gen_manager', 'name', 'gora',
            'connects', 'created_date', 'status', 'documents', 'approval_status', 'lead_documents', 'notes',
            'activities', 'communication_notes',
        ]

    def create(self, validated_data):
        # Extract documents data
        documents_data = validated_data.pop('lead_documents', [])
        # Create the lead
        lead = Lead.objects.create(**validated_data)
        # Create associated documents and link them to the lead
        if documents_data:
            document_instances = [Document.objects.create(file=file, name=file.name) for file in documents_data]
            lead.documents.set(document_instances)
        return lead

    def update(self, instance, validated_data):
        # Extract documents data
        documents_data = validated_data.pop('lead_documents', [])
        # Update the lead fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        # Clear existing documents and add the new ones if provided
        if documents_data:
            instance.documents.clear()
            document_instances = [Document.objects.create(file=file, name=file.name) for file in documents_data]
            instance.documents.set(document_instances)
        return instance


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class FolderSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
    last_modified = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Folder
        fields = ['id', 'name', 'users', 'last_modified','total_size']


class ArchiveSerializer(serializers.ModelSerializer):
    last_modified = serializers.DateTimeField(read_only=True)
    file_size = serializers.IntegerField(read_only=True)

    class Meta:
        model = Archive
        fields = ['id', 'name', 'file', 'folder', 'last_modified', 'file_size']

    def create(self, validated_data):
        # Automatically set the 'name' field to the filename from the 'file' field
        file = validated_data.get('file')
        if file:
            validated_data['name'] = file.name
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Automatically set the 'name' field to the filename from the 'file' field during update
        file = validated_data.get('file')
        if file:
            instance.name = file.name
        return super().update(instance, validated_data)



class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

class ContactActivitySerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = ContactActivity
        fields = ['id', 'created_at', 'user', 'text', 'contact']



class ContactNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactNote
        fields = '__all__'