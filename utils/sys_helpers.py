import sys
import io

def fix_sys_streams():
    """
    Перенаправляє stdout та stderr у пам'ять, якщо консоль відсутня
    (необхідно для коректної роботи PyInstaller з прапорцем --noconsole).
    """
    if sys.stdout is None:
        sys.stdout = io.StringIO()
    if sys.stderr is None:
        sys.stderr = io.StringIO()