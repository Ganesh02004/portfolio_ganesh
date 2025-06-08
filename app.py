# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import os
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.secret_key = 'big-bang'

# MongoDB configuration
client = MongoClient('mongodb+srv://ganesh:Bigbang%402004@portfolio.ibwb3ld.mongodb.net/?retryWrites=true&w=majority&appName=Portfolio')
db = client.portfolio_db

# Collections
projects = db.projects
skills = db.skills
experience = db.experience
profile = db.profile
messages=db.messages
admin_users = db.admin_users


# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function



# Routes
@app.route('/')
def index():
    """Main portfolio page"""
    user_profile = profile.find_one() or {}
    user_projects = list(projects.find().sort('date', -1))
    user_skills = list(skills.find())
    user_experience = list(experience.find().sort('start_date', -1))
    
    return render_template('index.html', 
                         profile=user_profile,
                         projects=user_projects,
                         skills=user_skills,
                         experience=user_experience)


@app.route('/resume')
def resume():
    """Resume page"""
    user_profile = profile.find_one() or {}
    return render_template('resume.html', profile=user_profile)
    """Admin dashboard"""
    return render_template('admin.html')


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check credentials
        admin_user = admin_users.find_one({'username': username})
        
        if admin_user and check_password_hash(admin_user['password'], password):
            session['admin_logged_in'] = True
            session['admin_username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('admin'))
        else:
            flash('Invalid username or password!', 'error')
            
    return render_template('admin_login.html')


@app.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    session.pop('admin_logged_in', None)
    session.pop('admin_username', None)
    flash('You have been logged out successfully!', 'success')
    return redirect(url_for('index'))



@app.route('/admin')
@login_required
def admin():
    """Admin dashboard"""
    return render_template('admin.html')



@app.route('/admin/profile', methods=['GET', 'POST'])
@login_required
def admin_profile():
    """Manage profile information"""
    if request.method == 'POST':
        profile_data = {
            'name': request.form['name'],
            'title': request.form['title'],
            'email': request.form['email'],
            'phone': request.form['phone'],
            'location': request.form['location'],
            'bio': request.form['bio'],
            'linkedin': request.form['linkedin'],
            'github': request.form['github'],
            'website': request.form['website']
        }
        
        profile.replace_one({}, profile_data, upsert=True)
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('admin_profile'))
    
    user_profile = profile.find_one() or {}
    return render_template('admin_profile.html', profile=user_profile)

@app.route('/admin/projects')
@login_required
def admin_projects():
    """Manage projects"""
    user_projects = list(projects.find().sort('date', -1))
    return render_template('admin_projects.html', projects=user_projects)

@app.route('/admin/projects/add', methods=['GET', 'POST'])
@login_required
def add_project():
    """Add new project"""
    if request.method == 'POST':
        project_data = {
            'title': request.form['title'],
            'description': request.form['description'],
            'technologies': request.form['technologies'].split(','),
            'github_url': request.form['github_url'],
            'live_url': request.form['live_url'],
            'image_url': request.form['image_url'],
            'date': datetime.strptime(request.form['date'], '%Y-%m-%d'),
            'featured': 'featured' in request.form
        }
        
        projects.insert_one(project_data)
        flash('Project added successfully!', 'success')
        return redirect(url_for('admin_projects'))
    
    return render_template('add_project.html')

@app.route('/admin/projects/edit/<project_id>', methods=['GET', 'POST'])
@login_required
def edit_project(project_id):
    """Edit existing project"""
    project = projects.find_one({'_id': ObjectId(project_id)})
    
    if request.method == 'POST':
        updated_data = {
            'title': request.form['title'],
            'description': request.form['description'],
            'technologies': request.form['technologies'].split(','),
            'github_url': request.form['github_url'],
            'live_url': request.form['live_url'],
            'image_url': request.form['image_url'],
            'date': datetime.strptime(request.form['date'], '%Y-%m-%d'),
            'featured': 'featured' in request.form
        }
        
        projects.update_one({'_id': ObjectId(project_id)}, {'$set': updated_data})
        flash('Project updated successfully!', 'success')
        return redirect(url_for('admin_projects'))
    
    return render_template('edit_project.html', project=project)

