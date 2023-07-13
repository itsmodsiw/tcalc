from flask import Flask, request
import psycopg2

app = Flask(__name__)

# Connect to the PostgreSQL database
conn = psycopg2.connect(os.environ['DATABASE_URL'])
cursor = conn.cursor()

# Endpoint to store user information
@app.route('/storeUser', methods=['POST'])
def store_user():
    try:
        wallet_address = request.json['walletAddress']
        cursor.execute('INSERT INTO users (wallet_address) VALUES (%s)', (wallet_address,))
        conn.commit()
        return 'User information stored successfully'
    except (Exception, psycopg2.Error) as error:
        print('Error storing user information:', error)
        return 'An error occurred while storing user information'

if __name__ == '__main__':
    app.run()
