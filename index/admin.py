from django.contrib import admin
from .models import Device, BindDevice, DeviceData


# Register your models here.
@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('unique_id', 'name', 'is_bind')
    search_fields = ('unique_id', 'name')
    list_filter = ('is_bind',)


@admin.register(BindDevice)
class BindDeviceAdmin(admin.ModelAdmin):
    list_display = ('user', 'device', 'bind_time')
    search_fields = ('user__username', 'device__name')
    list_filter = ('bind_time',)


@admin.register(DeviceData)
class DeviceDataAdmin(admin.ModelAdmin):
    list_display = ('device', 'timestamp', 'heart_rate', 'blood_oxygen', 'temperature', 'blood_pressure')
    search_fields = ('device__name',)
    list_filter = ('timestamp',)
