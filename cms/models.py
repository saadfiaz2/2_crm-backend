from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver


class Source(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Medium(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Document(models.Model):
    file = models.FileField(upload_to='lead_documents/')
    name = models.CharField(max_length=100, default='none')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Document for {self.file.name}"


class Quotation(models.Model):
    PAYMENT_CHOICES = [
        ('PKR', 'PKR'),
        ('USD', 'USD'),
    ]

    PAYMENT_DURATION_CHOICES = [
        (15, '15 days'),
        (30, '30 days'),
        (45, '45 days'),
        (60, '60 days'),
    ]
    customer_name = models.CharField(max_length=100, default='none')
    payment_list = models.CharField(max_length=3, choices=PAYMENT_CHOICES, default='USD')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    payment_duration = models.IntegerField(choices=PAYMENT_DURATION_CHOICES, default=25)
    created_at = models.DateTimeField(auto_now_add=True)
    lead = models.ForeignKey('Lead', on_delete=models.CASCADE, related_name='quotations', null=True)

    def __str__(self):
        return f"Quotation for {self.customer_name} - {self.get_payment_list_display()}"


class Lead(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('opportunity', 'Opportunity'),
        ('quotation', 'Quotation'),
        ('win', 'Win'),
        ('lost', 'Lost'),
    ]

    APPROVAL_CHOICES = [
        ('approved', 'Approved'),
        ('disapproved', 'DisApproved'),
        ('pending', 'Pending'),

    ]

    name = models.CharField(max_length=255)
    source = models.ForeignKey(Source, on_delete=models.SET_NULL, null=True, related_name='source')
    medium = models.ForeignKey(Medium, on_delete=models.SET_NULL, null=True, related_name='medium')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='leads_assigned')
    account_executive = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                          related_name='leads_account_executive')
    sdr = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='leads_sdr')
    lead_gen_manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                         related_name='leads_lead_gen_manager')
    gora = models.TextField(null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    connects = models.IntegerField(default=0, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    documents = models.ManyToManyField(Document, related_name='leads', blank=True)
    communication_notes = models.TextField(blank=True, null=True, default="NULL")
    approval_status = models.CharField(max_length=20, choices=APPROVAL_CHOICES, default='approved')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    lead = models.ForeignKey(Lead, related_name='orders', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.total_price = self.unit_price * self.quantity
        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.name}"


class Note(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='notes')
    title = models.TextField()
    note = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Note for {self.lead.name} by {self.created_by.username if self.created_by else 'Unknown'}"


class Activity(models.Model):
    lead = models.ForeignKey('Lead', on_delete=models.CASCADE, related_name='activities')
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    text = models.TextField()

    def __str__(self):
        return f"Activity for {self.lead.name} by {self.user.username if self.user else 'Unknown'}"


class Folder(models.Model):
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(User, related_name='folders')  # Many-to-Many relation with User
    last_modified = models.DateTimeField(auto_now=True)  # Updates on every modification
    total_size = models.PositiveIntegerField(default=0)  # Stored in bytes

    def __str__(self):
        return self.name


class Archive(models.Model):
    name = models.CharField(max_length=255, default="document-1")
    file = models.FileField(upload_to='documents/')
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='documents')

    last_modified = models.DateTimeField(auto_now=True)  # Updates on every modification
    file_size = models.PositiveIntegerField(null=True, blank=True)  # Size in bytes

    def save(self, *args, **kwargs):
        # Automatically calculate file size if a file is uploaded
        if self.file and hasattr(self.file, 'size'):
            self.file_size = self.file.size

        super().save(*args, **kwargs)


class Contact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    title = models.CharField(max_length=100, null=True, blank=True)
    company = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


@receiver(post_save, sender=Archive)
def update_folder_total_size_on_save(sender, instance, **kwargs):
    folder = instance.folder
    folders = Archive.objects.filter(folder__name=folder.name)
    folder.total_size = sum(doc.file_size for doc in folders)
    folder.save()


@receiver(post_delete, sender=Archive)
def update_folder_total_size_on_delete(sender, instance, **kwargs):
    folder = instance.folder
    folders = Archive.objects.filter(folder__name=folder.name)
    folder.total_size = sum(doc.file_size for doc in folders)
    folder.save()


class ContactActivity(models.Model):
    contact = models.ForeignKey('Contact', on_delete=models.CASCADE, related_name='activities')
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    text = models.TextField()

    def __str__(self):
        return f"Activity for {self.contact.first_name} by {self.user.username if self.user else 'Unknown'}"


class ContactNote(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='notes')
    title = models.TextField()
    note = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Note for {self.contact.first_name} by {self.created_by.username if self.created_by else 'Unknown'}"