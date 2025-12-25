# Generated manually for index optimization

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_course_raw_summary_alter_course_course_image_and_more'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='course',
            index=models.Index(fields=['name', 'professor', '-study_start'], name='idx_course_dedup'),
        ),
        migrations.AddIndex(
            model_name='course',
            index=models.Index(fields=['classfy_name'], name='idx_classfy'),
        ),
        migrations.AddIndex(
            model_name='course',
            index=models.Index(fields=['middle_classfy_name'], name='idx_middle_classfy'),
        ),
        migrations.AddIndex(
            model_name='course',
            index=models.Index(fields=['name'], name='idx_course_name'),
        ),
        migrations.AddIndex(
            model_name='course',
            index=models.Index(fields=['org_name'], name='idx_org_name'),
        ),
        migrations.AddIndex(
            model_name='course',
            index=models.Index(fields=['professor'], name='idx_professor'),
        ),
    ]
