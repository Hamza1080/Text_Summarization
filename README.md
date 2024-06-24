Make sure to have all required flask related libraries installed

# How to Run

1) pip install -r requirements.txt
2) export GEM_KEY= YOUR API KEY
3) source env/bin/activate
4) python3 app.py


#Flask Text Summarizer Web App
This Flask application allows users to register, log in, input text for summarization, and view summaries generated using Google's Generative AI. Users can also view their previously generated summaries on their dashboard.

# Features
* User registration and authentication
* Text input for summarization
* Dashboard to view saved summaries
  
# Technologies Used
* Flask
* SQLAlchemy (for database management)
* Flask-Login (for user session management)
* Google Generative AI (for text summarization)

# Usage
1) Run the application:
 python app.py
   
2) Access the application:
Open your web browser and go to http://localhost:5000

3) Register or log in:

If you're a new user, click on "Register" and fill out the registration form.
If you're an existing user, click on "Login" and enter your credentials.

4) Summarize text:

After logging in, you can input text in the provided form on the homepage.
Select the desired summary length and click "Summarize".
View the generated summary on the result page.
View dashboard:

Click on "Dashboard" to view all summaries you've generated.
Summaries are associated with your account and are saved in the database.
