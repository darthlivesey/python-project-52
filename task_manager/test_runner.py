from django.test.runner import DiscoverRunner
from django.db import connection


class CustomTestRunner(DiscoverRunner):
    def setup_databases(self, **kwargs):
        result = super().setup_databases(**kwargs)

        with connection.schema_editor() as schema_editor:
            for app_config in apps.get_app_configs():
                for model in app_config.get_models():
                    try:
                        schema_editor.create_model(model)
                    except Exception:
                        pass
        return result
