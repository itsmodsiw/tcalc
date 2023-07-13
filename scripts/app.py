from flask import Flask, render_template_string, request
from google.cloud import storage
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Authenticate with the service account
storage_client = storage.Client.from_service_account_json(os.getenv('JSON_KEY_PATH'))

# Store IDs of images to be grayed out
grayed_out_ids = set()

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    bucket_name = os.getenv('GCS_BUCKET_NAME')
    bucket = storage_client.get_bucket(bucket_name)
    blobs = bucket.list_blobs()

    items = [{'name': blob.name, 'image_url': f'https://storage.googleapis.com/{bucket_name}/{blob.name}', 'id': i+1} for i, blob in enumerate(blobs)]

    if request.method == 'POST':
        # Update grayed_out_ids based on form submission
        grayed_out_ids.clear()
        for item in items:
            if request.form.get(f'item-checkbox-{item["id"]}') == 'on':
                grayed_out_ids.add(item['id'])

    # Include information about which images are grayed out
    for item in items:
        item['grayed_out'] = item['id'] in grayed_out_ids

    # Render the admin template
    template = render_template_string("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Admin</title>
        </head>
        <body>
            <h1>Admin</h1>
            <form method="post">
                {% for item in items %}
                    <div>
                        <img src="{{ item.image_url }}" alt="{{ item.name }}" width="150" height="150" {% if item.grayed_out %}class="grayed-out"{% endif %}>
                        <p>{{ item.name }}</p>
                        <input type="checkbox" name="item-checkbox-{{ item.id }}" {% if item.grayed_out %}checked{% endif %}> Grey out
                    </div>
                {% endfor %}
                <input type="submit" value="Update">
            </form>
        </body>
        </html>
        """, items=items)
    return template

@app.route('/gallery')
def gallery():
    bucket_name = os.getenv('GCS_BUCKET_NAME')
    bucket = storage_client.get_bucket(bucket_name)
    blobs = bucket.list_blobs()

    items = [{'name': blob.name, 'image_url': f'https://storage.googleapis.com/{bucket_name}/{blob.name}', 'id': i+1} for i, blob in enumerate(blobs)]

    # Include information about which images are grayed out
    for item in items:
        item['grayed_out'] = item['id'] in grayed_out_ids

    # Render the gallery template
    template = render_template_string("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Gallery</title>
            <style>
                .grayed-out {
                    filter: grayscale(100%);
                }
            </style>
        </head>
        <body>
            <h1>Gallery</h1>
            {% for item in items %}
                <div>
                    <img src="{{ item.image_url }}" alt="{{ item.name }}" width="150" height="150" {% if item.grayed_out %}class="grayed-out"{% endif %}>
                    <p>{{ item.name }}</p>
                </div>
            {% endfor %}
        </body>
        </html>
        """, items=items)
    return template

if __name__ == '__main__':
    app.run()
