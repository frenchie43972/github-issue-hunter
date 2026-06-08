"""
FastAPI application entry point.

This module creates the backend API application. 
"""
from fastapi import FastAPI, HTTPException

from app.database import check_database_connection
from app.routers.issues import router as issues_router

app = FastAPI(
  title='GitHub Issue Hunter API',
  version='0.1.0',
)

app.include_router(issues_router)

@app.get('/health')
def health_check() -> dict[str, str]:
  return {'status': 'ok'}

@app.get('/health/db')
def database_health_check() -> dict[str, str]:
  try:
    is_connected = check_database_connection()
  except Exception as error:
    raise HTTPException(
      status_code=503,
      detail=f'Database connection failed: {error}',
    ) from error
    
  if not is_connected:
    raise HTTPException(
      status_code=503,
      detail='Database connection check failed',
    )
    
  return {'status': 'ok', 'database': 'connected'}