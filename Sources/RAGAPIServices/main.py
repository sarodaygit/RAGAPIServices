from fastapi import FastAPI
from Utils.ConfigParserUtil import ConfigParserUtil
from Utils.LoggerUtil import LoggerUtil
from Routers.WeaviateWriter import WeaviateWriter
from Routers.PDFQAEngineRouter import PDFQARouter
from Handlers.Middlewares import TimeTrackerMiddleware
from Handlers.OpenTelemetryServices import OpenTelemetryServices
# from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# Initialize configuration and logger
config = ConfigParserUtil()
logger = LoggerUtil()

# Create FastAPI app instance
app = FastAPI()

# Optional: Initialize OpenTelemetry tracing (currently disabled)
opentelemetry_setup = OpenTelemetryServices()
opentelemetry_setup.initialize_opentelemetry()
# FastAPIInstrumentor.instrument_app(app)

# Add custom middleware
app.add_middleware(TimeTrackerMiddleware)

# Global API prefix (e.g., "/api/v1")
global_prefix = config.getValue("General", "prefix_url")

# Register routers

# movie_router = MovieStatsRouter(prefix="/movies").router
pdf_router = WeaviateWriter(prefix="/pdrwriter").router
PDFqa_router = PDFQARouter(prefix="/pdfqa").router


# Register endpoints
@app.get("/test")
def read_root():
    logger.log_info("Hello Worldxxxxxxxxxxxx")
    return {"message": "Hello World"}

# Include routers in the FastAPI app

# app.include_router(movie_router)
app.include_router(pdf_router)
app.include_router(PDFqa_router)

# To run:
# cd ~/git/RAGAPIServices/Sources/RAGAPIServices
# uvicorn main:app --host 0.0.0.0 --port 8000 --reload
