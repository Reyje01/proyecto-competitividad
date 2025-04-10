from django.db import models

# Create your models here.
class TipoUnidad(models.Model):
    idtipo_unidad = models.AutoField(primary_key=True, serialize=False)
    tipo_unidad = models.CharField(max_length=45)

    def __str__(self):
        return self.tipo_unidad
    

    class Meta:
        db_table = 'tipo_unidad'


class UnidadAnalisis(models.Model):
    idunidad_analisis = models.AutoField(primary_key=True, serialize=False)
    nombre_unidad = models.CharField(max_length=45)
    provincia = models.CharField(max_length=45)
    descripcion_unidad = models.CharField(max_length=100, blank=True, null=True)
    idtipo_unidad = models.ForeignKey(TipoUnidad, on_delete=models.CASCADE, db_column='idtipo_unidad')

    def __str__(self):
        return self.nombre_unidad
    
    @property
    def tipo_unidad_display(self):
        return self.idtipo_unidad.tipo_unidad
    
    class Meta:
        db_table = 'unidad_analisis'


class Pilar(models.Model):
    idpilar = models.AutoField(primary_key=True, serialize=False)
    nombre_pilar = models.CharField(max_length=45)
    descripcion_pilar = models.CharField(max_length=100, blank=True, null=True)
    idtipo_unidad = models.ForeignKey(TipoUnidad, on_delete=models.CASCADE, db_column='idtipo_unidad')

    def __str__(self):
        return self.nombre_pilar
    
    class Meta:
        db_table = 'pilar'


class Indicador(models.Model):
    idindicador = models.AutoField(primary_key=True, serialize=False)
    nombre_indicador = models.CharField(max_length=45)
    peso_indicador = models.IntegerField()
    tipo_indicador = models.CharField(max_length=45)
    idpilar = models.ForeignKey(Pilar, on_delete=models.CASCADE, db_column='idpilar')

    class Meta:
        db_table = 'indicador'

    def __str__(self):
        return self.nombre_indicador
    

class Registro(models.Model):
    idregistro = models.AutoField(primary_key=True, serialize=False)
    fecha_registro = models.DateField(auto_now_add = True, serialize=False)
    idindicador = models.ForeignKey(Indicador,on_delete=models.CASCADE, db_column='idindicador')
    idunidad_analisis = models.ForeignKey(UnidadAnalisis, on_delete=models.CASCADE, db_column='idunidad_analisis')

    def __str__(self):
        text = "{0} ({1})"
        return text.format(self.idregistro, self.fecha_registro)


    class Meta:
        db_table = 'registro'


class ValorCualitativo(models.Model):
    idregistro = models.OneToOneField(Registro, on_delete=models.CASCADE, db_column='idregistro', primary_key=True)
    valor_cualitativo = models.CharField(max_length=45, blank=True, null=True)

    def __str__(self):
        text = "({0}) ({1})"
        return text.format(self.idregistro, self.valor_cualitativo)

    class Meta:
        db_table = 'valor_cualitativo'


class ValorCuantitativo(models.Model):
    idregistro = models.OneToOneField(Registro, on_delete=models.CASCADE, db_column='idregistro', primary_key=True)
    valor_cuantitativo = models.FloatField()

    def __str__(self):
        text = "({0}) ({1})"
        return text.format(self.idregistro, self.valor_cuantitativo)

    class Meta:
        db_table = 'valor_cuantitativo'

class IndiceIndicador(models.Model):
    idindice_indicador = models.AutoField(primary_key=True, serialize=False)
    fecha_ii = models.DateField(auto_now_add=True, serialize=False)
    valor_ii = models.FloatField(blank=True, null=True)
    clasificacion_ii = models.CharField(max_length=45, blank=True, null=True)
    idindicador = models.ForeignKey(Indicador, on_delete=models.CASCADE, db_column='idindicador')
    idunidad_analisis = models.ForeignKey(UnidadAnalisis, on_delete=models.CASCADE, db_column='idunidad_analisis')

    def __str__(self):
        text = "{0} ({1})"
        return text.format(self.valor_ii, self.clasificacion_ii)

    class Meta:
        db_table = 'indice_indicador'


class IndicePilar(models.Model):
    idindice_pilar = models.AutoField(primary_key=True, serialize=False)
    fecha_ip = models.DateField(auto_now_add=True, serialize=False)
    valor_ip = models.FloatField(blank=True, null=True)
    clasificacion_ip = models.CharField(max_length=45, blank=True, null=True)
    idpilar = models.ForeignKey(Pilar, on_delete=models.CASCADE, db_column='idpilar')
    idunidad_analisis = models.ForeignKey(UnidadAnalisis, on_delete=models.CASCADE, db_column='idunidad_analisis')

    def __str__(self):
        text = "{0} ({1})"
        return text.format(self.valor_ip, self.clasificacion_ip)

    class Meta:
        db_table = 'indice_pilar'


class IndiceGeneral(models.Model):
    idindice_general = models.AutoField(primary_key=True, serialize=False)
    fecha_ig = models.DateField(auto_now_add=True, serialize=False)
    valor_ig = models.FloatField(blank=True, null=True)
    clasificacion_ig = models.CharField(max_length=45, blank=True, null=True)
    idunidad_analisis = models.ForeignKey(UnidadAnalisis, on_delete=models.CASCADE, db_column='idunidad_analisis')

    def __str__(self):
        text = "{0} ({1})"
        return text.format(self.valor_ig, self.clasificacion_ig)

    class Meta:
        db_table = 'indice_general'
