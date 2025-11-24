from rest_framework import serializers
from api.models import Member, Message


class MemberSerializer(serializers.ModelSerializer):
    """Serializer for Member model - excludes password from output"""
    
    class Meta:
        model = Member
        fields = ['id', 'username', 'created_at']
        read_only_fields = ['id', 'created_at']


class MemberRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for Member registration with password validation and hashing"""
    password = serializers.CharField(
        write_only=True,
        min_length=6,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = Member
        fields = ['id', 'username', 'password', 'created_at']
        read_only_fields = ['id', 'created_at']
        extra_kwargs = {
            'username': {
                'min_length': 3,
                'max_length': 50
            }
        }
    
    def validate_username(self, value):
        """Validate username uniqueness"""
        if Member.objects.filter(username=value).exists():
            raise serializers.ValidationError("Пользователь с таким именем уже существует")
        return value
    
    def validate_password(self, value):
        """Validate password strength"""
        if len(value) < 6:
            raise serializers.ValidationError("Пароль должен содержать минимум 6 символов")
        return value
    
    def create(self, validated_data):
        """Create member with hashed password"""
        password = validated_data.pop('password')
        member = Member(**validated_data)
        member.set_password(password)
        member.save()
        return member


class MemberLoginSerializer(serializers.Serializer):
    """Serializer for login validation"""
    username = serializers.CharField(
        min_length=3,
        max_length=50
    )
    password = serializers.CharField(
        min_length=6,
        write_only=True,
        style={'input_type': 'password'}
    )
    
    def validate(self, attrs):
        """Validate credentials"""
        username = attrs.get('username')
        password = attrs.get('password')
        
        try:
            member = Member.objects.get(username=username)
        except Member.DoesNotExist:
            raise serializers.ValidationError("Неверные учетные данные")
        
        if not member.check_password(password):
            raise serializers.ValidationError("Неверные учетные данные")
        
        attrs['member'] = member
        return attrs


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message model - includes username from related Member"""
    username = serializers.CharField(source='member.username', read_only=True)
    member_id = serializers.IntegerField(source='member.id', read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'member_id', 'username', 'text', 'created_at']
        read_only_fields = ['id', 'member_id', 'username', 'created_at']


class MessageCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating messages - accepts member_id and text"""
    member_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Message
        fields = ['member_id', 'text']
        extra_kwargs = {
            'text': {
                'min_length': 1,
                'max_length': 1000
            }
        }
    
    def validate_member_id(self, value):
        """Validate that member exists"""
        if not Member.objects.filter(id=value).exists():
            raise serializers.ValidationError("Пользователь не найден")
        return value
    
    def validate_text(self, value):
        """Validate message text"""
        if not value.strip():
            raise serializers.ValidationError("Сообщение не может быть пустым")
        return value
    
    def create(self, validated_data):
        """Create message with member relationship"""
        member_id = validated_data.pop('member_id')
        member = Member.objects.get(id=member_id)
        message = Message.objects.create(member=member, **validated_data)
        return message
