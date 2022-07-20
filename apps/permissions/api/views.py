from unicodedata import decimal

from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated

from apps.core.models import *
from apps.permissions.api.serializers import *
from rest_framework.response import Response
from django.db.models import Q
from apps.core.constants import *

class PermissionCreateView(generics.CreateAPIView):
    queryset = Permiso.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = (IsAuthenticated,)
    def create(self, request, *args, **kwargs):
        obj = Permiso()
        obj.estado = 'ACT'
        obj.actividades_id = request.data['actividades']
        obj.tiposussuarios_id = request.data['tiposussuarios']
        obj.visualizar = request.data['visualizar']
        obj.editar = request.data['editar']
        obj.importar = request.data['importar']
        obj.exportar = request.data['exportar']

        obj.save()
        result = result_success_object(obj, self)
        return Response(result)

class PermissionUpdateView(generics.UpdateAPIView):
    queryset = Permiso.objects.all()
    serializer_class = PermissionSerializer
    lookup_field = "id"
    permission_classes = (IsAuthenticated,)
    def update(self, request, *args, **kwargs):
        _id = self.kwargs['id']
        obj = Permiso.objects.get(Q(id=_id))
        obj.estado = 'ACT'
        obj.actividades_id = request.data['actividades']
        obj.tiposussuarios_id = request.data['tiposussuarios']
        obj.visualizar = request.data['visualizar']
        obj.editar = request.data['editar']
        obj.importar = request.data['importar']
        obj.exportar = request.data['exportar']

        obj.save()
        result = result_success_object(obj, self)
        return Response(result)

class PermissionListView(generics.ListAPIView):
    queryset = Permiso.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = (IsAuthenticated,)
    def list(self, request, *args, **kwargs):
        value = Permiso.objects.filter(Q(estado="ACT"))
        result = result_success_list(value, self)
        return Response(result)

class PermissionActivityListView(generics.ListAPIView):
    queryset = Actividad.objects.all()
    serializer_class = PermisionActivityFatherSerializer
    permission_classes = (IsAuthenticated,)
    def list(self, request, *args, **kwargs):
        _id_tipousuario = self.kwargs['idtipousuario']
        actividades = Actividad.objects.filter(Q(estado="ACT") & Q(actividad_padre_id=None)).order_by('orden').all()
        objectos = []
        for item in actividades:
            detalles_permissions_activities_sons = []
            for item_actividad_hijo in Actividad.objects.filter(Q(estado="ACT") & Q(actividad_padre_id=item.id)& ~Q(actividad_padre_id=None)):
                permiso_hijo = Permiso.objects.filter(Q(actividades_id=item_actividad_hijo.id) & Q(tiposussuarios__id=_id_tipousuario) & Q(estado='ACT')).order_by('id').first()
                if permiso_hijo is not None:
                    detalle_permission_activitie_son = {
                        'actividades': item_actividad_hijo.id,
                        'actividades_nombre': item_actividad_hijo.nombre,
                        'controlador': item_actividad_hijo.controlador,
                        'accion': item_actividad_hijo.accion,
                        'tiposussuarios': permiso_hijo.tiposussuarios.id,
                        'tiposussuarios_nombre': permiso_hijo.tiposussuarios.nombre,
                        'visualizar': permiso_hijo.visualizar,
                        'editar': permiso_hijo.editar,
                        'importar': permiso_hijo.importar,
                        'exportar': permiso_hijo.exportar,
                        'estado': item_actividad_hijo.estado
                    }
                    detalles_permissions_activities_sons.append(detalle_permission_activitie_son)

            permiso = Permiso.objects.filter(Q(actividades_id=item.id) & Q(tiposussuarios__id=_id_tipousuario) & Q(estado='ACT')).order_by('id').first()
            if permiso is not None:
                objeto = {
                    'actividades': item.id,
                    'actividades_nombre': item.nombre,
                    'icono': item.icono,
                    'visualizar': permiso.visualizar,
                    'tiposussuarios': permiso.tiposussuarios.id,
                    'tiposussuarios_nombre': permiso.tiposussuarios.nombre,
                    'detalles_permissions_activities_sons': detalles_permissions_activities_sons,
                    'estado': item.estado,
                }
                objectos.append(objeto)

        serializer = PermisionActivityFatherSerializer(objectos, many=True)
        result = {
            'data': serializer.data,
            'error': False,
            'message': 'Success',
            'code': 200
        }
        return Response(result)

class PermissionActivityDetailView(generics.ListAPIView):
    queryset = Permiso.objects.all()
    serializer_class = PermisionActivitySonSerializer
    permission_classes = (IsAuthenticated,)
    def list(self, request, *args, **kwargs):
        _id_actividad = self.kwargs['idactividad']
        _id_tipousuario = self.kwargs['idtipousuario']
        if Actividad.objects.filter(Q(estado="ACT") & Q(id=_id_actividad)).exists():
            actividades = Actividad.objects.get(Q(estado="ACT") & Q(id=_id_actividad))
            permiso_hijo = Permiso.objects.get(Q(actividades_id=actividades.id) & Q(tiposussuarios__id=_id_tipousuario) & Q(estado='ACT'))
            detalle_permission_activitie_son = {
                'actividades': actividades.id,
                'actividades_nombre': actividades.nombre,
                'controlador': actividades.controlador,
                'accion': actividades.accion,
                'tiposussuarios': permiso_hijo.tiposussuarios.id,
                'tiposussuarios_nombre': permiso_hijo.tiposussuarios.nombre,
                'visualizar': permiso_hijo.visualizar,
                'editar': permiso_hijo.editar,
                'importar': permiso_hijo.importar,
                'exportar': permiso_hijo.exportar,
                'estado': actividades.estado
            }
        else:
            result = {
                'data': None,
                'error': True,
                'message': 'Error: permiso no encontrado',
                'code': 404
            }
            return Response(result)

        serializer = PermisionActivitySonSerializer(detalle_permission_activitie_son)
        result = {
            'data': serializer.data,
            'error': False,
            'message': 'Success',
            'code': 200
        }
        return Response(result)

class PermissionDetailView(generics.RetrieveAPIView):
    queryset = Permiso.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = (IsAuthenticated,)
    def retrieve(self, request, *args, **kwargs):
        _id = self.kwargs['id']
        value = Permiso.objects.get(Q(id=_id))
        result = result_success_object(value, self)
        return Response(result)

class PermissionDeleteView(generics.DestroyAPIView):
    queryset = Permiso.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = (IsAuthenticated,)
    def delete(self, request, *args, **kwargs):
        _id = self.kwargs['id']
        obj = Permiso.objects.get(Q(id=_id))
        obj.estado = "INA"
        obj.save()
        result = result_success_object(obj, self)
        return Response(result)