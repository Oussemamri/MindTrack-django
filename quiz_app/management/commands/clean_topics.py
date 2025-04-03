from django.core.management.base import BaseCommand
from quiz_app.models import Topic

class Command(BaseCommand):
    help = 'Delete all topics except linux, devops, docker, code, and sql'

    def handle(self, *args, **options):
        # Keep only these topics
        keep_topics = ['linux', 'devops', 'docker', 'code', 'sql']
        
        # Delete other topics
        deleted_count = Topic.objects.exclude(name__in=keep_topics).delete()[0]
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully deleted {deleted_count} topics. Kept {len(keep_topics)} topics.')
        )