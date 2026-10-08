from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_hostname: str
    database_name: str
    database_port: str
    database_username: str
    database_password: str = ''
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    test_database_hostname: str
    test_database_name: str
    test_database_port: str
    test_database_username: str
    test_database_password: str = ''

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )
    
settings = Settings() # type: ignore