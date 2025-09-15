#!/usr/bin/env python3
"""PostgreSQL Python client demo.

This script demonstrates how to connect to PostgreSQL and query tables,
their structure, and data using psycopg2.
"""

import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Dict, Any
from rich.console import Console
from rich.panel import Panel
from rich import print as rprint

from config import get_database_config, get_connection_string
from utils import (
    get_table_list,
    get_table_structure,
    get_table_data,
    get_table_count,
    display_table_structure,
    display_table_data,
    execute_custom_query,
    display_query_results,
)

console = Console()


def connect_to_database() -> psycopg2.extensions.connection:
    """Establish connection to PostgreSQL database."""
    try:
        config = get_database_config()
        console.print(f"[green]Connecting to PostgreSQL database: {config['database']}@{config['host']}:{config['port']}[/green]")
        
        connection = psycopg2.connect(**config)
        console.print("[green]✓ Successfully connected to PostgreSQL![/green]")
        return connection
        
    except psycopg2.Error as e:
        console.print(f"[red]Error connecting to PostgreSQL: {e}[/red]")
        raise


def explore_database(connection: psycopg2.extensions.connection) -> None:
    """Explore database tables, their structure, and data."""
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        # Get list of all tables
        console.print("\n[bold blue]📋 Getting list of all tables...[/bold blue]")
        tables = get_table_list(cursor)
        
        if not tables:
            console.print("[yellow]No tables found in the database.[/yellow]")
            return
        
        console.print(f"[green]Found {len(tables)} tables: {', '.join(tables)}[/green]")
        
        # Explore each table
        for table_name in tables:
            console.print(f"\n{'='*60}")
            console.print(f"[bold cyan]🔍 Exploring table: {table_name}[/bold cyan]")
            
            # Get table structure
            console.print(f"\n[blue]📊 Table Structure:[/blue]")
            structure = get_table_structure(cursor, table_name)
            display_table_structure(table_name, structure)
            
            # Get table count
            count = get_table_count(cursor, table_name)
            console.print(f"\n[blue]📈 Total rows: {count}[/blue]")
            
            # Get sample data
            if count > 0:
                console.print(f"\n[blue]📄 Sample data (first 10 rows):[/blue]")
                sample_data = get_table_data(cursor, table_name, limit=10)
                display_table_data(table_name, sample_data, count)
            else:
                console.print(f"[yellow]Table {table_name} is empty.[/yellow]")


def run_sample_queries(connection: psycopg2.extensions.connection) -> None:
    """Run some sample queries to demonstrate different capabilities."""
    console.print(f"\n{'='*60}")
    console.print("[bold cyan]🔬 Running Sample Queries[/bold cyan]")
    
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        # Query 1: Database information
        console.print("\n[blue]📊 Database Information:[/blue]")
        db_info_query = """
            SELECT 
                current_database() as database_name,
                current_user as current_user,
                version() as postgresql_version,
                now() as current_time;
        """
        results = execute_custom_query(cursor, db_info_query)
        display_query_results("Database Info", results)
        
        # Query 2: Table sizes
        console.print("\n[blue]📏 Table Sizes:[/blue]")
        table_sizes_query = """
            SELECT 
                schemaname,
                tablename,
                pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
            FROM pg_tables 
            WHERE schemaname = 'public'
            ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
        """
        results = execute_custom_query(cursor, table_sizes_query)
        display_query_results("Table Sizes", results)
        
        # Query 3: Index information
        console.print("\n[blue]🔍 Index Information:[/blue]")
        index_query = """
            SELECT 
                schemaname,
                tablename,
                indexname,
                indexdef
            FROM pg_indexes 
            WHERE schemaname = 'public'
            ORDER BY tablename, indexname;
        """
        results = execute_custom_query(cursor, index_query)
        display_query_results("Indexes", results)


def interactive_mode(connection: psycopg2.extensions.connection) -> None:
    """Interactive mode for running custom queries."""
    console.print(f"\n{'='*60}")
    console.print("[bold cyan]🎮 Interactive Query Mode[/bold cyan]")
    console.print("[yellow]Enter SQL queries (type 'quit' to exit):[/yellow]")
    
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        while True:
            try:
                query = input("\nSQL> ").strip()
                
                if query.lower() in ['quit', 'exit', 'q']:
                    break
                
                if not query:
                    continue
                
                if query.lower().startswith('select'):
                    results = execute_custom_query(cursor, query)
                    display_query_results(query, results)
                else:
                    # For non-SELECT queries, execute and show affected rows
                    cursor.execute(query)
                    affected_rows = cursor.rowcount
                    console.print(f"[green]Query executed successfully. Rows affected: {affected_rows}[/green]")
                    connection.commit()
                    
            except KeyboardInterrupt:
                console.print("\n[yellow]Exiting interactive mode...[/yellow]")
                break
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")


def main() -> None:
    """Main function to demonstrate PostgreSQL operations."""
    console.print(Panel.fit(
        "[bold blue]PostgreSQL Python Client Demo[/bold blue]\n"
        "This demo shows how to connect to PostgreSQL and explore database structure and data.",
        title="🐘 PostgreSQL Client",
        border_style="blue"
    ))
    
    try:
        # Connect to database
        connection = connect_to_database()
        
        try:
            # Explore database
            explore_database(connection)
            
            # Run sample queries
            run_sample_queries(connection)
            
            # Interactive mode
            interactive_mode(connection)
            
        finally:
            connection.close()
            console.print("\n[green]✓ Database connection closed.[/green]")
            
    except Exception as e:
        console.print(f"[red]Fatal error: {e}[/red]")
        return 1
    
    console.print("\n[bold green]🎉 Demo completed successfully![/bold green]")
    return 0


if __name__ == "__main__":
    exit(main())
