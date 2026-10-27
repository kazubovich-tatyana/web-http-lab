import psycopg
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
import models


class Settings(BaseSettings):
    DATABASE_URL: str = Field(...)
    model_config = SettingsConfigDict(env_file='.env', env_ignore_empty=True, extra = 'ignore')


settings = Settings()
pool = ConnectionPool(conninfo=settings.DATABASE_URL,
                      min_size=1, max_size=10,
                      open=True,
                      kwargs={'row_factory': dict_row})

def init_db():
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(models.CREATE_STATUS_ENUM)
            cur.execute(models.CREATE_USERS_TABLE)
            cur.execute(models.CREATE_NOTES_TABLE)
            cur.execute(models.CREATE_NOTES_INDEX)
            cur.execute(models.CREATE_USER_NOTES_INDEX)
            conn.commit()

def get_db():
    with pool.connection() as conn:
        yield conn
