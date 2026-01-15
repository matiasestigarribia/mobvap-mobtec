import os
from django.core.management.base import BaseCommand
from django.core.files import File
from photos.models import Photo
from editions.models import Edition


class Command(BaseCommand):
    help = 'import photos from a local folder to a specific edition'
    
    def add_arguments(self, parser):
        parser.add_argument('folder_path', type=str, help='path to folder with photos')
        parser.add_argument('edition_slug', type=str, help='Editions slug where will be saved')
        parser.add_argument('--desc', type=str, help=' Standart descrption to all photos', default='')
        
    def handle(self, *args, **options):
        folder_path = options['folder_path']
        edition_slug = options['edition_slug']
        description = options['desc']
        
        try:
            edition = Edition.objects.get(slug=edition_slug)
            self.stdout.write(self.style.SUCCESS(f'Edition founded: {edition.edition_name}'))
            
        except Edition.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Error: edition with slug "{edition_slug} not found.'))
            return
        
        if not os.path.exists(folder_path):
            self.stdout.write(self.style.ERROR(f'Error: folder not found: {folder_path}'))
            return
    
        valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
        files = [f for f in os.listdir(folder_path) if any(f.lowe().endswith(ext) for ext in valid_extensions)]
        self.stdout.write(f'Founded {len(files)} images. Importing images...')
        
        count = 0
        for filename in files:
            file_path = os.path.join(folder_path, filename)
            
            try:
                with open(file_path, 'rb') as f:
                    photo = Photo(
                        image_title=filename,
                        image_description=description,
                        edition=edition,
                    )
                    
                    photo.image_file.save(filename, File(f), save=True)
                    
                    count += 1
                    self.stdout.write(f'Saved: {filename}')
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error while saving {filename}: {e}'))
        self.stdout.write(self.style.SUCCESS(f'Concluded! {count} imported photos'))        