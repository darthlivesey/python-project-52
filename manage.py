#!/usr/bin/env python
import os
import sys
from pathlib import Path

# Путь к основному manage.py
main_manage = Path(__file__).resolve().parent / 'src' / 'manage.py'

# Запускаем основной manage.py
if main_manage.exists():
    os.execv(str(main_manage), [str(main_manage)] + sys.argv[1:])
else:
    sys.stderr.write(f"Error: Main manage.py not found at {main_manage}\n")
    sys.exit(1)