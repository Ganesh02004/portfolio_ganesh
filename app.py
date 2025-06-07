# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import os

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

@app.route('/admin')
def admin():
    """Admin dashboard"""
    return render_template('admin.html')

@app.route('/admin/profile', methods=['GET', 'POST'])
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
def admin_projects():
    """Manage projects"""
    user_projects = list(projects.find().sort('date', -1))
    return render_template('admin_projects.html', projects=user_projects)

@app.route('/admin/projects/add', methods=['GET', 'POST'])
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
def delete_project(project_id):
    """Delete project"""
    projects.delete_one({'_id': ObjectId(project_id)})
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('admin_projects'))

@app.route('/admin/experience')
def admin_experience():
    """Manage work experience"""
    user_experience = list(experience.find().sort('start_date', -1))
    return render_template('admin_experience.html', experience=user_experience)

@app.route('/admin/experience/add', methods=['GET', 'POST'])
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
def admin_skills():
    """Manage skills"""
    user_skills = list(skills.find())
    return render_template('admin_skills.html', skills=user_skills)

@app.route('/admin/skills/add', methods=['GET', 'POST'])
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
def delete_skill(skill_id):
    """Delete skill"""
    skills.delete_one({'_id': ObjectId(skill_id)})
    flash('Skill deleted successfully!', 'success')
    return redirect(url_for('admin_skills'))



@app.route('/api/contact', methods=['POST'])
def contact():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email') 
        message = data.get('message')

        print("Form name:", name)
        print("Form email:", email)
        print("Form message:", message)

        if not name or not email or not message:
            raise ValueError("Missing fields")

        contact_data = {
            'name': name,
            'email': email,
            'message': message,
            'timestamp': datetime.now(),
            'status': 'new'
        }

        db.contacts.insert_one(contact_data)

        return jsonify({
            'status': 'success', 
            'message': 'Thank you! Your message has been sent successfully!'
        })
    except Exception as e:
        print("ERROR:", e)
        return jsonify({
            'status': 'error',
            'message': 'Sorry, there was an error sending your message. Please try again.'
        }), 500

# Add route to view contact messages
@app.route('/admin/contacts')
def admin_contacts():
    """View contact messages"""
    contact_messages = list(db.contacts.find().sort('timestamp', -1))
    return render_template('admin_contacts.html', contacts=contact_messages)





if __name__ == '__main__':
    
    app.run(debug=True)
