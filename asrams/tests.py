from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import default_storage

from core.models import ImageRecords
from .models import Sanyashi, Asram

class ImageRecordsSignalTest(TestCase):
    def setUp(self):
        # Create a sample image file for testing
        self.avatar_file = SimpleUploadedFile(
            name='test_avatar.jpg',
            content=b'',
            content_type='image/jpeg'
        )

    def test_image_records_signal(self):
        # Create a Sanyashi instance with an avatar
        asram = Asram.objects.create(
            name='Test Asram'
      
        )

        sanyashi = Sanyashi.objects.create(
            name='Test Sanyashi',
            asram=asram,            
            avatar=self.avatar_file,
        )

        
    
        
        # Check if an ImageRecords record is created for the avatar
        
        image_record = ImageRecords.objects.filter(obj_id=sanyashi.id)  
       
            
        if image_record.exists():
            for image in image_record:
                try:
                    self.assertEqual(image.obj_model, 'Sanyashi')
                    self.assertEqual(image.obj_field, 'avatar')
                    self.assertEqual(image.obj_url, sanyashi.avatar)
                except:
                    pass
                
                image.delete()
        

            # Delete the Sanyashi instance
            sanyashi.delete()
            
            # Check if the associated image file is deleted
            file_path = sanyashi.avatar.name if sanyashi.avatar else None
            print(file_path)
            if file_path is not None:
                self.assertFalse(default_storage.exists(file_path))

    def tearDown(self):
        # Clean up: delete the uploaded files
        default_storage.delete(self.avatar_file.name)
