from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import serializers
from rest_framework.permissions import AllowAny
from django.contrib.auth.password_validation import validate_password

from users.models import Profile, Education, WorkExperience, Skill

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile


class RegisterSerializer(serializers.ModelSerializer):
    # User fields
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=False)

    # Profile fields
    role = serializers.ChoiceField(choices=Profile.ROLE_CHOICES, default='Employee')
    profile_photo = serializers.ImageField(required=False)
    cnic = serializers.CharField(required=False, max_length=13)
    date_of_birth = serializers.DateField(required=False)
    date_of_joining = serializers.DateField(required=False)
    designation = serializers.CharField(required=False, max_length=100)
    salary = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    description = serializers.CharField(required=False,allow_null=True,allow_blank=True)
    mobile_number = serializers.CharField(required=False, max_length=15)
    address = serializers.CharField()
    nationality = serializers.CharField(required=False, max_length=100)
    gender = serializers.ChoiceField(choices=Profile.GENDER_CHOICES, required=False)
    marital_status = serializers.CharField(required=False, max_length=50)
    religion = serializers.CharField(required=False, max_length=50)
    employment_of_spouse = serializers.CharField(required=False, max_length=100)
    number_of_children = serializers.IntegerField(required=False)
    bank_name = serializers.CharField(required=False, max_length=100)
    account_holder_name = serializers.CharField(required=False, max_length=100)
    account_number = serializers.CharField(required=False, max_length=30)
    iban_number = serializers.CharField(required=False, max_length=34)
    lead = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all(), required=False)
    emergency_contact_primary_name = serializers.CharField(required=False, max_length=100)
    emergency_contact_primary_relationship = serializers.CharField(required=False, max_length=50)
    emergency_contact_primary_phone = serializers.CharField(required=False, max_length=15)
    emergency_contact_secondary_name = serializers.CharField(required=False, max_length=100)
    emergency_contact_secondary_relationship = serializers.CharField(required=False, max_length=50)
    emergency_contact_secondary_phone = serializers.CharField(required=False, max_length=15)
    skills = serializers.PrimaryKeyRelatedField(queryset=Skill.objects.all(), many=True, required=False)
    casual_leave_quota = serializers.FloatField(required=False)
    sick_leave_quota = serializers.FloatField(required=False)
    annual_leave_quota = serializers.FloatField(required=False)

    class Meta:
        model = User
        fields = [
            'username', 'password', 'email', 'role', 'profile_photo', 'cnic', 'date_of_birth', 'date_of_joining',
            'designation', 'salary', 'description', 'mobile_number', 'address', 'nationality',
            'gender', 'marital_status', 'religion', 'employment_of_spouse', 'number_of_children', 'bank_name',
            'account_holder_name', 'account_number', 'iban_number', 'lead', 'emergency_contact_primary_name',
            'emergency_contact_primary_relationship', 'emergency_contact_primary_phone',
            'emergency_contact_secondary_name',
            'emergency_contact_secondary_relationship', 'emergency_contact_secondary_phone', 'skills',
            'casual_leave_quota', 'sick_leave_quota', 'annual_leave_quota'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'required': True},
            'address': {'required': True},
        }

    def create(self, validated_data):
        # Separate User fields
        user_data = {
            'username': validated_data.pop('email'),
            'password': validated_data.pop('password'),
            'email': validated_data.get('email', '')
        }

        # Create User instance
        user = User.objects.create_user(**user_data)

        # Prepare Profile data
        profile_data = {}
        profile_fields = {field.name for field in Profile._meta.fields}
        for field in profile_fields:
            if field in validated_data:
                profile_data[field] = validated_data[field]

        # Create Profile instance
        Profile.objects.create(user=user, **profile_data)

        return user

        return user, profile.id

class UserProfileSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='profile.role')

    class Meta:
        model = User
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError("User account is disabled.")
            else:
                raise serializers.ValidationError("Unable to log in with provided credentials.")
        else:
            raise serializers.ValidationError("Must include 'username' and 'password'.")
        data["user"] = user
        return data


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'  # Include any fields you need from the Profile model


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'  # Include any fields you need from the Profile model


class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = '__all__'  # Include any fields you need from the Profile model


class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField(source='profile.role')
    profile = ProfileSerializer()
    education = EducationSerializer(source='profile.educations', many=True, read_only=True)
    experience = WorkSerializer(source='profile.work_experiences', many=True, read_only=True)

    class Meta:
        model = User
        fields = '__all__'

    def get_role(self, obj):
        return obj.profile.role


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError('User with this email does not exist.')
        return value

    def save(self):
        request = self.context.get('request')
        user = User.objects.get(email=self.validated_data['email'])
        token = PasswordResetTokenGenerator().make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_url = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
        frontend_reset_url = f"{request.scheme}://localhost:3000/react/template/reset-password/{uid}/{token}/"
        subject = 'Password Reset Requested'
        message = f'Please click the link below to reset your password:\n{frontend_reset_url}'
        send_mail(subject, message, 'shahmeerhussainkhadmi@gmail.com', [user.email])


class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def save(self, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError('Invalid token')

        user.set_password(self.validated_data['new_password'])
        user.save()
class RoleFilterSerializer(serializers.Serializer):
    roles = serializers.ListField(
        child=serializers.ChoiceField(choices=Profile.ROLE_CHOICES),
        allow_empty=False
    )