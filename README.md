# ainventory_project

Интеллектуальная система для малого и среднего бизнеса, которая помогает прогнозировать спрос и управлять запасами с учётом сезонности, трендов и промо-акций.

## Возможности
- Прогнозирование спроса по SKU (Prophet, SARIMA, ML)
- Визуализация результатов (Streamlit)
- Рекомендации по закупкам
- Поддержка CSV, Excel, Google Sheets
- Упаковка проекта в Docker

## Технологии
Python 3.10+, pandas, Prophet, statsmodels, seaborn, plotly, scikit-learn, Streamlit, Docker

## Структура
- `notebooks/` — исследования, EDA, модели
- `app/` — веб-интерфейс на Streamlit
- `data/` — данные (не попадают в Git)
- `docker/` — Dockerfile и сборка

## Запуск (локально)
```bash
pip install -r requirements.txt
jupyter notebook
