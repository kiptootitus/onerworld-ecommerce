from datetime import datetime 
from config_master import TZ

from django.db import models
from utils import generate_random_string


class BaseModel(models.Model):
    """
    This is the base model for all models in the application
    """
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=500, default='', null=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    modified_by = models.CharField(max_length=500, default='', null=True)
    class Meta:
        abstract = True
        
        
        
def unique_id_generator(id_string: str = None) -> str:
  """
  This method generates a unique id for the model
  :param id_string: The string to be used as a prefix
  :return: str
  """
  if id_string:
    id_string_split = id_string.split('_')
    increment_value = id_string_split[-1]
    increment_value = int(increment_value) + 1
    return f'{str(id_string_split[0])}-{str(increment_value)}'
  now = datetime.now(TZ)
  time_string = now.strftime('%Y%m%d%H%M%S')
  return f'{time_string}{str(generate_random_string(4))}-0'
        
        
def generate_unigue_id(instance) -> str:
  """
  This method generates a unique id for the model
  :param instance: The model instance
  :return: str
  """
  unique_id = unique_id_generator().upper()
  Kclass = instance.__class__
  qs_exists = Kclass.objects.filter(unique_id=unique_id).exists()
  if qs_exists:
    return generate_unigue_id(instance)
  return unique_id
        
