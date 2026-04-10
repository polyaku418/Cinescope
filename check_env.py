# cd C:\Users\User\PycharmProjects\Practics_Projects
# python check_env.py
import os
import sys
from pathlib import Path

# Добавляем путь к проекту
sys.path.insert(0, str(Path(__file__).parent))

print("=" * 50)
print("ПРОВЕРКА .env ФАЙЛА")
print("=" * 50)

# Проверяем текущую директорию
current_dir = Path.cwd()
print(f"\nТекущая директория: {current_dir}")

# Ищем .env
env_file = current_dir / '.env'
print(f"\nИщем .env: {env_file}")
print(f"Файл существует: {env_file.exists()}")

if env_file.exists():
    print("\n✅ .env файл найден!")
    print("\nСодержимое .env:")
    print("-" * 30)
    with open(env_file, 'r', encoding='utf-8') as f:
        content = f.read()
        print(content)
    print("-" * 30)

    # Парсим содержимое
    lines = content.strip().split('\n')
    for line in lines:
        if '=' in line and not line.startswith('#'):
            key, value = line.split('=', 1)
            if key == 'SUPER_ADMIN_EMAIL':
                print(f"\n📧 {key} = {value}")
            elif key == 'SUPER_ADMIN_PASSWORD':
                print(f"🔑 {key} = {'*' * len(value)}")
else:
    print("\n❌ .env файл НЕ НАЙДЕН!")
    print(f"\nСоздайте файл: {current_dir / '.env'}")
    print("Со следующим содержимым:")
    print("SUPER_ADMIN_EMAIL=api1@gmail.com")
    print("SUPER_ADMIN_PASSWORD=asdqwe123Q")

print("\n" + "=" * 50)

# Проверяем загрузку через dotenv
if env_file.exists():
    try:
        from dotenv import load_dotenv

        load_dotenv(dotenv_path=env_file)

        email = os.getenv('SUPER_ADMIN_EMAIL')
        password = os.getenv('SUPER_ADMIN_PASSWORD')

        print(f"\nЧерез os.getenv():")
        print(f"SUPER_ADMIN_EMAIL = {email}")
        print(f"SUPER_ADMIN_PASSWORD = {'*' * len(password) if password else 'None'}")

        if email and password:
            print("\n✅ УСПЕХ! Переменные загружены корректно!")
        else:
            print("\n❌ ОШИБКА! Переменные не загрузились!")
    except ImportError:
        print("\n⚠️ python-dotenv не установлен!")
        print("Установите: pip install python-dotenv")