from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SUPABASE_URL: str = "https://your-project.supabase.co"
    SUPABASE_KEY: str = "your-supabase-service-role-key"
    TINYFISH_API_KEY: str = "tf_live_your_tinyfish_key"
    TINYFISH_BASE_URL: str = "https://api.tinyfish.io/v1"
    OPENAI_API_KEY: str = "sk-your-llm-key"
    GROQ_API_KEY: str = ""
    USER_ALIAS_DOMAIN: str = "myscout.id"
    WEBHOOK_SECRET: str = "scout_edge_secret_2026"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
