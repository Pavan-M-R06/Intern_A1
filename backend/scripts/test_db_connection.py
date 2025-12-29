"""
PostgreSQL Connection Troubleshooting Script
Tests connection and provides detailed diagnostics
"""
import psycopg2
import sys
import os

# Test different connection scenarios
def test_connection_scenarios():
    """Test various PostgreSQL connection parameters"""
    
    print("=" * 70)
    print("PostgreSQL Connection Troubleshooting")
    print("=" * 70)
    
    # Common scenarios to test
    scenarios = [
        {
            "name": "Default postgres user (no password)",
            "params": {
                "host": "localhost",
                "port": 5432,
                "user": "postgres",
                "password": "",
                "dbname": "postgres"
            }
        },
        {
            "name": "Default postgres user (password: postgres)",
            "params": {
                "host": "localhost",
                "port": 5432,
                "user": "postgres",
                "password": "postgres",
                "dbname": "postgres"
            }
        },
        {
            "name": "Default postgres user (password: password)",
            "params": {
                "host": "localhost",
                "port": 5432,
                "user": "postgres",
                "password": "password",
                "dbname": "postgres"
            }
        },
        {
            "name": "Trust authentication (127.0.0.1)",
            "params": {
                "host": "127.0.0.1",
                "port": 5432,
                "user": "postgres",
                "password": "",
                "dbname": "postgres"
            }
        }
    ]
    
    successful_params = None
    
    for scenario in scenarios:
        print(f"\n🔍 Testing: {scenario['name']}")
        print(f"   Connection: postgresql://{scenario['params']['user']}:***@{scenario['params']['host']}:{scenario['params']['port']}/{scenario['params']['dbname']}")
        
        try:
            conn = psycopg2.connect(**scenario['params'])
            print(f"   ✅ SUCCESS! Connection established.")
            
            # Test if we can create a database
            conn.autocommit = True
            cursor = conn.cursor()
            
            # Check if intern_ai database exists
            cursor.execute("SELECT 1 FROM pg_database WHERE datname='intern_ai'")
            db_exists = cursor.fetchone()
            
            if db_exists:
                print(f"   ✅ Database 'intern_ai' already exists.")
            else:
                print(f"   ℹ️  Database 'intern_ai' does not exist.")
                print(f"   📝 Creating database 'intern_ai'...")
                try:
                    cursor.execute("CREATE DATABASE intern_ai")
                    print(f"   ✅ Database 'intern_ai' created successfully!")
                except Exception as e:
                    print(f"   ⚠️  Could not create database: {e}")
            
            cursor.close()
            conn.close()
            
            successful_params = scenario['params']
            break
            
        except psycopg2.OperationalError as e:
            print(f"   ❌ Failed: {e}")
        except Exception as e:
            print(f"   ❌ Unexpected error: {e}")
    
    print("\n" + "=" * 70)
    
    if successful_params:
        print("✅ SOLUTION FOUND!")
        print("\n📝 Update your .env file with these credentials:")
        print(f"DATABASE_URL=postgresql://{successful_params['user']}:{successful_params['password']}@{successful_params['host']}:{successful_params['port']}/intern_ai")
        print("\n🎉 You can now run: python scripts/init_db.py")
        return successful_params
    else:
        print("❌ NO WORKING CONNECTION FOUND")
        print("\n💡 NEXT STEPS:")
        print("\n1. Find your PostgreSQL installation directory:")
        print("   - Check: C:\\Program Files\\PostgreSQL\\")
        print("   - Look for: bin\\psql.exe")
        print("\n2. Reset PostgreSQL password:")
        print("   Method A - Using pgAdmin:")
        print("     - Open pgAdmin")
        print("     - Right-click postgres user → Properties → Definition")
        print("     - Set new password")
        print("\n   Method B - Using command line (as admin):")
        print("     - Find pg_hba.conf file")
        print("     - Change 'md5' to 'trust' temporarily")
        print("     - Restart PostgreSQL service")
        print("     - Run: psql -U postgres")
        print("     - Run: ALTER USER postgres PASSWORD 'newpassword';")
        print("     - Change pg_hba.conf back to 'md5'")
        print("     - Restart PostgreSQL service")
        print("\n3. Check PostgreSQL service is running:")
        print("   PowerShell: Get-Service postgresql*")
        print("\n4. Check which port PostgreSQL is using:")
        print("   netstat -an | findstr 5432")
        
        return None


def check_environment():
    """Check if .env file exists and has DATABASE_URL"""
    print("\n📁 Checking environment configuration...")
    
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    
    if not os.path.exists(env_path):
        print("   ⚠️  .env file not found!")
        print(f"   Expected location: {env_path}")
        print("   💡 Copy .env.example to .env and configure it")
        return False
    
    print(f"   ✅ .env file exists")
    
    # Check for DATABASE_URL
    with open(env_path, 'r') as f:
        content = f.read()
        if 'DATABASE_URL' in content:
            print("   ✅ DATABASE_URL is configured")
            # Try to extract it (simple parsing)
            for line in content.split('\n'):
                if line.startswith('DATABASE_URL='):
                    url = line.split('=', 1)[1].strip()
                    # Mask password
                    if '@' in url:
                        parts = url.split('@')
                        creds = parts[0].split('://')[-1]
                        if ':' in creds:
                            user, _ = creds.split(':', 1)
                            masked_url = url.replace(creds, f"{user}:***")
                            print(f"   Current value: {masked_url}")
                    return True
        else:
            print("   ⚠️  DATABASE_URL not found in .env file")
            return False
    
    return True


if __name__ == "__main__":
    print("\n🔧 Intern_AI - PostgreSQL Connection Troubleshooting\n")
    
    # Check environment first
    env_ok = check_environment()
    
    if not env_ok:
        print("\n⚠️  Please configure .env file first")
        sys.exit(1)
    
    # Test connection scenarios
    result = test_connection_scenarios()
    
    sys.exit(0 if result else 1)
