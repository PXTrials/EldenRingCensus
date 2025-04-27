

from django.db import migrations, models

def create_outcomes(apps, schema_editor):
    Outcome = apps.get_model('census', 'Outcome')
    Role = apps.get_model('census', 'Role')
    db_alias = schema_editor.connection.alias
    outcomes = [
        ['Host Cleared Objective', 'gold', True, False],
        ['Host Died', 'gold', False, True],
        ['I Died', 'gold', False, True],
        ['Invader Defeated', 'blue', True, False],
        ['Host Cleared Objective', 'blue', True, False],
        ['Host Died', 'blue', False, True],
        ['I Died', 'blue', False, True],
        ['Host Killed', 'red', True, False],
        ['Disconnect (Evasion)', 'red', True, False],
        ['Fogwall (Evasion)', 'red', True, False],
        ['Disconnect (No Encounter)', 'red', False, False],
        ['Fogwall (No Encounter)', 'red', False, False],
        ['I Died', 'red', False, True]
        ]
    for idx, outcome in enumerate(outcomes):
        description, role, is_win, is_loss = outcome
        Outcome.objects.using(db_alias).create(
                    description = description,
                    role = Role.objects.using(db_alias).get(name=role),
                    is_win = is_win,
                    is_loss = is_loss,
                    sort_order = idx
                )

def delete_outcomes(apps, schema_editor):
    Outcome = apps.get_model('census', 'Outcome')
    db_alias = schema_editor.connection.alias
    Outcome.objects.using(db_alias).all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('census', '0005_seed_locations'),
    ]

    operations = [
        migrations.AddField(
            model_name='outcome',
            name='sort_order',
            field=models.PositiveSmallIntegerField(default=10),
        ),
        migrations.RunPython(create_outcomes, delete_outcomes)
    ]
