from flask import Flask, flash, request, redirect, url_for, render_template, send_file
from werkzeug.utils import secure_filename
import os
from .style_transfer import load_image, get_image, model

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static/images')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def create_app():
    app = Flask(__name__, static_url_path='/static')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @app.route('/', methods=['GET', 'POST'])
    def upload_file():
        if request.method == 'POST':
            if 'style' not in request.files and 'content' not in request.files:
                flash('No file part')
                return redirect(request.url)
            style = request.files['style']
            content = request.files['content']
            if style.filename == '' and content.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if style and allowed_file(style.filename) and content and allowed_file(content.filename):
                stylename = secure_filename(style.filename)
                contentname = secure_filename(content.filename)
                if os.path.isfile(stylename):
                    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], stylename))
                if os.path.isfile(contentname):
                    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], contentname))
                style.save(os.path.join(app.config['UPLOAD_FOLDER'], stylename))
                content.save(os.path.join(app.config['UPLOAD_FOLDER'], contentname))
                return redirect(url_for('download_style', style=stylename, content=contentname))
        return render_template('home.html')

    @app.route('/style/<style>__<content>')
    def download_style(style, content):
        style_path = os.path.join(app.config['UPLOAD_FOLDER'], style)
        content_path = os.path.join(app.config['UPLOAD_FOLDER'], content)

        con_img, st_img = get_image(content_path, style_path)
        _ = model(con_img, st_img)

        if request.method == "POST":
            return redirect(url_for('download'))

        return render_template('style.html', content_image=content, style_image=style)

    @app.route('/download')
    def download():
        return send_file(os.path.join(app.config['UPLOAD_FOLDER'], 'style_photo.png'), as_attachment=True)


    return app