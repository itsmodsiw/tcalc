import os
from flask import Flask
from google.cloud import storage

app = Flask(__name__)

# Retrieve the JSON key file path from the environment variable
json_key_path = os.environ.get('JSON_KEY_PATH')

# Authenticate with the service account
storage_client = storage.Client.from_service_account_json(json_key_path)

# Fetch and display items from the bucket
@app.route('/gallery')
def gallery():
    bucket_name = 'oracles'

    # Get a reference to the bucket
    bucket = storage_client.get_bucket(bucket_name)

    # Fetch the items from the bucket
    items = []
    blobs = bucket.list_blobs()
    for blob in blobs:
        item = {
            'name': blob.name,
            'id': generate_item_id(blob.name)  # Implement your logic to generate item IDs
        }
        items.append(item)

    # Render the gallery template with the items
    return render_template('gallery.html', items=items)

# Update item status
@app.route('/admin/update_item_status', methods=['POST'])
def update_item_status():
    item_id = request.form.get('item_id')
    checked = request.form.get('checked')

    # Update the item's status in the storage system based on 'item_id' and 'checked'

    # Return a response, such as a success message
    return jsonify({'message': 'Item status updated successfully'})

if __name__ == '__main__':
    app.run()
