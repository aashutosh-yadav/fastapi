from pydantic_settings  import BaseSettings


class Settings(BaseSettings):
    database_hostname: str = "localhost"      # optional in .env
    database_port: str = "5432"               # optional in .env
    database_password: str                    # required in .env
    database_name: str                        # required in .env
    database_username: str = "postgres"       # optional in .env
    secret_key: str                           # required in .env
    algorithm: str = "HS256"                  # optional in .env
    access_token_expire_minutes: int = 30     # optional in .env

    class Config:
        env_file = ".env"


settings = Settings()
