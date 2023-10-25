from django.db import models

# Create your models here.

class MealType(models.Model):
    """A type of meal which user is adding."""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Meal Types'

    def __str__(self):
        """Return a string representation of the model."""
        return self.text

class Entry(models.Model):
    """A specific idea for the given meal type."""
    meal_type = models.ForeignKey(MealType, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        """Return a simple string representing the entry."""
        return f"{self.text[:50]}..." if len(self.text) > 50 else f"{self.text}"

    