"""
Direct PostgreSQL Password Verification
This script helps you find and verify the correct password
"""
import psycopg2
import getpass

def test_specific_password():
    """Test with user-provided password"""
    print("=" * 70)
    print("PostgreSQL Password Verification")
    print("=" * 70)
    
    print("\nℹ️  Your current .env shows: postgresql://postgres:***@localhost:5432/intern_ai")
    print("\nLet's verify the correct password interactively.\n")
    
    # Get password from user
    password = getpass.getpass("Enter your PostgreSQL password for user 'postgres': ")
    
    # Test connection
    print("\n🔍 Testing connection...")
    
    try:
        conn_params = {
            "host": "localhost",
            "port": 5432,
            "user": "postgres",
            "password": password,
            "dbname": "postgres"  # Connect to default database first
        }
        
        conn = psycopg2.connect(**conn_params)
        print("✅ SUCCESS! Password is correct!\n")
        
        # Now check/create intern_ai database
        conn.autocommit = True
        cursor = conn.cursor()
        
        cursor.execute("SELECT 1 FROM pg_database WHERE datname='intern_ai'")
        db_exists = cursor.fetchone()
        
        if db_exists:
            print("✅ Database 'intern_ai' already exists")
        else:
            print("📝 Creating database 'intern_ai'...")
            try:
                cursor.execute("CREATE DATABASE intern_ai")
                print("✅ Database created!")
            except Exception as e:
                print(f"⚠️  Error creating database: {e}")
        
        cursor.close()
        conn.close()
        
        # Show the correct DATABASE_URL
        print("\n" + "=" * 70)
        print("✅ COPY THIS TO YOUR .env FILE:")
        print("=" * 70)
        print(f"\nDATABASE_URL=postgresql://postgres:{password}@localhost:5432/intern_ai\n")
        print("=" * 70)
        
        return True
        
    except psycopg2.OperationalError as e:
        print(f"❌ Connection failed: {e}\n")
        
        if "password authentication failed" in str(e):
            print("💡 The password is incorrect. Try again or reset it using pgAdmin.")
        elif "no password supplied" in str(e):
            print("💡 No password was provided. Press Enter and try again.")
        
        return False


def offer_solutions():
    """Provide alternative solutions"""
    print("\n" + "=" * 70)
    print("ALTERNATIVE SOLUTIONS:")
    print("=" * 70)
    
    print("\n1️⃣  RESET PASSWORD USING pgAdmin (EASIEST):")
    print("   - Open pgAdmin (should be in Start Menu)")
    print("   - Connect to PostgreSQL Server (you may need to enter current password)")
    print("   - Expand 'Servers' → PostgreSQL 16")
    print("   - Right-click 'Login/Group Roles' → 'postgres' → 'Properties'")
    print("   - Go to 'Definition' tab")
    print("   - Enter new password: 'postgres' (or any password you'll remember)")
    print("   - Click 'Save'")
    print("   - Then update .env with: DATABASE_URL=postgresql://postgres:postgres@localhost:5432/intern_ai")
    
    print("\n2️⃣  USE DOCKER PostgreSQL (CLEAN SLATE):")
    print("   - Stop current PostgreSQL service:")
    print("     Stop-Service postgresql*")
    print("   - Run PostgreSQL in Docker:")
    print("     docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=intern_ai --name intern_ai_db postgres:16")
    print("   - Update .env:")
    print("     DATABASE_URL=postgresql://postgres:postgres@localhost:5432/intern_ai")
    
    print("\n3️⃣  ENABLE TRUST AUTHENTICATION (TEMPORARY - LOCAL ONLY):")
    print("   This allows connections without a password temporarily.")
    print("   ⚠️  Only for local development!")
    print("\n   Steps:")
    print("   a) Find pg_hba.conf file:")
    print("      - Usually at: C:\\Program Files\\PostgreSQL\\16\\data\\pg_hba.conf")
    print("      - Open with Notepad as Administrator")
    print("   b) Find lines with '127.0.0.1/32' and 'md5'")
    print("   c) Change 'md5' to 'trust' on those lines")
    print("   d) Save the file")
    print("   e) Restart PostgreSQL:")
    print("      Restart-Service postgresql-x64-16")
    print("   f) Update .env:")
    print("      DATABASE_URL=postgresql://postgres:@localhost:5432/intern_ai")
    print("      (note: empty password)")


if __name__ == "__main__":
    success = test_specific_password()
    
    if not success:
        offer_solutions()
        print("\n💡 After fixing, run this script again to verify.")
