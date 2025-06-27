# Feed Personalizer

This project is a FastAPI-based machine learning app that ranks posts based on user preferences.

## Features
- FastAPI REST API
- RandomForest model for relevance scoring
- Dockerized deployment
- Unit tested with pytest

## How to Run (Docker)

```bash
docker build -t feed-personalizer .
docker run -p 8000:8000 feed-personalizer
