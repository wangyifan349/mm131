from flask import Flask, render_template
import os

app = Flask(__name__)

# 设置静态文件夹路径
IMAGE_FOLDER = os.path.join('static', 'images')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/all-images')
def all_images():
    images = []
    for filename in os.listdir(IMAGE_FOLDER):
        if filename.endswith(('.png', '.jpg', '.jpeg', '.gif')):
            images.append({
                'src': f'/{IMAGE_FOLDER}/{filename}',
                'title': filename
            })
    return render_template('all-images.html', images=images)

if __name__ == '__main__':
    app.run(debug=True)














