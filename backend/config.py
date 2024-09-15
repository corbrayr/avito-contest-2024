from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    SERVER_ADDRESS: str
    POSTGRES_CONN: str
    POSTGRES_JDBC_URL: str
    POSTGRES_USERNAME: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DATABASE: str
    
    @property
    def database_url(self):
        user = f"{self.POSTGRES_USERNAME}:{self.POSTGRES_PASSWORD}"
        database = f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DATABASE}"
        return f"postgresql+asyncpg://{user}@{database}"
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    
settings = Settings()