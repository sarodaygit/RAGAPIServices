# RAGAPIServices

A FastAPI-based microservice for handling REST API requests, integrating with MongoDB, SQL Server, and supporting OpenTelemetry tracing.

## Features

✅ FastAPI server with modular router architecture

✅ MongoDB integration using async Motor client

🚧 SQL Server integration (planned)

⚙️ Middleware for request logging and execution time

🧠 Centralized config with dynamic environment support

📊 Structured logging utility

🔍 OpenTelemetry tracing with Jaeger support

🐳 Docker and Docker Compose support

## Project Structure

```
.
├── Deployment/           # Dockerfile and deployment scripts
├── Docs/                 # UML diagrams and documentation
├── Sources/              # Main source code
│   ├── RAGAPIServices/
│   │   ├── Conf/         # Configuration files
│   │   ├── Handlers/     # Middleware, error handling, telemetry
│   │   ├── Routers/      # API routers
│   │   ├── Stores/       # Database access (Mongo, SQLServer)
│   │   ├── Utils/        # Utilities (logging, config, JSON encoder)
│   │   └── main.py       # FastAPI app entry point
├── Tests/                # Unit and integration tests
├── cleancache.sh         # Script to clean Python cache files
├── launch.sh             # Script to build and run Docker container
└── README.md             # This file
```


⚙️ Getting Started
✅ Prerequisites
Python 3.8+

Docker & Docker Compose

MongoDB instance (local or TLS-enabled)


🛠️ Setup Instructions

Make sure Mongodb server is available for the testing. 
Clone the git repo and follow the instructions if you don't have mongodb
    repo - git@github.com:sarodaygit/docker_mongodb.git

1️⃣ Clone and Install

    git clone https://github.com/sarodaygit/RAGAPIServices.git
        cd RAGAPIServices
        cd Sources
        pip install -r requirements.txt

2️⃣ TLS Certificate Setup (Optional)

    If using MongoDB with SSL (UseSSL=true in config):
        mkdir -p Sources/RAGAPIServices/certs

    Sources/RAGAPIServices/certs/
    ├── ca.pem         # Root certificate
    └── mongodb.pem    # Mongo server certificate + private key (combined)

    Note : > These files should be excluded from version control. Use `.gitignore`.
```

3️⃣ Running Locally (Without Docker)
    Use .vscode/launch.json profiles:
        Dev Mode: Dev Python: FastAPI
        Prod Mode: Prod Python: FastAPI

        "env": {
                "ENV": "prod",
                "MONGO_CERT_PATH": "./Sources/RAGAPIServices/certs/ca.pem"
                }

4️⃣ Running in Docker
    Use the helper script:
    # Launch Docker containers
    ./launch.sh start dev         # or prod
    ./launch.sh status prod       # View container status
    ./launch.sh restart dev       # Restart
    ./launch.sh shutdown all      # Stop and clean



📦 API Endpoints
    Endpoint	Description
    /test	Health check
    /movies/count	Get total movie count
    /movies/latest	Get the most recent movie
    /movies/highrated	Get IMDb rating > 9.0 movies
    ## API Endpoints

📌 Configuration
    All config files reside in:
    Sources/RAGAPIServices/Conf/
        ├── RAGAPIServices.dev.conf
        └── RAGAPIServices.prod.conf

🧪 Running Tests
    cd Tests
    pytest

## License


```
RAGAPIServices
├─ Deployment
│  └─ Dockerfile
├─ Docs
├─ README.md
├─ Sources
│  ├─ RAGAPIServices
│  │  ├─ Conf
│  │  ├─ Handlers
│  │  ├─ Routers
│  │  ├─ Stores
│  │  │  ├─ Mongo
│  │  │  │  ├─ Models
│  │  │  │  ├─ motorstore.py
│  │  │  │  └─ store.py
│  │  │  ├─ SQLServer
│  │  │  │  ├─ Models
│  │  │  │  └─ store.py
│  │  ├─ Utils
│  │  └─ main.py
│  └─ requirements.txt
├─ Tests
│  └─ test_TestPlanner.py
├─ docker-compose.dev.yml
├─ docker-compose.prod.yml
├─ launch.sh

```
```
ragapi_services
├─ Deployment
│  └─ Dockerfile
├─ Docs
│  ├─ Class_diagram.png
│  ├─ Class_diagrams.plantuml
│  ├─ sequence_diagrams.plantuml
│  └─ sequence_diagrams.png
├─ README.md
├─ Sources
│  ├─ .pylintrc
│  ├─ RAGAPIServices
│  │  ├─ Conf
│  │  │  ├─ FastApiServices.dev copy.conf
│  │  │  ├─ FastApiServices.prod copy.conf
│  │  │  ├─ FastApiServices.prod.conf
│  │  │  ├─ RAGAPIServices.dev.conf
│  │  │  └─ __init__.py
│  │  ├─ Handlers
│  │  │  ├─ ErrorCodes.py
│  │  │  ├─ Middlewares.py
│  │  │  ├─ OpenTelemetryServices.py
│  │  │  ├─ RagapiServicesException.py
│  │  │  └─ __init__.py
│  │  ├─ RAGAPIServices.log
│  │  ├─ Routers
│  │  │  ├─ MovieStatsRouter.py
│  │  │  └─ __init__.py
│  │  ├─ Stores
│  │  │  ├─ Mongo
│  │  │  │  ├─ Models
│  │  │  │  │  ├─ MoviStats.py
│  │  │  │  │  ├─ __init__.py
│  │  │  │  │  └─ user.py
│  │  │  │  ├─ __init__.py
│  │  │  │  ├─ motorstore.py
│  │  │  │  └─ store.py
│  │  │  ├─ SQLServer
│  │  │  │  ├─ Models
│  │  │  │  │  └─ __init__.py
│  │  │  │  ├─ __init__.py
│  │  │  │  └─ store.py
│  │  │  ├─ Weaviate
│  │  │  │  ├─ __init__.py
│  │  │  │  └─ store.py
│  │  │  └─ __init__.py
│  │  ├─ Utils
│  │  │  ├─ ConfigParserUtil.py
│  │  │  ├─ JSONEncoder.py
│  │  │  ├─ LoggerUtil.py
│  │  │  └─ __init__.py
│  │  ├─ __init__.py
│  │  └─ main.py
│  ├─ __init__.py
│  └─ requirements.txt
├─ Tests
│  ├─ __init__.py
│  └─ test_TestPlanner.py
├─ cleancache.sh
├─ docker-compose.dev.yml
├─ docker-compose.prod.yml
├─ launch.sh
└─ notes.txt

```# RAGAPIServices
