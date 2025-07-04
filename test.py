import pyodbc

# Replace these with your SQL Server credentials
server = 'LAPTOP-ITJUVA2H\SQLExpress'  # Or your server name (e.g., .\SQLEXPRESS)
database = 'GOFASTT'   # Database to connect to

try:
    # Establish the connection using Windows Authentication (trusted connection)
    connection = pyodbc.connect(
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"Trusted_Connection=yes;"  # Use Windows Authentication
        f"Encrypt=no;"  # Optional: Disable encryption (use yes if needed)
    )
    print("Connection successful!")

    # Create a cursor to execute SQL queries
    cursor = connection.cursor()
    
    # Execute a query to list databases
    cursor.execute("SELECT name FROM sys.databases")
    
    # Fetch and display the results
    print("Databases available:")
    for row in cursor.fetchall():
        print(row[0])

    # Close the connection
    cursor.close()
    connection.close()

except pyodbc.Error as e:
    print("Error occurred:", e)
