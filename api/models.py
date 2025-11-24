from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class Member(models.Model):
    """Member model for chat users"""
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    auth_token = models.CharField(max_length=64, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'members'
        ordering = ['-created_at']

    def __str__(self):
        return self.username

    def set_password(self, raw_password):
        """Hash and set password"""
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """Check if provided password is correct"""
        return check_password(raw_password, self.password)

    @property
    def is_authenticated(self):
        """Always return True for compatibility with DRF"""
        return True

    @property
    def is_anonymous(self):
        """Always return False for compatibility with DRF"""
        return False

    def has_perm(self, perm, obj=None):
        """Simple permission check for DRF compatibility"""
        return True

    def has_module_perms(self, app_label):
        """Simple module permission check for DRF compatibility"""
        return True


class Message(models.Model):
    """Message model for chat messages"""
    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    text = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'messages'
        ordering = ['created_at']

    def __str__(self):
        return f"{self.member.username}: {self.text[:50]}"
