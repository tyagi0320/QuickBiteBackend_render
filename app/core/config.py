from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES:int 
    REFRESH_TOKEN_EXPIRE_DAYS: int
    REFRESH_SECRET_KEY: str 

    SMTP_SERVER: str
    SMTP_PORT: int
    EMAIL_ADDRESS: str      
    EMAIL_PASSWORD: str
    FRONTEND_URL: str
    
    class Config:
        env_file=".env"

settings=Settings()