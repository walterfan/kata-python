"""Database configuration module."""
import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_database_config() -> Dict[str, Any]:
    """Get database configuration from environment variables."""
    return {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", "5432")),
        "database": os.getenv("DB_NAME", "postgres"),
        "user": os.getenv("DB_USERNAME", "postgres"),
        "password": os.getenv("DB_PASSWORD", "password"),
    }


def get_connection_string() -> str:
    """Get PostgreSQL connection string."""
    config = get_database_config()
    
    return (
        f"postgresql://{config['user']}:{config['password']}"
        f"@{config['host']}:{config['port']}/{config['database']}"
    )
