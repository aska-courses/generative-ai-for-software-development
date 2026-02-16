"""Quick setup script"""
from app.database import create_tables, SessionLocal
from app.seed import seed_database

if __name__ == "__main__":
    print("🚀 Setting up Orders API...\n")
    
    # Create tables
    print("1. Creating database tables...")
    create_tables()
    print("   ✓ Tables created!\n")
    
    # Seed data
    print("2. Generating fake data...")
    db = SessionLocal()
    try:
        seed_database(db, 10000)
    finally:
        db.close()
    
    print("\n✅ Setup complete!")
    print("\nNext steps:")
    print("  Run API: uvicorn app.main:app --reload")
    print("  Run tests: pytest app/tests/ -v")
    print("  View docs: http://localhost:8000/docs")
