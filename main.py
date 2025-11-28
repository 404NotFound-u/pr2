import csv
import sys
import os

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

def main():
    config = load_config()
    print('Конфигурация:')
    for key, value in config.items():
        print(f'{key}={value}')

if __name__ == '__main__':
    main()
