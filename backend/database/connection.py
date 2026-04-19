"""
MongoDB connection using Motor + Beanie ODM.
Gracefully handles MongoDB being unavailable — server starts regardless.
"""
import os
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "lres")

client: AsyncIOMotorClient = None  # type: ignore
db_connected = False


async def init_db():
    """Initialize MongoDB connection and Beanie ODM."""
    global client, db_connected

    try:
        from database.models import Evaluation, AdminUser, LandRateDataset

        client = AsyncIOMotorClient(MONGO_URI, serverSelectionTimeoutMS=3000)

        # Test connection
        await client.server_info()

        db = client[MONGO_DB_NAME]
        await init_beanie(
            database=db,
            document_models=[Evaluation, AdminUser, LandRateDataset],
        )
        db_connected = True
        print(f"MongoDB connected: {MONGO_DB_NAME}")

        # Seed default admin
        await _seed_admin()

    except Exception as e:
        db_connected = False
        print(f"MongoDB not available ({e}). Server will run without database persistence.")
        print("   Install MongoDB or set MONGO_URI to a remote instance to enable database features.")


async def _seed_admin():
    """Create default admin on first run."""
    if not db_connected:
        return
    from database.models import AdminUser
    import bcrypt

    existing = await AdminUser.find_one(AdminUser.username == os.getenv("ADMIN_USERNAME", "admin"))
    if existing is None:
        username = os.getenv("ADMIN_USERNAME", "admin")
        password = os.getenv("ADMIN_PASSWORD", "admin123")
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        await AdminUser(username=username, password_hash=hashed).insert()
        print(f"Default admin created: {username}")


async def close_db():
    """Close MongoDB connection."""
    global client
    if client:
        client.close()


def is_db_connected() -> bool:
    return db_connected
