import uuid
from django.utils import timezone
from django.db import models

class Pessoa(models.Model):
    name = models.CharField(max_length=100, null=True)
    photo = models.ImageField(upload_to='fotos/', null=True)

    def __str__(self):
        return self.name 

class EstacaoTrabalho(models.Model):
    name = models.CharField(max_length=100, null=True)
    mac_address = models.CharField(max_length=17, unique=True, null=True)

    def __str__(self):
        return self.name 
    
    @staticmethod
    def obter_mac_address():
        mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0,2*6,2)][::-1])
        return mac_address


class RegistroAcesso(models.Model):
    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE, null=True)
    estacao_trabalho = models.ForeignKey(EstacaoTrabalho, on_delete=models.CASCADE, related_name='registros_acesso', null=True)
    data_hora_acesso = models.DateTimeField(default=timezone.now, null=True)
    mac_address = models.CharField(max_length=17, null=True, blank=True)

    @staticmethod
    def obter_mac_address():
        mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0,2*6,2)][::-1])
        return mac_address

    def save(self, *args, **kwargs):
        if not self.mac_address:
            self.mac_address = self.obter_mac_address()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.pessoa.name} acessou {self.estacao_trabalho.name} em {self.data_hora_acesso}"