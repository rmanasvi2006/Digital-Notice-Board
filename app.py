from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from PIL import Image
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)  # Secret key for session
import os
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(os.path.dirname(os.path.abspath(__file__)), "notices.db")}'  # This will create the database in the project root directory
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

db = SQLAlchemy(app)

# Create uploads directory if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

class Notice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_path = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=True)

    def as_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'image_path': self.image_path,
            'category': self.category,
            'created_at': self.created_at.isoformat(),
            'expires_at': self.expires_at.isoformat() if self.expires_at else None
        }

# Comment model for Q&A system
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    notice_id = db.Column(db.Integer, db.ForeignKey('notice.id'), nullable=False)
    user_name = db.Column(db.String(100), nullable=False)
    comment_text = db.Column(db.Text, nullable=False)
    is_admin_reply = db.Column(db.Boolean, default=False)
    reply_to_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def as_dict(self):
        return {
            'id': self.id,
            'notice_id': self.notice_id,
            'user_name': self.user_name,
            'comment_text': self.comment_text,
            'is_admin_reply': self.is_admin_reply,
            'reply_to_id': self.reply_to_id,
            'created_at': self.created_at.isoformat()
        }

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def is_admin():
    return 'admin' in session

@app.route('/')
def index():
    notices = Notice.query.order_by(Notice.created_at.desc()).all()
    return render_template('index.html', notices=notices)

@app.route('/admin')
def admin():
    if not is_admin():
        return redirect(url_for('login'))
    
    notices = Notice.query.order_by(Notice.created_at.desc()).all()
    return render_template('admin.html', notices=notices)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Simple admin credentials (in a real app, use proper authentication)
        if username == 'admin' and password == 'admin123':
            session['admin'] = True
            return redirect(url_for('admin'))
        else:
            return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('index'))

@app.route('/upload', methods=['POST'])
def upload():
    if not is_admin():
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        title = request.form.get('title')
        description = request.form.get('description')
        category = request.form.get('category')
        
        if not file or not title:
            return jsonify({'error': 'Title and file are required'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Allowed types: png, jpg, jpeg, gif'}), 400
        
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Save and resize image
        try:
            img = Image.open(file)
            img.thumbnail((800, 600))  # Resize to max 800x600
            img.save(filepath)
        except Exception as e:
            return jsonify({'error': f'Error processing image: {str(e)}'}), 500
        
        # Create notice record
        notice = Notice(
            title=title,
            description=description,
            image_path=filepath,
            category=category
        )
        db.session.add(notice)
        db.session.commit()
        
        return jsonify({'message': 'Notice uploaded successfully', 'notice': notice.as_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/search')
def search():
    query = request.args.get('q', '')
    category = request.args.get('category', '')
    
    notices = Notice.query
    
    if query:
        notices = notices.filter(
            (Notice.title.ilike(f'%{query}%')) |
            (Notice.description.ilike(f'%{query}%'))
        )
    
    if category and category != 'all':
        notices = notices.filter(Notice.category == category)
    
    notices = notices.order_by(Notice.created_at.desc()).all()
    
    return render_template('index.html', 
                         notices=notices,
                         search_query=query,
                         selected_category=category)

@app.route('/categories')
def get_categories():
    categories = db.session.query(Notice.category).distinct().all()
    return jsonify([cat[0] for cat in categories if cat[0]])

@app.route('/get_notice/<int:notice_id>', methods=['GET'])
def get_notice(notice_id):
    notice = Notice.query.get_or_404(notice_id)
    comments = Comment.query.filter_by(notice_id=notice_id).order_by(Comment.created_at.desc()).all()
    return jsonify({
        'notice': notice.as_dict(),
        'comments': [comment.as_dict() for comment in comments]
    })

@app.route('/post_comment', methods=['POST'])
def post_comment():
    data = request.json
    if not data or not all(key in data for key in ['notice_id', 'user_name', 'comment_text']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    comment = Comment(
        notice_id=data['notice_id'],
        user_name=data['user_name'],
        comment_text=data['comment_text'],
        is_admin_reply=False,
        reply_to_id=data.get('reply_to_id')
    )
    db.session.add(comment)
    db.session.commit()
    return jsonify(comment.as_dict())

@app.route('/post_admin_reply', methods=['POST'])
def post_admin_reply():
    if not is_admin():
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.json
    if not data or not all(key in data for key in ['notice_id', 'comment_text', 'reply_to_id']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    reply = Comment(
        notice_id=data['notice_id'],
        user_name='Admin',
        comment_text=data['comment_text'],
        is_admin_reply=True,
        reply_to_id=data['reply_to_id']
    )
    db.session.add(reply)
    db.session.commit()
    return jsonify(reply.as_dict())

@app.route('/view_notice/<int:notice_id>')
def view_notice(notice_id):
    notice = Notice.query.get_or_404(notice_id)
    comments = Comment.query.filter_by(notice_id=notice_id).order_by(Comment.created_at.desc()).all()
    return render_template('notice_detail.html', notice=notice, comments=comments, is_admin=is_admin)

@app.route('/notices/<int:notice_id>', methods=['DELETE'])
def delete_notice(notice_id):
    if not is_admin():
        return jsonify({'error': 'Unauthorized'}), 401
    
    notice = Notice.query.get_or_404(notice_id)
    if os.path.exists(notice.image_path):
        os.remove(notice.image_path)
    db.session.delete(notice)
    db.session.commit()
    return jsonify({'message': 'Notice deleted successfully'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
