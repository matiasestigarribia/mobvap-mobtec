import os
import zipfile
from django.core.management.base import BaseCommand
from django.core.files import File
from photos.models import Photo
from editions.models import Edition


class Command(BaseCommand):
    help = 'import photos from a local folder to a specific edition'
    
    def add_arguments(self, parser):
        parser.add_argument('zip_path', type=str, help='path to .zip with photos')
        parser.add_argument('edition_slug', type=str, help='Editions slug where will be saved')
        parser.add_argument('--desc', type=str, help=' Standart descrption to all photos', default='')
        
    def handle(self, *args, **options):
        zip_path = options['zip_path']
        edition_slug = options['edition_slug']
        description = options['desc']
        
        try:
            edition = Edition.objects.get(slug=edition_slug)
            self.stdout.write(self.style.SUCCESS(f'Edition founded: {edition.edition_name}'))
            
        except Edition.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Error: edition with slug "{edition_slug} not found.'))
            return
        
        if not os.path.exists(zip_path):
            self.stdout.write(self.style.ERROR(f'Error: folder not found: {zip_path}'))
            return
    
        try:
            with zipfile.ZipFile(zip_path, 'r') as z:
                valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
                all_files = z.namelist()
                image_files = [f for f in all_files if f.lower().endswith(valid_extensions) and not f.startswith('__MACOSX')]
        
            self.stdout.write(f'Founded {len(image_files)} images within zip. Importing images...')
        
            count = 0
            for filename in files:
                simple_name = os.path.basename(filename)
                
                if not simple_name:
                    continue
                    
                try:
                    file_content = z.read(filename)
                    photo= Photo(
                        image_title=simple_name,
                        image_description=description,
                        edition=edition,
                    )
                    photo.image_file.save(simple_name, ContentFile(file_content), save=True)
                    count += 1
                    self.stdout.write(f'Saved: {simple_name}')
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Failed saving {simple_name}: {e}'))
            
            self.stdout.write(self.style.SUCCESS(f'Concluded! {count} imported photos'))
        except zipfile.BadZipFile:
            self.stdout.write(self.style.ERROR('Zip file not valid or corrupted'))
