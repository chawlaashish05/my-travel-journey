# My Travel Journey
#### Video Demo:  https://youtu.be/La-WbNoNgTI
#### Description:
My Travel Journey is a web application designed to help users plan and manage their travel itineraries. Users can register, log in, and store their travel plans securely in a database. The application provides a user-friendly interface for adding, viewing, and managing travel plans.

## Project Structure
This project consists of several components including a Flask application (`app.py`), HTML templates, CSS stylesheets, JavaScript, and supporting Python scripts (`helpers.py`). Below is a detailed description of each file and its purpose:

### app.py
`app.py` is the main application file that contains the core logic of the Travel Journey website. It is built using Flask, a lightweight web framework for Python. The file includes routes for different functionalities such as registering, logging in, logging out, and managing travel plans.

**Routes**:
  - `/`: Home page, accessible to everyone, first page of the website.
  - `/home`: Home page, accessible only to logged-in users.
  - `/register`: Registration page for new users.
  - `/login`: Login page for existing users.
  - `/logout`: Logs out the current user and redirects to the index (`/`) page.
  - `/add_places`: Page to select a place that the user has already visited or wants to visit, along with the date of visit, accessible only to logged-in users.
  - `/my_places`: Page to view a table of already visited places or future visit plans with dates. Places are also marked on a map, accessible only to logged-in users.
  - `/notes`: Page to write specific notes for each added place. All notes are visible in a table, accessible only to logged-in users.

**Database Design (travel.db)**:
  - Utilizes SQLite through the CS50 SQL library.
  - `users` table stores user credentials, including the username and hashed password of each user.
  - `user_places` table stores the place names, dates, and the status of whether the user has visited the place or wants to visit it. Each entry is linked to a user via a foreign key relationship.
  - `user_notes` table stores the title and content of notes. Each entry is linked to a user via a foreign key relationship.

### helpers.py
`helpers.py` contains helper functions used throughout the application. It includes the `login_required` decorator to restrict access to certain routes only to logged-in users.

### HTML Templates
The HTML templates are located in the `templates` folder and are rendered by Flask to display the web pages. The main templates include:
- **layout.html**: The base template that includes the common structure for all pages.
- **index.html**: The home page displayed when a user opens the website and is not logged in.
- **register.html**: The registration page for new users.
- **login.html**: The login page for existing users.
- **home.html**: The home page displayed after a user logs in.
- **add_places.html**: The page where the user can choose a place they have visited or wish to visit. Using OpenStreetMap, they can add the name of a place and choose a date with a calendar.
- **my_places.html**: The page where the user can choose three options between all, visited, or to visit to see the related places in a table with the date. A map, created with leaflet, also shows the selected places with marked blue points.
- **notes.html**: The page to add user-specified notes. Users can add a title (e.g., the name of the place) and a text (e.g., something they want to do there), which is shown in a table with all their notes. This table is similar to the table in the `my_places.html` page and was created using bootstrap.

### CSS Stylesheets
The CSS stylesheets are located in the `static/css` folder. The main stylesheet is `styles.css`, which contains the styles for all the pages in the application. The CSS ensures a consistent and user-friendly design. The `static` folder also contains two images, `globe.jpg` and `map.jpg`, to ensure a special layout with a map background on every page and a globe icon in the header. The picture from the navigation bar is a image source and not in the folder.

## Design Choices
### Security
- **Password Hashing**: User passwords are hashed using Werkzeug’s security module before being stored in the database. This ensures that even if the database is compromised, the actual passwords are not exposed.
- **Session Management**: Flask-Session is used to manage user sessions securely. Session data is stored on the server side to prevent client-side tampering.

### Usability
- **Form Validation**: Both client-side (HTML5) and server-side validation are implemented to ensure that users provide the necessary information in the correct format.
- **User Feedback**: Flash messages provide feedback to users, guiding them to correct any mistakes (e.g., incorrect login credentials, missing form fields).

## Future Improvements
- **Enhanced Security**: Implement additional security features such as two-factor authentication (2FA) and CSRF protection.
- **Rich User Interface**: Enhance the UI with JavaScript for dynamic content updates and a more interactive experience.
- **Expanded Functionality**: Add features such as the ability to share travel plans with other users, integration with third-party travel services, and more detailed travel itineraries.

## Conclusion
The My Travel Journey project demonstrates a full-stack web application that integrates user authentication, database interactions, and a responsive user interface. By following best practices in web development and security, the application provides a robust and user-friendly platform for managing travel plans. The project structure and code organization facilitate maintainability and scalability for future enhancements.
