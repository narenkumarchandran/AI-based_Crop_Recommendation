# Farmer's Friend - Project Documentation

Welcome to the development repository for "Farmer's Friend", an AI-driven agricultural assistant SaaS application.

## Overview

This project is broken down into three major architectures to support a scalable SaaS model:
1. **Python ML Microservice (`python-ml-service`)**: Contains a FastAPI wrapper over a Random Forest Crop Recommendation Model.
2. **Node.js Core Backend (`node-backend`)**: Resolves external IoT data, integrates external APIs (Weather, Agmarknet, Gemini), and manages MongoDB SaaS models.
3. **Mobile Frontend (`mobile-app`)**: A React Native (Expo) application serving the end user.

## Running Locally

### Prerequisites
- Docker & Docker Compose
- Node.js (for Expo)
- Python 3.11+ (if running the backend locally without Docker)

### Build & Run the Backend
Ensure you are in the root directory and use Docker Compose to spin up the backend:

```bash
docker-compose up --build
```
This will start:
- `mongodb` on port 27017
- `node-backend` on port 5000
- `python-ml-service` on port 8000

### Start the Frontend
First, navigate to the `mobile-app` directory. Install the dependencies for your preferred framework:

```bash
cd mobile-app
npm install 
npx expo start
```
