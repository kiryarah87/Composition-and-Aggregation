# Система управления онлайн-магазином

Проект демонстрирует применение принципов ООП (композиция, агрегация, полиморфизм, инкапсуляция) и SOLID на примере системы управления онлайн-магазином.

## Цель проекта

Разобраться с основными концепциями ООП и понять разницу между композицией и агрегацией на практическом примере.

## Основные компоненты

### Базовые классы

- **Product** - товар с атрибутами (id, name, price, category)
- **Customer** - покупатель с профилем и историей заказов
- **Order** - заказ, связывающий товары и покупателя
- **ShoppingCart** - корзина покупок
- **PaymentProcessor** - обработчик платежей (Strategy pattern)

## Запуск проекта

### Предварительные требования

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) - современный менеджер пакетов Python

### Установка uv

```bash
# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Или через pip
pip install uv
```

### Установка зависимостей и запуск

```bash
# Клонирование репозитория
git clone git@github.com:kiryarah87/Composition-and-Aggregation.git
cd Composition-and-Aggregation

# Установка зависимостей
uv sync

# Запуск проекта
uv run python main.py
```

### Работа с виртуальным окружением

```bash
# Активация виртуального окружения
source .venv/bin/activate

# Запуск без префикса uv run
python main.py
```

## Тестирование

Проект включает **195 комплексных тестов** с полным покрытием функционала.

### Быстрый старт тестирования

```bash
# Запуск всех тестов
uv run -m pytest tests/ -v

# С отчетом о покрытии
uv run -m pytest tests/ --cov=src --cov-report=html
```

### Категории тестов

- **Модульные тесты** (165): изолированное тестирование компонентов
  - Модели (Product, Customer, Order, Cart, Discount, Payment, Delivery)
  - Репозитории (ProductRepository, CustomerRepository, OrderRepository)
  - Сервисы (ProductService, CartService)
  - Схемы (DTO и конвертация)

- **Интеграционные тесты** (9): полный жизненный цикл заказа
  ```bash
  uv run -m pytest tests/test_integration.py -v
  ```

### Что протестировано

**Принципы ООП:**
- Инкапсуляция (приватные поля, валидация)
- Наследование и полиморфизм (абстрактные классы Payment, Delivery, Discount)
- Композиция и агрегация (Order содержит Customer, Items, Payment)

**SOLID принципы:**
- **SRP**: Одна ответственность у каждого класса
- **OCP**: Расширяемость через наследование
- **LSP**: Взаимозаменяемость реализаций
- **ISP**: Разделение интерфейсов
- **DIP**: Зависимость от абстракций

**Функциональность:**
- CRUD операции для всех сущностей
- Бизнес-логика (скидки, доставка, расчеты)
- Валидация входных данных
- Обработка ошибок и исключений

### Дополнительные команды

```bash
# Тесты конкретной категории
uv run -m pytest tests/test_models_*.py -v        # Только модели
uv run -m pytest tests/test_repositories_*.py -v  # Только репозитории
uv run -m pytest tests/test_services_*.py -v      # Только сервисы

# Конкретный файл или тест
uv run -m pytest tests/test_models_product.py -v
uv run -m pytest tests/test_models_product.py::TestProduct::test_product_creation -v
```

**Результаты:** Все 195 тестов пройдены успешно за ~0.09 секунд
