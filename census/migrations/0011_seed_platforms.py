

from django.db import migrations, models

def create_platforms(apps, schema_editor):
    Platform = apps.get_model('census', 'Platform')
    db_alias = schema_editor.connection.alias
    for platform_name in ['PSN','XBOX','PC Vanilla', 'PC Seamless']:
        Platform.objects.using(db_alias).create(name=platform_name)

def delete_platforms(apps, schema_editor):
    platform = apps.get_model('census', 'platform')
    db_alias = schema_editor.connection.alias
    platform.objects.using(db_alias).all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('census', '0010_character_player'),
    ]

    operations = [
        migrations.RunPython(create_platforms, delete_platforms)
    ]
