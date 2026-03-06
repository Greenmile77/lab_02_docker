# Лабораторная работа №2: Docker-контейнеризация
## Вариант 4: Финансы - Портфель Марковица

### 📋 Описание проекта
Микросервисное приложение для анализа финансового портфеля по модели Марковица с генерацией PDF-отчетов.

### 🏗 Архитектура
- **db**: PostgreSQL для хранения финансовых данных
- **loader**: ETL-контейнер для загрузки данных из CSV
- **analytics_app**: Генератор PDF-отчетов

### 📁 Структура проекта
.
├── .env                    # Переменные окружения
├── .dockerignore           # Исключения для Docker
├── docker-compose.yml      # Оркестрация сервисов
├── Dockerfile              # Для analytics_app
├── Dockerfile.loader       # Для loader
├── requirements.txt        # Зависимости Python
├── README.md               # Документация
├── data/
│   └── financial_data.csv  # Исходные данные
├── scripts/
│   ├── entrypoint.sh       # Точка входа с netcat
│   ├── loader.py           # Загрузчик данных
│   └── markowitz_report.py # Генератор отчетов
├── reports/                # PDF отчеты
└── screenshots/            # Скриншоты для отчета
### 🚀 Запуск проекта
```bash
# Клонировать репозиторий
git clone <url-репозитория>
cd lab_02

# Создать .env файл
cat > .env << EOF
POSTGRES_DB=portfolio_db
POSTGRES_USER=portfolio_user
POSTGRES_PASSWORD=secure_password_123
POSTGRES_HOST=db
POSTGRES_PORT=5432
EOF

# Запустить
docker-compose up -d

# Проверить статус
docker-compose ps

# Посмотреть логи
docker-compose logs -f analytics_app

