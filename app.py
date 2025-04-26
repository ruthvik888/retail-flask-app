
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return "<h2>Welcome to the Dashboard</h2>"

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        hshd = request.form.get('hshd_num')
        return f"Results for Household #{hshd}"
    return '''
        <form method="post">
            <label>Enter HSHD_NUM:</label>
            <input type="number" name="hshd_num">
            <input type="submit" value="Search">
        </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)

from azure.storage.blob import BlobServiceClient
import pandas as pd
from io import BytesIO

# Connect to Azure Blob Storage using your connection string
blob_service_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=retailanalyticsstorage1;AccountKey=3mX/rYbcn3WVf1rhCIA281tdDPypuMgN3A7nRrbgDwcUo7DUShJZOh6ORuYGUwF6oYZfyopMwo5C+ASt8D628A==;EndpointSuffix=core.windows.net")
container_name = "project-data"

# Function to load CSV data from Blob Storage
def load_data_from_blob(blob_name):
    # Get the blob client for the specific file
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    download_stream = blob_client.download_blob()
    data = download_stream.readall()
    return pd.read_csv(BytesIO(data))

# Load the households data (for Household #10 example)
df_households = load_data_from_blob('400_households.csv')

@app.route('/sample-data')
def sample_data():
    # Filter data for Household #10
    sample = df_households[df_households['HSHD_NUM'] == 10]
    return render_template('sample_data.html', data=sample)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)


