from django.db import models
# Create your models here.


class ChunkedUpload(models.Model):
    video = models.ForeignKey('yourapp.Video', on_delete=models.CASCADE)
    chunk = models.FileField(upload_to='chunked_uploads/')
    sequence = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.video.title} - Chunk {self.sequence}"
