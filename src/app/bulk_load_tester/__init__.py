from tunobase.bulk_loading.bulk_updaters import BulkUpdater
from tunobase.corporate.media.models import Article

class BulkUpdaterTest(BulkUpdater):
    data_key = 'title'
    model = Article
    
    def bulk_create_objects(self, object_list):
        self.model.objects.bulk_create(object_list)
    
    def create_object(self, data):
        return self.model(
            title=data['title'],
            plain_content=data['plain_content']
        )
    
    def update_object(self, obj, data, created):
        obj.plain_content=data['plain_content']
        obj.save()