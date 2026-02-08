from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api import tasks
from src.api.v1 import auth  # Keep auth at v1 for now
from src.config.settings import get_settings
from src.auth.middleware import AuthMiddleware
from src.middleware.error_handler import add_error_handling_middleware

# Initialize FastAPI app
app = FastAPI(
    title="Secure Todo API Backend",
    description="RESTful API for task management with JWT authentication",
    version="1.0.0"
)

# Add error handling middleware first (top of the stack)
add_error_handling_middleware(app)

# Add authentication middleware first (before CORS)
app.add_middleware(AuthMiddleware)

# Get settings
settings = get_settings()

# Configure CORS middleware - allow frontend at port 3001
allow_origins = settings.allowed_origins
if settings.frontend_url:
    if settings.frontend_url not in allow_origins:
        allow_origins.append(settings.frontend_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-Requested-With"],
)

# Include API routes - updated to new structure
app.include_router(tasks.router, prefix="/api", tags=["tasks"])
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])

@app.get("/")
def read_root():
    return {"message": "Secure Todo API Backend"}

@app.get("/health")
async def health_check():
    # In a real application, you might want to check database connectivity, etc.
    return {"status": "healthy", "service": "todo-api", "version": "1.0.0"}