from django.db import models
        
class Reporte(models.Model):
            
    class Meta:
        
        managed = False  # No database table creation or deletion  \
                         # operations will be performed for this model. 
                
        default_permissions = () # disable "add", "change", "delete"
                                 # and "view" default permissions

        permissions = ( 
            ("recaudacion","Ver reporte de recaudación"),  
            ("demora_por_estados","Ver reporte de demoras por estados de permiso"), 
            ("comision","Ver reporte de comisiones"), 
        )