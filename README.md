# Notas Docker

**Disciplina:** Sistemas Operacionais  
**Aluna:** Taylane Castelo Branco Cavalcante
**Data:** 17/09/2026

API de anotações desenvolvida em Python com Flask e SQLite.

## Rotas

- GET /health
- POST /notas
- GET /notas

## Execução

A aplicação utiliza a variável de ambiente DATA_DIR para definir o local onde o banco de dados será armazenado. No Docker, os dados são persistidos através do volume nomeado notas-dados. Foi utilizado um ambiente virtual .venv para a realização da
