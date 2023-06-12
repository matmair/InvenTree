import os
from django.db import migrations, models


def attach_file(instance, filename):  # pragma: no cover
    """
    Generate a filename for the uploaded attachment.

    2021-11-17 - This was moved here from part.models.py,
    as the function itself is no longer used,
    but is still required for migration
    """

    # Construct a path to store a file attachment
    return os.path.join('part_files', str(instance.part.id), filename)


class RemoveFieldOrSkip(migrations.RemoveField):
    """Custom RemoveField operation which will fail gracefully if the field does not exist

    Ref: https://stackoverflow.com/questions/58518726/how-to-ignore-a-specific-migration
    """

    def database_backwards(self, app_label, schema_editor, from_state, to_state) -> None:
        # Backwards migration should not do anything
        pass

    def database_forwards(self, app_label, schema_editor, from_state, to_state) -> None:
        """Forwards migration *attempts* to remove existing fields, but will fail gracefully if they do not exist"""

        try:
            super().database_forwards(app_label, schema_editor, from_state, to_state)
            print(f'Removed field {self.name} from model {self.model_name}')
        except Exception as exc:
            pass

    def state_forwards(self, app_label, state) -> None:
        try:
            super().state_forwards(app_label, state)
        except Exception:
            pass

class AddFieldOrSkip(migrations.AddField):
    """Custom AddField operation which will fail gracefully if the field already exists

    Ref: https://stackoverflow.com/questions/58518726/how-to-ignore-a-specific-migration
    """

    def database_backwards(self, app_label, schema_editor, from_state, to_state) -> None:
        # Backwards migration should not do anything
        pass

    def database_forwards(self, app_label, schema_editor, from_state, to_state) -> None:
        """Forwards migration *attempts* to remove existing fields, but will fail gracefully if they do not exist"""

        try:
            super().database_forwards(app_label, schema_editor, from_state, to_state)
            print(f'Added field {self.name} to model {self.model_name}')
        except Exception as exc:
            pass

    def state_forwards(self, app_label, state) -> None:
        try:
            super().state_forwards(app_label, state)
        except Exception:
            pass
