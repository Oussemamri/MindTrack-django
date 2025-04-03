# MindTrack

MindTrack is a comprehensive learning management platform designed to help users track, manage, and enhance their educational journey through interactive quizzes, personalized learning paths, and AI-powered assistance.

![MindTrack Dashboard](https://img.freepik.com/free-vector/online-learning-isometric-concept_1284-17947.jpg)

## 📸 Application Screenshots

Here are some screenshots of the MindTrack application:

### Dashboard View
![Dashboard View](/screenshots/Dashboard%20View.png)
*The main dashboard showing learning progress, recent activities, and quick access to features.*

### Learning Path Interface
![Learning Path](/screenshots/Learning%20Path.png)
*The learning path interface showing topic progression and quiz requirements.*

### AI Assistant
![AI Assistant](/screenshots/AI%20Assistant.png)
*The AI Learning Assistant providing personalized recommendations and answers.*

## 🌟 Features

### 📚 Quiz System
- Create AI-generated quizzes on various topics
- Take quizzes and receive immediate feedback
- Review quiz performance with detailed statistics
- Teacher/student role-based access control

### 🛣️ Learning Paths
- Create structured learning journeys
- Organize topics in a logical sequence
- Set completion thresholds for progression
- Track progress through learning paths

### ⏱️ Study Sessions
- Track study time and increase productivity
- Record different types of learning activities
- Measure progress and focus during study sessions
- Analyze study patterns and improvements

### 🤖 AI Learning Assistant
- Get personalized learning recommendations
- Ask questions about specific topics
- Generate study plans and learning paths
- Receive instant assistance with learning challenges

### 📊 Dashboard Analytics
- View progress across all learning activities
- Track quiz performance and improvements
- Monitor study session effectiveness
- Visualize learning path completion

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- Django 5.0 or higher
- SQLite (default) or PostgreSQL

### Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/yourusername/MindTrack-django.git
cd MindTrack-django
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
```
Then edit the `.env` file with your API keys and configuration.

5. Run migrations:
```bash
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

8. Open your browser and navigate to:
```
http://127.0.0.1:8000/
```

## 💻 Usage

### User Roles
- **Students**: Can take quizzes, enroll in learning paths, track study sessions
- **Teachers**: Can create quizzes, design learning paths, access performance analytics

### Creating Quizzes
Teachers can create quizzes by:
1. Navigating to "Quizzes" → "Create Quiz"
2. Selecting a topic and entering a title
3. Specifying the number of questions
4. The AI system will generate questions and answers automatically

### Creating Learning Paths
To create a structured learning journey:
1. Go to "Learning Paths" → "Create Path"
2. Add a title and description
3. Add topics in the desired order
4. Specify required quizzes and completion thresholds
5. Publish the path when ready

### Starting Study Sessions
Track your learning time with:
1. Navigate to "Study Sessions"
2. Click "Start Learning"
3. Add different activities during your session
4. Complete the session to record your progress

### Using the AI Assistant
Get help with your learning:
1. Go to "AI Assistant" or use the assistant in your dashboard
2. Ask questions about topics, request explanations, or get learning path recommendations
3. The AI will provide personalized responses to help your learning journey

## 🧩 Project Structure

```
MindTrack-django/
├── accounts/            # User authentication and profiles
├── learning_paths/      # Learning path management
├── mindtrack/           # Project core settings
├── quiz_app/            # Quiz generation and management
├── study_sessions/      # Study time tracking
├── manage.py            # Django management script
├── requirements.txt     # Project dependencies
└── README.md            # Project documentation
```

## 🛠️ Technologies Used

- **Backend**: Django, Python
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Database**: SQLite (default), PostgreSQL (production)
- **AI Integration**: Hugging Face API, GPT4All
- **Authentication**: Django built-in auth system
- **Styling**: Bootstrap 5, Font Awesome
- **Other**: Chart.js (for analytics visualizations)

## 🔄 API Endpoints

- `/accounts/` - User management
- `/quiz/` - Quiz creation and submission
- `/paths/` - Learning path management
- `/sessions/` - Study session tracking
- `/paths/ai-assistant/` - AI assistant endpoint

## 🤝 Contributing

Contributions to MindTrack are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📬 Contact

- Project Creator: [oussema amri](oussema9100@gmail.com)
- Project Link: [https://github.com/Oussemamri/MindTrack-django](https://github.com/Oussemamri/MindTrack-django)

---

Built with ❤️ by [oussema amri]
