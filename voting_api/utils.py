import random
import string

def create_unique_id(prefix, model, field_name):
    
     while True:
            unique_id = f"{prefix}-{random.randint(1000, 9999)}"
            if not model.objects.filter(**{field_name: unique_id}).exists():
               return unique_id
            