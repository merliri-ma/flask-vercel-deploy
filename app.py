from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flashing messages

# Initialize the SQLite database
def init_db():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS resources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            type TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Fetch news and resources from the database
def get_news():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, title, content FROM news')
    news = cursor.fetchall()
    conn.close()
    return news

def get_resources():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, title, type FROM resources')
    resources = cursor.fetchall()
    conn.close()
    return resources

# Home route
@app.route('/')
def home():
    news = get_news()
    resources = get_resources()
    return render_template('index.html', news=news, resources=resources)

# Search route
@app.route('/search', methods=['GET'])
def search():
    search_term = request.args.get('search')
    news = get_news()
    resources = get_resources()
    filtered_news = [item for item in news if search_term.lower() in item[1].lower()]
    filtered_resources = [item for item in resources if search_term.lower() in item[1].lower()]
    return render_template('index.html', news=filtered_news, resources=filtered_resources, search_term=search_term)

# Add Resource route
@app.route('/add_resource', methods=['POST'])
def add_resource():
    resource_title = request.form.get('resource_title')
    resource_type = request.form.get('resource_type')

    if resource_title and resource_type:
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO resources (title, type) VALUES (?, ?)', (resource_title, resource_type))
        conn.commit()
        conn.close()
        flash('Resource added successfully!', 'success')
    else:
        flash('Title and Type are required fields!', 'error')
    
    return redirect(url_for('home'))

# Update Resource route
@app.route('/update_resource/<int:id>', methods=['GET', 'POST'])
def update_resource(id):
    if request.method == 'GET':
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, title, type FROM resources WHERE id = ?', (id,))
        resource = cursor.fetchone()
        conn.close()

        if resource:
            return render_template('update_resource.html', resource=resource)
        else:
            flash('Resource not found!', 'error')
            return redirect(url_for('home'))

    resource_title = request.form.get('resource_title')
    resource_type = request.form.get('resource_type')

    if resource_title and resource_type:
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE resources SET title = ?, type = ? WHERE id = ?', (resource_title, resource_type, id))
        conn.commit()
        conn.close()
        flash('Resource updated successfully!', 'success')
        return redirect(url_for('home'))
    
    flash('Title and Type are required fields!', 'error')
    return redirect(url_for('update_resource', id=id))

# Delete Resource route
@app.route('/delete_resource/<int:id>', methods=['GET'])
def delete_resource(id):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM resources WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Resource deleted successfully!', 'success')
    return redirect(url_for('home'))

# Post Info route (placeholder)
@app.route('/post_info', methods=['POST'])
def post_info():
    print("Post new information action triggered!")
    return redirect(url_for('home'))

# Initialize the database when the app starts
init_db()

if __name__ == '__main__':
    app.run(debug=True)