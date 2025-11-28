import csv
import sys
import os
import urllib.request
import json

def load_config(config_file='config.csv'):
    if not os.path.exists(config_file):
        print(f'Ошибка: файл конфигурации \"{config_file}\" не найден.', file=sys.stderr)
        sys.exit(1)

    with open(config_file, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        if not rows:
            print('Ошибка: конфигурационный файл пуст.', file=sys.stderr)
            sys.exit(1)

        config = rows[0]
        required_keys = ['package_name', 'repo_url_or_test_path', 'test_mode', 'filter_substring']
        for key in required_keys:
            if key not in config:
                print(f'Ошибка: отсутствует обязательный параметр \"{key}\" в CSV.', file=sys.stderr)
                sys.exit(1)

        config['test_mode'] = config['test_mode'].strip().lower() in ('true', '1', 'yes', 'on')
        return config

def get_latest_version(package_name):
    url = f'https://crates.io/api/v1/crates/{package_name}'
    try:
        with urllib.request.urlopen(url) as resp:
            data = json.load(resp)
            return data['crate']['max_version']
    except Exception as e:
        print(f'Ошибка получения версии пакета {package_name}: {e}', file=sys.stderr)
        sys.exit(1)

def fetch_dependencies(package_name, version):
    url = f'https://crates.io/api/v1/crates/{package_name}/{version}/dependencies'
    try:
        with urllib.request.urlopen(url) as resp:
            data = json.load(resp)
            deps = [d['crate_id'] for d in data['dependencies']]
            return deps
    except Exception as e:
        print(f'Ошибка получения зависимостей: {e}', file=sys.stderr)
        sys.exit(1)

def main():
    config = load_config()
    print('Конфигурация:')
    for key, value in config.items():
        print(f'{key}={value}')

    if config['test_mode']:
        print('Тестовый режим: этап 2 пропущен.')
        return

    package = config['package_name']
    print(f'\n[Stage 2] Получение прямых зависимостей для пакета: {package}')

    version = get_latest_version(package)
    print(f'Последняя версия: {version}')

    deps = fetch_dependencies(package, version)
    print(f'\nПрямые зависимости ({len(deps)} шт.):')
    for d in sorted(deps):
        print(f'- {d}')

if __name__ == '__main__':
    main()
