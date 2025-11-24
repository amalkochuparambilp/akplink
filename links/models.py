from django.db import models
from django.contrib.auth.models import User


class LinkPage(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="link_page"
    )
    display_name = models.CharField(max_length=100, blank=True)
    bio = models.CharField(max_length=200, blank=True)
    avatar_initials = models.CharField(max_length=4, blank=True)

    def __str__(self):
        return f"{self.user.username}'s link page"

    @property
    def name(self):
        return self.display_name or self.user.get_username()

    @property
    def initials(self):
        if self.avatar_initials:
            return self.avatar_initials
        # Simple automatic initials from username
        return (self.user.get_username()[:2] or "U").upper()


class Link(models.Model):
    page = models.ForeignKey(
        LinkPage,
        on_delete=models.CASCADE,
        related_name="links",
    )
    title = models.CharField(max_length=100)
    url = models.URLField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.title} ({self.page.user.username})"