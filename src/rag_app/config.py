from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "rag-knowledge-assistant"
    app_version: str = "0.1.0"
    chroma_persist_directory: str = "data/chroma_db"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    top_k: int = 4
    chunk_size: int = 800
    chunk_overlap: int = 120
    max_upload_bytes: int = 10 * 1024 * 1024

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


settings = Settings()
