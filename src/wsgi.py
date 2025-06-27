import os
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings')
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()