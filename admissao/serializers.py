from rest_framework import serializers

from .models import Base, Departamento, Turno


class DepartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamento
        fields = '__all__'

class BaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Base
        fields = '__all__'

class TurnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turno
        fields = '__all__'
