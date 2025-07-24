
```
ragapi_services
         └─ isympy.1
├─ Deployment
│  └─ Dockerfile
├─ Docs
│  ├─ Class_diagram.png
│  ├─ Class_diagrams.plantuml
│  ├─ sequence_diagrams.plantuml
│  └─ sequence_diagrams.png
├─ README_RAG_PDF_QA.md
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
│  │  │  ├─ PDFQAEngineRouter.py
│  │  │  ├─ WeaviateWriter.py
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
│  │  │  ├─ Embedders
│  │  │  │  ├─ BaseEmbedder.py
│  │  │  │  ├─ PDFEmbedder.py
│  │  │  │  └─ TEXTEmbedder.py
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
└─ launch.sh

```