@app.route('/admin/projects/delete/<project_id>')
@login_required
def delete_project(project_id):
    """Delete project"""
    projects.delete_one({'_id': ObjectId(project_id)})
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('admin_projects'))

@app.route('/admin/experience')
@login_required
def admin_experience():
    """Manage work experience"""
    user_experience = list(experience.find().sort('start_date', -1))
    return render_template('admin_experience.html', experience=user_experience)

@app.route('/admin/experience/add', methods=['GET', 'POST'])
@login_required
def add_experience():
    """Add work experience"""
    if request.method == 'POST':
        exp_data = {
            'company': request.form['company'],
            'position': request.form['position'],
            'location': request.form['location'],
            'start_date': datetime.strptime(request.form['start_date'], '%Y-%m-%d'),
            'end_date': datetime.strptime(request.form['end_date'], '%Y-%m-%d') if request.form['end_date'] else None,
            'current': 'current' in request.form,
            'description': request.form['description'],
            'achievements': request.form['achievements'].split('\n') if request.form['achievements'] else []
        }
        
        experience.insert_one(exp_data)
        flash('Experience added successfully!', 'success')
        return redirect(url_for('admin_experience'))
    
    return render_template('add_experience.html')

@app.route('/admin/skills')
@login_required
def admin_skills():
    """Manage skills"""
    user_skills = list(skills.find())
    return render_template('admin_skills.html', skills=user_skills)

@app.route('/admin/skills/add', methods=['GET', 'POST'])
@login_required
def add_skill():
    """Add skill"""
    if request.method == 'POST':
        skill_data = {
            'name': request.form['name'],
            'category': request.form['category'],
            'proficiency': int(request.form['proficiency'])
        }
        
        skills.insert_one(skill_data)
        flash('Skill added successfully!', 'success')
        return redirect(url_for('admin_skills'))
    
    return render_template('add_skill.html')

@app.route('/admin/skills/delete/<skill_id>')
@login_required
def delete_skill(skill_id):
    """Delete skill"""
    skills.delete_one({'_id': ObjectId(skill_id)})
    flash('Skill deleted successfully!', 'success')
    return redirect(url_for('admin_skills'))


@app.route('/api/contact', methods=['POST'])
@login_required
def contact():
    """Handle contact form submission"""
    try:
        # Get form data - check both form and JSON
        if request.is_json:
            data = request.get_json()
            name = data.get('name')
            email = data.get('email')
            message = data.get('message')
        else:
            name = request.form.get('name')
            email = request.form.get('email')
            message = request.form.get('message')
        
        # Debug print
        print(f"Received: name={name}, email={email}, message={message}")
        
        # Validate required fields
        if not name or not email or not message:
            return jsonify({'status': 'error', 'message': 'All fields are required!'})
        
        # Save to database
        contact_data = {
            'name': name,
            'email': email,
            'message': message,
            'date': datetime.now(),
            'read': False
        }
        
        messages.insert_one(contact_data)
        return jsonify({'status': 'success', 'message': 'Message sent successfully!'})
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'status': 'error', 'message': 'Failed to send message. Please try again.'})

@app.route('/admin/messages')
@login_required
def admin_messages():
    """View contact messages"""
    contact_messages = list(messages.find().sort('date', -1))
    return render_template('admin_messages.html', messages=contact_messages)

@app.route('/admin/messages/mark-read/<message_id>')
@login_required
def mark_message_read(message_id):
    """Mark message as read"""
    messages.update_one({'_id': ObjectId(message_id)}, {'$set': {'read': True}})
    flash('Message marked as read!', 'success')
    return redirect(url_for('admin_messages'))

@app.route('/admin/messages/delete/<message_id>')
@login_required
def delete_message(message_id):
    """Delete message"""
    messages.delete_one({'_id': ObjectId(message_id)})
    flash('Message deleted successfully!', 'success')
    return redirect(url_for('admin_messages'))

def init_dummy_data():
    """Initialize database with dummy data for Ganesh"""
    

    admin_users.delete_many({})
    
    # Create default admin user
    admin_data = {
        'username': 'toxezz',
        'password': generate_password_hash('Bigbang@2004'),
        'created_date': datetime.now()
    }
    admin_users.insert_one(admin_data)



if __name__ == '__main__':
    init_dummy_data()
    app.run(debug=True)
