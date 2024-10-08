from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Problem(models.Model):
    name = models.CharField(max_length=50)
    statement = models.TextField()

    def __str__(self):
        return self.name


class CodeSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    problem = models.ForeignKey(Problem, on_delete= models.CASCADE, default=1)
    language = models.CharField(max_length=100)
    code = models.TextField()
    input_data = models.TextField(null=True, blank=True)
    output_data = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, null=True, blank=True)
    result = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.problem.name} - {self.status}"

class TestCase(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name= "test_cases")
    input_data = models.TextField()
    expected_output= models.TextField()
    is_sample = models.BooleanField(default=False)

    def __str__(self):
        return f"TestCase for {self.problem.name} - Input: {self.input_data}"