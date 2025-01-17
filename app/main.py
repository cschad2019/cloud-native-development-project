import os
from flask import Flask, redirect, request, send_file, render_template

# Ensure 'files' directory exists
os.makedirs('files', exist_ok=True)

app = Flask(__name__)

############################
# 1st phase - all in 1 app #
############################

# Serve the main upload and display page
@app.route('/')
def index():
    # Placeholder for displaying an uploaded image
    image_url = None  # Replace this with actual logic if needed later
    return render_template('index.html', image_url=image_url)

# Handle file uploads
@app.route('/upload', methods=["POST"])
def upload():
    file = request.files['form_file']  # item name must match name in HTML form
    if file and file.filename.lower().endswith(('.jpeg', '.jpg', '.png')):
        file.save(os.path.join("./files", file.filename))
    return redirect("/")

# Serve individual files
@app.route('/files/<filename>')
def get_file(filename):
    return send_file('./files/' + filename)

# List previously uploaded files
@app.route('/previous_uploads')
def previous_uploads():
    files = os.listdir("./files")
    jpegs = [file for file in files if file.lower().endswith(('.jpeg', '.jpg', '.png'))]
    return render_template('previous_uploads.html', files=jpegs)

# Additional hardcoded HTML responses (from professor's code)
@app.route('/hardcoded')
def hardcoded_example():
    index_html = """
    <form method="post" enctype="multipart/form-data" action="/upload" method="post">
      <div>
        <label for="file">Choose file to upload</label>
        <input type="file" id="file" name="form_file" accept="image/jpeg"/>
      </div>
      <div>
        <button>Submit</button>
      </div>
    </form>
    """
    for file in list_files():
        index_html += f"<li><a href=\"/files/{file}\">{file}</a></li>"
    return index_html

# Function to list files in the directory
@app.route('/files')
def list_files():
    files = os.listdir("./files")
    jpegs = []
    for file in files:
        if file.lower().endswith(".jpeg") or file.lower().endswith(".jpg"):
            jpegs.append(file)
    return jpegs

if __name__ == '__main__':
    app.run(debug=True)
