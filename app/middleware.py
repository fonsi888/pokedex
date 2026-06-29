from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Añade cabeceras de seguridad HTTP a todas las respuestas."""
    
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Evita que el navegador ejecute contenido en contextos incorrectos
        response.headers["X-Content-Type-Options"] = "nosniff"
        
        # Protección contra clickjacking
        response.headers["X-Frame-Options"] = "DENY"
        
        # Activa el filtro XSS del navegador
        response.headers["X-XSS-Protection"] = "1; mode=block"
        
        # Política de seguridad de contenido
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "img-src 'self' https://raw.githubusercontent.com data:; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline';"
        )
        
        # En producción fuerza HTTPS
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains"
        )
        
        return response