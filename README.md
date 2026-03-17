# ToDoList

A Django-based task management web application for organising daily tasks, managing categories, tracking progress, and improving productivity through a clean and interactive interface.

This project combines **server-side Django development** with **client-side JavaScript features**, including AJAX-based task updates and frontend API fetching for dynamic content.

---

## Project Overview

ToDoList is designed as a personal productivity system where users can create and organise tasks, assign categories, monitor progress, and interact with a responsive dashboard.

The project was built with a focus on:
- clear task management workflow
- practical dashboard features
- client-side interactivity
- accessibility improvements
- sustainability and performance refinement

The application supports both traditional server-rendered functionality and modern frontend behaviour such as asynchronous updates and external API integration.

---

## Main Features

### User Authentication
- User registration
- User login
- User logout
- Session-based personalised dashboard

### Task Management
- Create new tasks
- Edit existing tasks
- Delete tasks
- Mark tasks as completed or pending
- Assign tasks to categories
- Add optional descriptions and due dates

### Category Management
- Create custom categories
- Edit categories
- Delete categories
- Use categories to organise tasks more clearly

### Search, Filter, and Sort
- Search tasks by title
- Filter by category
- Filter by status
- Sort tasks using different options
- Reset filters quickly using the clear function

### Dashboard and Analytics
- Dashboard overview of user tasks
- Completed and pending task counts
- Completion rate summary
- Category-based task distribution
- Upcoming due task information
- Structured analytics layout for tracking progress

### JavaScript / AJAX Features
- AJAX-based task status toggle on the dashboard
- Task completion status updates without full page reload
- Dynamic DOM updates for smoother interaction
- Frontend API fetching for homepage content

### Dynamic API Features
- Live weather information for **London**
- Live weather information for **Glasgow**
- Compact **Glasgow weather widget** in the navigation bar
- Dynamic daily motivation quote section
- Weather conditions displayed with icons and descriptions

### Accessibility Improvements
- Skip link for keyboard navigation
- Focus styles for interactive elements
- Improved heading hierarchy
- Better colour contrast in key sections
- Clearer form guidance and labels

### Sustainability / Performance Improvements
- Lighthouse-tested page refinement
- Reduced duplicated static resource loading
- Improved semantic metadata
- Lightweight interface structure
- Strong accessibility, SEO, and performance results after optimisation

---

## Technologies Used

### Backend
- Python
- Django 6
- SQLite

### Frontend
- HTML5
- CSS3
- Bootstrap 5
- JavaScript
- Fetch API
- AJAX-style asynchronous updates

### External APIs
- Open-Meteo API for live weather
- Quotes API for dynamic motivational content

### Deployment
- PythonAnywhere

---

## Project Structure

```text
config/                  # Django project settings and configuration
tasks/                   # Main app for task management
tasks/templates/tasks/   # App-specific templates
templates/               # Shared templates (base.html, auth templates, etc.)
static/
  css/                   # Stylesheets
  js/                    # JavaScript logic
manage.py
requirements.txt
README.md
```

---


## Main Functional Areas
### Authentication
Users can register, log in, and log out securely using Django’s authentication system.
### Task Management
Users can:
- add tasks
- edit tasks
- delete tasks
- assign categories
- set due dates
- change completion status
### Search, Filter, and Sort
The dashboard supports task discovery and organisation through:
- keyword search
- category filtering
- status filtering
- sorting controls
### AJAX Task Status Update
The completion status of a task can be changed directly from the dashboard without refreshing the whole page. This is implemented using JavaScript and asynchronous requests, improving responsiveness and user experience.
### Frontend API Dynamic Content
The homepage includes client-side API fetching using JavaScript fetch:
- motivation quote loading
- weather data loading
- live Glasgow weather shown in the navbar
This demonstrates that the project does not rely only on Django views for content rendering.
### Analytics
The analytics page provides a structured overview of:
- total tasks
- completed tasks
- pending tasks
- completion rate
- category breakdown
- upcoming due task information
### Accessibility
The project includes several improvements to support usability and accessibility, including keyboard navigation support, semantic structure, clearer labels, and better visual contrast.

---


