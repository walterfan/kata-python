"""Utility functions for PostgreSQL operations."""
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Dict, Any, Optional
from rich.console import Console
from rich.table import Table
from rich import print as rprint

console = Console()


def get_table_list(cursor: RealDictCursor) -> List[str]:
    """Get list of all tables in the current database."""
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        ORDER BY table_name;
    """)
    return [row['table_name'] for row in cursor.fetchall()]


def get_table_structure(cursor: RealDictCursor, table_name: str) -> List[Dict[str, Any]]:
    """Get detailed structure of a specific table."""
    cursor.execute("""
        SELECT 
            column_name,
            data_type,
            is_nullable,
            column_default,
            character_maximum_length,
            numeric_precision,
            numeric_scale
        FROM information_schema.columns 
        WHERE table_name = %s 
        ORDER BY ordinal_position;
    """, (table_name,))
    
    return cursor.fetchall()


def get_table_data(cursor: RealDictCursor, table_name: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Get sample data from a table."""
    cursor.execute(f"SELECT * FROM {table_name} LIMIT %s;", (limit,))
    return cursor.fetchall()


def get_table_count(cursor: RealDictCursor, table_name: str) -> int:
    """Get total row count for a table."""
    cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
    return cursor.fetchone()['count']


def display_table_structure(table_name: str, structure: List[Dict[str, Any]]) -> None:
    """Display table structure in a formatted table."""
    table = Table(title=f"Structure of table: {table_name}")
    
    table.add_column("Column", style="cyan", no_wrap=True)
    table.add_column("Type", style="magenta")
    table.add_column("Nullable", style="green")
    table.add_column("Default", style="yellow")
    table.add_column("Max Length", style="blue")
    
    for col in structure:
        max_length = col['character_maximum_length'] or col['numeric_precision']
        table.add_row(
            col['column_name'],
            col['data_type'],
            col['is_nullable'],
            str(col['column_default']) if col['column_default'] else '',
            str(max_length) if max_length else ''
        )
    
    console.print(table)


def display_table_data(table_name: str, data: List[Dict[str, Any]], count: int) -> None:
    """Display table data in a formatted table."""
    if not data:
        console.print(f"[yellow]No data found in table: {table_name}[/yellow]")
        return
    
    table = Table(title=f"Sample data from table: {table_name} (Total rows: {count})")
    
    # Add columns based on the first row
    if data:
        for column_name in data[0].keys():
            table.add_column(column_name, style="cyan")
    
    # Add rows
    for row in data:
        table.add_row(*[str(value) if value is not None else 'NULL' for value in row.values()])
    
    console.print(table)


def execute_custom_query(cursor: RealDictCursor, query: str) -> List[Dict[str, Any]]:
    """Execute a custom SQL query and return results."""
    try:
        cursor.execute(query)
        return cursor.fetchall()
    except psycopg2.Error as e:
        console.print(f"[red]Error executing query: {e}[/red]")
        return []


def display_query_results(query: str, results: List[Dict[str, Any]]) -> None:
    """Display query results in a formatted table."""
    if not results:
        console.print("[yellow]No results returned from query.[/yellow]")
        return
    
    table = Table(title=f"Query Results")
    
    # Add columns based on the first row
    if results:
        for column_name in results[0].keys():
            table.add_column(column_name, style="cyan")
    
    # Add rows
    for row in results:
        table.add_row(*[str(value) if value is not None else 'NULL' for value in row.values()])
    
    console.print(table)
