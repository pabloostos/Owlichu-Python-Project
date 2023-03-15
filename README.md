# Python project: Owlichu - Create Your Own Word!

## Project Information

- Student: Pablo Ostos Bollmann
- Email: p.ostos@gmail.com
- Master: MCSBT (IE)
- Professor: Jose Luis García Hernández

## Project description

The project is an app that facilitates the addition of words to the dictionary, allowing users to invent new words and provide definitions for them. In addition to the main functionality, the app also includes a registration and login system, enabling users to create and manage their profiles. Users can view their created words and obtain a certification for each word they invent. Overall, the app provides an efficient and user-friendly platform for expanding and diversifying the English language lexicon.

## Technologies

- Python 3.9
- Flask 2.1.1
- SQLite 3
- HTML/CSS/JavaScript
- Bootstrap 5
- jQuery 3.6.0

## Installation

To run the application locally, you need to have Python 3.9 installed, and then follow these steps:

- Clone this repository: git clone https://github.com/yourusername/owlichu.git
- Create a virtual environment: python3 -m venv venv
- Activate the virtual environment: source venv/bin/activate (Unix) or venv\Scripts\activate (Windows)
- Initialize the database: flask init-db
- Start the application: flask run
- By default, the application runs on http://localhost:5000/. You can customize the settings in the config.py file.

## Credits
This application was created by Pablo Ostos Bollmann, as a project for Advanced Programming in Python. Special thanks to Professor Pepe García Hernández for his guidance and support throughout the development of this project.

## Technical details

| Route                       | Description                                                                                                                  |
| --------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| /                           | Main page of the web application where users can introduce a new word                                                        |
| /handle_word                | Checks word restrictions and redirects to the next step of giving the word a definition                                      |
| /handle_definition          | Handles the definition input by the user                                                                                     |
| /handle_owlichu_to_database | Stores the owlichu word and its definition submitted by a user into a database                                               |
| /congratulations            | Renders a template that displays a message of congratulations to the user for successfully creating a new word (owlichu)     |
| /certificate                | Generates a certificate that displays the user's name, email, the word they created, and its definition                      |
| /login                      | Renders the login page                                                                                                       |
| /sign_in                    | Handles user login                                                                                                           |
| /unauthorized               | Renders the "Unauthorized_Owlichu.html" template indicating that the user is not authorized to access the requested resource |
| /identification             | Loads the "Identification_Owlichu.html" template for users to log in or register                                             |
| /registration               | Displays the registration form template for users to create a new account                                                    |
| /register_user              | Handles user registration and inserts the user's information into the database                                               |
| /user_profile               | Displays the user's profile including their username, email, and the owlichus they have created                              |
| /signout                    | Signs the user out of the session and redirects them to the home page or the identification page                             |

- index(): This route loads the main page of the web application where users can introduce a new word. If the user is already logged in (checked by session), the Word_Owlichu.html page is rendered, otherwise the user is redirected to the identification page.

- handle_word(): The handle_word() route takes care of word restrictions and redirects to the next step of giving the word a definition. It checks for five restrictions:

  1. It can only be a word, no spaces in between
  2. Only lowercase letters are allowed
  3. The word cannot be longer than the longest word in the English dictionary: Pneumonoultramicroscopicsilicovolcanoconiosis
  4. The word should not exist in the current English dictionary (API is called to check)
  5. The word is considered invalid if it already exists in the Owlichu database. If a word already exists, the user is redirected to a page displaying the word's definition. If the word passes all the restrictions, the session variable 'owlichu' is set to the word, and the user is redirected to the definition page.

- handle_definition(): This route handles the definition input by the user. It checks if the definition satisfies the set restrictions and if it does, it saves the definition to the session and redirects the user to the next step, which is adding the word to the database.

- handle_owlichu_to_database(): This route is responsible for storing the owlichu word and its definition submitted by a user into a database. The data is obtained from the user session, and then an SQL query is executed to insert the data into a table in the database. Finally, the user is redirected to a congratulations page.

- congratulations(): This route renders a template that displays a message of congratulations to the user for successfully creating a new word (owlichu) along with some information about the word, such as the word itself, its definition, the date it was created, the user's username, and email.

- certificate(username, word): This route generates a certificate that displays the user's name, email, the word they created, and its definition. The certificate is generated using a HTML template called "Certification_Owlichu.html". The word and its definition are obtained from the session data, and the user's name and email are passed as parameters in the URL.

- login(): This route simply renders the login page for the user to input their login credentials.

- sign_in(): This route handles user login. It retrieves the username and password from the HTML form and searches for the user's information in the database. If the user exists and the password matches, it creates a session for the user and redirects them to the home page. Otherwise, it redirects the user to an unauthorized page.

- unauthorized(): This route handles the rendering of the "Unauthorized_Owlichu.html" template which is displayed when a user enters an incorrect username or password. The HTTP status code 403 is also returned, indicating that the user is not authorized to access the requested resource.

- indentification(): This route loads the "Identification_Owlichu.html" template, which allows users to choose between logging in and registering if they do not already have an account.

- registration(): This route displays the registration form template for users to create a new account.

- register_user(): This route handles user registration and inserts the user's information into the database. It first retrieves the user's registration information from an HTML form and then checks whether the entered password matches the repeated password. If the passwords don't match, the user is redirected to a page where they can try entering their password again. If the passwords match, the user's password is hashed, and a check is performed to see if the username and email are already in use. If either is in use, the user is redirected to a page where they can try entering their username or email again. Finally, if the username and email are not in use, the user's information is inserted into the database, and they are redirected to the login page.

- user_profile(): The user_profile() route handles displaying the user's profile, including their username, email, and the owlichus they have created. It first checks if the user is logged in by checking if their username is in the session. If the user is not logged in, it redirects them to the /identification route. Otherwise, it retrieves the owlichus created by the user from the database using a SQL query, and renders the User_Profile_Owlichu.html template with the user's information.

- sign_out(): This route signs the user out of the session and redirects them to the home page or the identification page depending on whether the user was logged in or not

## Version 2.0 improvements:

- Implement password reset functionality: Currently, if a user forgets their password, there is no way for them to reset it. Adding a password reset functionality where users can reset their password via email would be a useful feature.

- Implement a search functionality: Adding a search functionality would allow users to search for existing owlichus and their definitions, making it easier to find and learn about words that have already been created.

- Implement social media sharing: Adding social media sharing functionality would allow users to easily share owlichus they have created on their social media platforms, increasing the reach of the application and potentially attracting new users.

- Add user comments and ratings: Adding user comments and ratings would allow users to share their thoughts and opinions on owlichus that have been created, and provide feedback to other users.

- Add more gamification elements: Gamification elements, such as badges, levels, and leaderboards, would make the application more engaging and encourage users to create more owlichus and engage more with the community.