## User Interface Highlights
The interface is designed to remain simple and practical while still including modern dynamic features.
### Homepage
- Hero introduction section
- Daily motivation quote
- Live weather cards for London and Glasgow
- Weather icon and condition mapping
- Responsive layout
### Dashboard
- Search and filter panel
- Create task shortcut
- Task card layout
- AJAX completion toggle
- Clear separation of metadata and actions
### Navigation Bar
- Authentication controls
- Compact real-time Glasgow weather indicator
- Responsive top-level navigation
### Analytics Page
- Summary cards
- Structured progress display
- Performance-oriented layout
- Easy-to-read statistics

---


## Installation and Local Setup
### Clone the repository
```text
git clone https://github.com/Jayden203/ToDoList.git
cd ToDoList
```
### Create a virtual environment
```
python -m venv venv
```
### Activate the virtual environment
Windows
```
venv\Scripts\activate
```
macOS / Linux
```
source venv/bin/activate
```
### Install dependencies
```
pip install -r requirements.txt
```
### Apply migrations
```
python manage.py makemigrations
python manage.py migrate
```
### Create a superuser (optional)
```
python manage.py createsuperuser
```
### Run the development server
```
python manage.py runserver
```
Then open the site in your browser:
http://127.0.0.1:8000/

---


## Requirements
A typical requirements.txt for this project includes:
```
asgiref==3.11.1
Django==6.0.3
sqlparse==0.5.5
tzdata==2025.3
requests==2.32.5
whitenoise==6.12.0
```

---

## Running Tests
This project includes tests for core functionality such as:
- model behaviour
- protected page access
- task status toggling
- analytics page loading
### Run tests with:
```
python manage.py test
```

---


## Deployment
The project is intended to be deployable on PythonAnywhere.
Typical deployment process
- Clone the repository on PythonAnywhere
- Create and activate a virtual environment
- Install dependencies from requirements.txt
- Configure WSGI
- Configure static files
- Apply migrations
- Run collectstatic
- Reload the web application
### Example deployment commands
```
git clone <repo-url>
cd ToDoList
mkvirtualenv todolist-venv --python=/usr/bin/python3.13
workon todolist-venv
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

---


## Important deployment settings
- ALLOWED_HOSTS must include the deployed domain
- static files must be configured correctly
- whitenoise should be installed if used in middleware
- the WSGI file must point to config.settings

---


## Accessibility Summary
Several accessibility-focused improvements were included in the project:
- skip link for keyboard users
- visible focus states
- improved colour contrast
- corrected heading hierarchy
- better form guidance and labels
These changes were made to improve usability and align the interface with more accessible design practice.

---


## Sustainability / Lighthouse Summary
The project was refined using Lighthouse-style evaluation and iterative improvement.
Key optimisation actions
- improved contrast in weather cards and UI text
- corrected heading order
- added metadata such as page description
- reduced duplicated resource loading
- kept homepage dynamic features lightweight
### Result
The optimised version achieved very strong scores across:
- performance
- accessibility
- best practices
- SEO
This demonstrates that small but targeted frontend improvements can significantly strengthen overall quality.

---


## Example Dynamic Features
### AJAX Task Toggle
Users can update task completion status directly on the dashboard without refreshing the entire page.
### Frontend Weather Fetch
Weather information is fetched asynchronously from an external API and displayed dynamically.
### Navigation Weather Widget
A compact Glasgow weather status component is displayed in the top navigation bar and updated on page load.
### Motivation Quote Fetch
The homepage loads a quote asynchronously using JavaScript. Fallback logic can be used if the quote API is unavailable.

---


## Future Improvements
Possible future extensions for the project include:
- email reminders for due tasks
- AI-assisted task recommendations
- more advanced AJAX interactions
- richer analytics visualisations
- user preference settings
- theme switching / dark mode
- additional API-based productivity features

---


## Notes
This project was built as a coursework-style Django application and aims to demonstrate:
- practical backend development with Django
- structured frontend layout
- JavaScript-based interaction beyond plain server rendering
- accessible interface improvements
- sustainable and performance-conscious design choices

---


## Author
Yibo Cao
GitHub: https://github.com/Jayden203

---


## License
This repository is provided for educational and coursework purposes.
