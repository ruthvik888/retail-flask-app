
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

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
    df.columns = df.columns.str.strip().str.upper()
    return df

df_households = load_data_from_blob('400_households.csv')
df_tx         = load_data_from_blob('400_transactions.csv')
df_prod       = load_data_from_blob('400_products.csv')

# Ensure numeric keys
df_households['HSHD_NUM']    = pd.to_numeric(df_households['HSHD_NUM'],    errors='coerce')
df_tx        ['HSHD_NUM']    = pd.to_numeric(df_tx        ['HSHD_NUM'],    errors='coerce')
df_tx        ['PRODUCT_NUM'] = pd.to_numeric(df_tx        ['PRODUCT_NUM'], errors='coerce')
df_prod      ['PRODUCT_NUM'] = pd.to_numeric(df_prod      ['PRODUCT_NUM'], errors='coerce')

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        try:
            h = int(request.form["hshd_num"])
        except ValueError:
            flash("Please enter a valid household number.", "danger")
            return redirect(url_for("search"))

        # join: Households → Transactions → Products
        hh   = df_house[df_house["HSHD_NUM"] == h]
        merged = pd.merge(hh, df_tx, on="HSHD_NUM", how="inner")
        merged = pd.merge(merged, df_prod, on="PRODUCT_NUM", how="inner")
        merged.sort_values(
            ["HSHD_NUM","BASKET_NUM","DATE","PRODUCT_NUM","DEPARTMENT","COMMODITY"],
            inplace=True
        )
        records = merged.to_dict(orient="records")

        if not records:
            flash(f"No data found for household #{h}.", "warning")
        return render_template("search_results.html", hshd=h, rows=records)

    return render_template("search.html")


@app.route("/sample-pull")
def sample_pull():
    # shortcut: redirect form to /search with HSHD_NUM=10
    return render_template("search.html", prefill=10)





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)


