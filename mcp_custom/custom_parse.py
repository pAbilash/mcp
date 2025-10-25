import aiosqlite
from fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("SQLite Explorer", version="0.1.0")

# Database initialization function
async def init_db():
    async with aiosqlite.connect("database.db") as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT
            )
            """
        )
        await db.commit()

# MCP Tool for adding an item
@mcp.tool("add_item")
async def add_item(name: str, description: str = None) -> str:
    """Adds a new item to the database."""
    async with aiosqlite.connect("database.db") as db:
        await db.execute(
            "INSERT INTO items (name, description) VALUES (?, ?)", (name, description)
        )
        await db.commit()
    return f"Item '{name}' added successfully."

# MCP Tool for getting all items
@mcp.tool("get_all_items")
async def get_all_items() -> list[dict]:
    """Retrieves all items from the database."""
    async with aiosqlite.connect("database.db") as db:
        db.row_factory = aiosqlite.Row  # Return rows as dict-like objects
        cursor = await db.execute("SELECT id, name, description FROM items")
        items = await cursor.fetchall()
        return [dict(item) for item in items]

# MCP Tool for deleting an item by ID
@mcp.tool("delete_item")
async def delete_item(item_id: int) -> str:
    """Deletes an item from the database by its ID."""
    async with aiosqlite.connect("database.db") as db:
        cursor = await db.execute("DELETE FROM items WHERE id = ?", (item_id,))
        await db.commit()
        if cursor.rowcount > 0:
            return f"Item with ID {item_id} deleted successfully."
        else:
            return f"No item found with ID {item_id}."

# Main execution block to run the server
if __name__ == "__main__":
    import asyncio
    asyncio.run(init_db())  # Initialize database before starting the server
    mcp.run(transport="stdio")