# PostgreSQL Python Client Demo

This is a comprehensive demo of how to use the PostgreSQL Python client to connect to a PostgreSQL database, explore table structures, and query data using `psycopg2`.

## Features

- 🔌 **Database Connection**: Connect to PostgreSQL using environment variables
- 📋 **Table Exploration**: List all tables in the database
- 📊 **Structure Analysis**: Get detailed table structure (columns, types, constraints)
- 📄 **Data Sampling**: View sample data from tables
- 🔍 **Custom Queries**: Interactive SQL query mode
- 📈 **Database Statistics**: Table sizes, indexes, and database information
- 🎨 **Rich Output**: Beautiful formatted tables using Rich library

## Prerequisites

- Python 3.10+
- PostgreSQL 15+
- Poetry (for dependency management)

## Setup

1. **Clone and navigate to the project:**
   ```bash
   cd pg-client
   ```

2. **Install dependencies:**
   ```bash
   poetry install
   ```

3. **Configure database connection:**
   ```bash
   cp env.example .env
   ```
   
   Edit `.env` file with your PostgreSQL credentials:
   ```env
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=your_database
   DB_USERNAME=your_username
   DB_PASSWORD=your_password
   ```

4. **Ensure PostgreSQL is running** and accessible with the provided credentials.

## Usage

### Basic Usage

Run the demo script:
```bash
poetry run python main.py
```

The script will:
1. Connect to your PostgreSQL database
2. List all tables in the `public` schema
3. Show structure and sample data for each table
4. Display database statistics and information
5. Enter interactive mode for custom SQL queries

### Interactive Mode

When the script enters interactive mode, you can run custom SQL queries:

```sql
SQL> SELECT * FROM users WHERE created_at > '2023-01-01';
SQL> SELECT table_name, column_name FROM information_schema.columns WHERE table_schema = 'public';
SQL> quit
```

### Programmatic Usage

You can also import and use the modules in your own code:

```python
from config import get_database_config
from utils import get_table_list, get_table_structure
import psycopg2
from psycopg2.extras import RealDictCursor

# Connect to database
config = get_database_config()
connection = psycopg2.connect(**config)

# Get table information
with connection.cursor(cursor_factory=RealDictCursor) as cursor:
    tables = get_table_list(cursor)
    structure = get_table_structure(cursor, tables[0])
    
connection.close()
```

## Project Structure

```
pg-client/
├── main.py              # Main demo script
├── config.py            # Database configuration
├── utils.py             # Utility functions for database operations
├── pyproject.toml       # Poetry configuration and dependencies
├── env.example          # Environment variables template
└── README.md           # This file
```

## Dependencies

- **psycopg2-binary**: PostgreSQL adapter for Python
- **python-dotenv**: Load environment variables from .env file
- **rich**: Rich text and beautiful formatting in the terminal

## Development Dependencies

- **pytest**: Testing framework
- **black**: Code formatter
- **flake8**: Linting
- **mypy**: Type checking

## Example Output

The script provides rich, formatted output showing:

- 📋 **Table List**: All tables in the database
- 📊 **Table Structure**: Column details with types and constraints
- 📄 **Sample Data**: First 10 rows from each table
- 📈 **Statistics**: Table sizes and row counts
- 🔍 **Database Info**: Version, user, and connection details

## Troubleshooting

### Connection Issues

1. **Check PostgreSQL is running:**
   ```bash
   pg_isready -h localhost -p 5432
   ```

2. **Verify credentials** in your `.env` file

3. **Check firewall/network** if connecting to remote database

### Permission Issues

Ensure your database user has appropriate permissions:
```sql
-- Grant necessary permissions
GRANT USAGE ON SCHEMA public TO your_user;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO your_user;
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `poetry run pytest`
5. Format code: `poetry run black .`
6. Submit a pull request

## License

This project is open source and available under the MIT License.


