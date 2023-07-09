from flask import Flask, render_template_string
from google.cloud import storage
import os

app = Flask(__name__)

# Authenticate with the service account
storage_client = storage.Client.from_service_account_json('path/to/keyfile.json')

@app.route('/gallery')
def gallery():
    # Fetch the items from your storage or database and prepare the 'items' list
    items = [
        {'name': 'Item 1', 'image_url': 'path/to/image1.jpg', 'id': 1},
        {'name': 'Item 2', 'image_url': 'path/to/image2.jpg', 'id': 2},
        # Add more items as needed
    ]

    # Render the gallery template with the items
    template = render_template_string(
        """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Gallery</title>
            <style>
                .gallery-item {
                    display: inline-block;
                    width: 200px;
                    margin: 10px;
                    text-align: center;
                }
            </style>
        </head>
        <body>
            <h1>Gallery</h1>
            <div class="gallery">
                {% for item in items %}
                    <div class="gallery-item">
                        <img src="{{ item.image_url }}" alt="{{ item.name }}" width="150" height="150">
                        <p>{{ item.name }}</p>
                        <input type="checkbox" name="item-checkbox" value="{{ item.id }}"> Grey out
                    </div>
                {% endfor %}
            </div>
        </body>
        </html>
        """,
        items=items
    )

    # Save the generated HTML content to a file
    html_file_path = os.path.join(os.getcwd(), 'templates', 'gallery.html')
    with open(html_file_path, 'w') as file:
        file.write(template)

    # Upload the HTML file to your Google Cloud Storage bucket
    bucket_name = 'your_bucket_name'
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob('gallery.html')
    blob.upload_from_filename(html_file_path)

    return 'Gallery HTML file generated and uploaded to Google Cloud Storage successfully!'

if __name__ == '__main__':
    app.run()
