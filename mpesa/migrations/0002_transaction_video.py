# Generated by Django 4.2.7 on 2023-12-02 08:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0003_alter_video_thumbnail'),
        ('mpesa', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='video',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='videos.video'),
        ),
    ]