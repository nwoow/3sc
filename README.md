# Transaction Processing System

This project is a complete data pipeline demo built using:

- **Kafka** for message queuing
- **PostgreSQL** for data storage
- **Python Producer** to generate random transaction data
- **Python Consumer** to process and store data from Kafka to PostgreSQL
- **FastAPI Backend** to expose APIs for querying the transaction data
- **React Frontend** (with Material UI Data Grid) to display transaction data with filtering and pagination

---

## 📦 Project Architecture


---

## 🔧 Setup Instructions

### 1. Clone the repository

```bash
git clone git@github-nilayy:nwoow/3sc.git
cd 3sc

🐳 Build and Run All Services with Docker

    docker-compose build
    docker-compose up -d

🔄 Restart the Backend After Boot
    
    docker-compose restart backend

🧾 Available Services

    Service	Port	Description
    Kafka	9092	Kafka broker for message queue
    PostgreSQL	5432	Stores transaction data
    Backend	8000	FastAPI backend exposing REST API
    Frontend	3000	React frontend (Material UI)

🛠 Logs for Debugging

    docker-compose logs -f producer
    docker-compose logs -f consumer
    docker-compose logs -f backend
    docker-compose logs -f frontend


📂 Folder Structure

    3sc/
    ├── backend/        # FastAPI backend
    ├── producer/       # Kafka producer (Python)
    ├── consumer/       # Kafka consumer (Python)
    ├── frontend/       # React frontend (Material UI DataGrid)
    ├── docker-compose.yml
    └── README.md


✨ Features

Generates 1000+ random transactions per minute

Real-time processing with Kafka

Persistent storage in PostgreSQL

REST API with filtering and pagination

Material UI DataGrid in the frontend for search and display

