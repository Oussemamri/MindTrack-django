from django.db import migrations

def populate_topics(apps, schema_editor):
    Topic = apps.get_model('quiz_app', 'Topic')
    topics_data = [
        ('linux', 'Learn about Linux operating system'),
        ('devops', 'DevOps practices and methodologies'),
        ('docker', 'Docker containerization'),
        ('code', 'General programming concepts'),
        ('sql', 'Database and SQL queries'),
    ]
    
    for name, description in topics_data:
        Topic.objects.get_or_create(
            name=name,
            defaults={
                'description': description,
                'slug': name.lower()
            }
        )

def reverse_populate(apps, schema_editor):
    Topic = apps.get_model('quiz_app', 'Topic')
    Topic.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('quiz_app', '0002_topic_slug'),
    ]

    operations = [
        migrations.RunPython(populate_topics, reverse_populate),
    ]