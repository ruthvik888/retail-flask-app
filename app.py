
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
