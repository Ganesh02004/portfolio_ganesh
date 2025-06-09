# Professional Portfolio Web App

A dynamic, responsive portfolio web application built with Flask, MongoDB, and Bootstrap. Perfect for showcasing your professional experience, projects, and skills with an easy-to-use admin panel for content management.

## Features

### 🎨 Frontend
- **Responsive Design**: Mobile-first approach with Bootstrap 5
- **Modern UI**: Clean, professional design with smooth animations
- **Interactive Elements**: Hover effects, smooth scrolling, and dynamic content
- **Multi-section Layout**: Hero, About, Experience, Projects, Skills, Contact

### ⚙️ Backend
- **Flask Framework**: Lightweight Python web framework
- **MongoDB Integration**: NoSQL database for flexible data storage
- **Dynamic Content**: All content manageable through admin panel
- **RESTful Routes**: Clean URL structure and API endpoints

### 👨‍💼 Admin Panel
- **Profile Management**: Update personal information and bio
- **Project Management**: Add, edit, delete projects with technologies and links
- **Experience Management**: Manage work history and achievements
- **Skills Management**: Organize skills by categories with proficiency levels
- **User-Friendly Interface**: Intuitive forms and navigation

## Demo Data

The application comes pre-loaded with sample data for **Ganesh P**, an AI/ML Engineering student at BITM College, including:

- 4 AI/ML projects (Stock Prediction, Sentiment Analysis, Image Classification, Chatbot)
- 2 work experiences (AI/ML Intern, Data Science Trainee)
- 20+ technical skills across 5 categories
- Complete professional profile with contact information

## Tech Stack

- **Backend**: Python, Flask
- **Database**: MongoDB
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Icons**: Font Awesome
- **Template Engine**: Jinja2

## Prerequisites

Before running this application, make sure you have:

- Python 3.7 or higher
- MongoDB installed locally or MongoDB Atlas account
- Git (for cloning the repository)

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Ganesh02004/portfolio_ganesh.git
cd portfolio-webapp
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up MongoDB

#### Option A: Local MongoDB
1. Install MongoDB Community Edition from [mongodb.com](https://www.mongodb.com/try/download/community)
2. Start MongoDB service:
   ```bash
   # Windows
   net start MongoDB
   
   # macOS
   brew services start mongodb/brew/mongodb-community
   
   # Linux
   sudo systemctl start mongod
   ```

#### Option B: MongoDB Atlas (Cloud)
1. Create a free account at [MongoDB Atlas](https://www.mongodb.com/atlas)
2. Create a new cluster
3. Update the connection string in `app.py`:
   ```python
   client = MongoClient('mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/')
   ```

### 5. Configure Environment Variables (Optional)
Create a `.env` file in the root directory:
```env
SECRET_KEY=your-secret-key-here
MONGODB_URI=mongodb://localhost:27017/
DEBUG=True
```

## Running the Application

### 1. Start the Application
```bash
python app.py
```

### 2. Access the Application
- **Main Portfolio**: http://localhost:5000
- **Admin Panel**: http://localhost:5000/admin

The application will automatically initialize with dummy data on first run.

## Project Structure

```
portfolio-webapp/
│
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
│
├── templates/            # Jinja2 templates
│   ├── base.html         # Base template
│   ├── index.html        # Main portfolio page
│   ├── admin.html        # Admin dashboard
│   ├── admin_profile.html
│   ├── admin_projects.html
│   ├── admin_experience.html
│   ├── admin_skills.html
│   ├── add_project.html
│   ├── edit_project.html
│   ├── add_experience.html
│   └── add_skill.html
│
└── static/               # Static files
    └── css/
        └── style.css     # Custom CSS styles
```

## Usage

### Admin Panel Navigation

1. **Profile Management** (`/admin/profile`)
   - Update personal information
   - Edit bio and contact details
   - Manage social media links

2. **Projects Management** (`/admin/projects`)
   - Add new projects with descriptions
   - Upload project images
   - Link to GitHub repositories and live demos
   - Organize by technologies used

3. **Experience Management** (`/admin/experience`)
   - Add work experience entries
   - Include achievements and responsibilities
   - Set current position status

4. **Skills Management** (`/admin/skills`)
   - Organize skills by categories
   - Set proficiency levels (0-100%)
   - Add new skill categories

### Customization

#### Updating Colors and Styling
Edit `static/css/style.css` to customize:
```css
:root {
    --primary-color: #007bff;    /* Change primary color */
    --secondary-color: #6c757d;  /* Change secondary color */
    --dark-color: #343a40;       /* Change dark theme color */
}
```

#### Adding New Sections
1. Update the database schema in `app.py`
2. Create new routes and templates
3. Add navigation links in `base.html`

## Database Schema

### Collections

#### Profile
```json
{
  "name": "String",
  "title": "String",
  "email": "String",
  "phone": "String",
  "location": "String",
  "bio": "String",
  "linkedin": "String",
  "github": "String",
  "website": "String"
}
```

#### Projects
```json
{
  "title": "String",
  "description": "String",
  "technologies": ["Array of Strings"],
  "github_url": "String",
  "live_url": "String",
  "image_url": "String",
  "date": "Date",
  "featured": "Boolean"
}
```

#### Experience
```json
{
  "company": "String",
  "position": "String",
  "location": "String",
  "start_date": "Date",
  "end_date": "Date",
  "current": "Boolean",
  "description": "String",
  "achievements": ["Array of Strings"]
}
```

#### Skills
```json
{
  "name": "String",
  "category": "String",
  "proficiency": "Number (0-100)"
}
```


### Deployment Options
- **AWS EC2**: Deploy on Amazon Web Services
- **DigitalOcean**: Use their App Platform or Droplets
- **Vercel**: For serverless deployment
- **Railway**: Simple deployment platform

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Troubleshooting

### Common Issues

#### MongoDB Connection Error
```
pymongo.errors.ServerSelectionTimeoutError
```
**Solution**: Ensure MongoDB is running and the connection string is correct.

#### Template Not Found Error
```
jinja2.exceptions.TemplateNotFound
```
**Solution**: Ensure all template files are in the `templates/` directory.

#### Static Files Not Loading
**Solution**: Check that static files are in the `static/` directory and Flask is configured correctly.

#### Port Already in Use
```
OSError: [Errno 48] Address already in use
```
**Solution**: Change the port in `app.py` or kill the process using the port:
```bash
# Find process using port 5000
lsof -i :5000
# Kill the process
kill -9 <PID>
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/Ganesh02004/portfolio_ganesh/issues) section
2. Create a new issue with detailed information
3. Contact the maintainer

## Acknowledgments

- Bootstrap team for the responsive framework
- Flask community for the excellent documentation
- MongoDB for the flexible database solution
- Font Awesome for the beautiful icons

---

**Happy Coding...!** 🚀


