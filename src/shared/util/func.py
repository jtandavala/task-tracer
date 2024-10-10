from functools import reduce


def compose(*functions):
    """Compose multiple functions together."""
    return reduce(lambda f, g: lambda x: f(g(x)), reversed(functions))


def setup_database(conn, tables):
    create_tables = compose(tables)
    create_tables(conn)
    conn.commit()
