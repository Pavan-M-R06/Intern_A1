# PostgreSQL Connection Fix Guide

## Quick Diagnosis

Run this command to diagnose the issue:

```bash
cd backend
python scripts/test_db_connection.py
```

This will automatically:

- Test multiple connection scenarios
- Create the `intern_ai` database if needed
- Tell you the correct DATABASE_URL for your `.env` file

## Common Solutions

### Solution 1: Using Default Credentials

Most PostgreSQL installations on Windows use:

- **User**: `postgres`
- **Password**: The password you set during installation

Update your `.env` file:

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/intern_ai
```

Replace `YOUR_PASSWORD` with your actual PostgreSQL password.

### Solution 2: Password Reset (If You Forgot)

#### Using pgAdmin (Easiest):

1. Open pgAdmin
2. Connect to PostgreSQL Server
3. Right-click on "postgres" user → Properties
4. Go to "Definition" tab
5. Set new password → Save

#### Using Command Line (Advanced):

1. Find `pg_hba.conf` file (usually in `C:\Program Files\PostgreSQL\16\data\`)
2. Open as Administrator
3. Change line `host all all 127.0.0.1/32 md5` to `host all all 127.0.0.1/32 trust`
4. Restart PostgreSQL service:
   ```powershell
   Restart-Service postgresql-x64-16
   ```
5. Connect without password:
   ```bash
   psql -U postgres
   ```
6. Set new password:
   ```sql
   ALTER USER postgres PASSWORD 'newpassword';
   \q
   ```
7. Change `pg_hba.conf` back to `md5`
8. Restart PostgreSQL service again

### Solution 3: Create Database Manually

If the database doesn't exist:

```bash
# Find psql.exe (usually in C:\Program Files\PostgreSQL\16\bin\)
psql -U postgres

# Then in psql:
CREATE DATABASE intern_ai;
\q
```

### Solution 4: Check PostgreSQL Service

Ensure PostgreSQL is running:

```powershell
Get-Service postgresql*
```

If not running:

```powershell
Start-Service postgresql-x64-16
```

## After Fixing

Once you have the correct credentials:

1. Update `.env` file with correct DATABASE_URL
2. Run database initialization:
   ```bash
   python scripts/init_db.py
   ```
3. Start the backend:
   ```bash
   uvicorn app.main:app --reload
   ```

## Verify It Works

Test the connection:

```bash
python scripts/test_db_connection.py
```

Expected output: `✅ SUCCESS! Connection established.`

## Still Having Issues?

Check these:

1. **Port**: Ensure PostgreSQL is on port 5432

   ```powershell
   netstat -an | findstr 5432
   ```

2. **Firewall**: Ensure localhost connections are allowed

3. **Version**: Check PostgreSQL version matches expectations

   ```powershell
   Get-Service postgresql* | Select-Object Name, Status
   ```

4. **Alternative**: Use Docker PostgreSQL
   ```bash
   docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=intern_ai postgres:16
   ```
   Then use: `DATABASE_URL=postgresql://postgres:postgres@localhost:5432/intern_ai`
