from pydantic_settings import BaseSettings,SettingsConfigDict
from pydantic import Field
class Settings(BaseSettings):
    secret_key:str=Field(min_length=32)
    database_url:str
    algorithm:str="HS256"
    access_token_minutes:int=30
    model_config=SettingsConfigDict(env_file=".env")