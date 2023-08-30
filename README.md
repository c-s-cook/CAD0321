# ABOUT
This is a project from my Full Stack Cloud Application Development certification, but **this is primarily a *backend* project**. (The frontend sure ain't purtty.)

**CLOUD FUNCTIONS**

This Django app uses Cloud Function (aka 'serverless' or 'Lambda') API calls which interface with a NoSQL database in order to:
- retrieve and dynamically generate the homepage list of Dealerships;
- retrieve and dynamically generate pages for individual dealership details & reviews
- post new dealership reviews from authenticated users

**WATSON NATURAL LANGUAGE UNDERSTANDING**

The app also utilizes the Watson NLU SDK to analyze the sentiment of each review that is submitted and correlate the results to how the review is displayed on the dealership details page.

**AUTHENTICATION / AUTHORIZATION**

The app uses an SQLite database with Django's built-in Admin site and functionality for authenticating and authorizing users. 




<br/><br/>

# INSTALLATION
1. Download & unzip
2. >  cd  [ directory name ]
3. Upload the starter data found in the './NoSQL' folder to a NoSQL database of your choice.
4. Create three Cloud Functions on the platform of your choice (refactor code as needed) and provide each necessary connection URLs & Keys to your database
5. Create a Free Tier instance of the Watson NLU service on IBM Cloud.
6. (Optional/Recommended:) create & activate a python Virtual Environment
7. >  cd server
8. > pip install -r requirements.txt
9. Add your API end-points and Keys to the .env file
10. > python manage.py runserver

...That should be enough to get the front-end up and running. 




<br/><br/><br/>


### PYTHON VIRTUAL ENVIRONMENT SETUP
On Windows, it may be necessary to modify the Execution Policy in your PowerShell/cmd prompt to allow bash scripts to be run. The below command will allow the current terminal session to do just that.

 > Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope Process

*** to make ***
> python -mvenv [name]

*** to activate ***
>.\[name]\Scripts\activate

*** to deactivate ***
> deactivate


<br/> <br/>
## DEPLOYMENT TUTS:
- https://stackabuse.com/deploying-django-apps-to-heroku-from-github/




<br><br>






## FINAL PROJECT REQUIREMENTS

The final project for this course had several steps that I had to complete. 
All the high-level steps are listed below. 



**Prework: Sign up for IBM Cloud account and create a Watson Natural language Understanding service**
1. X  Create an IBM cloud account if you don't have one already.
2. X  Create an instance of the Natural Language Understanding (NLU) service.

**Fork the project Github repository with a project then build and deploy the template project**
1. X  Fork the repository in your account
2. X  Clone the repository in the theia lab environment
3. X  Create static pages to finish the user stories
4. X  Deploy the application on IBM Cloud

**Add user management to the application**
1. X  Implement user management using the Django user authentication system.
2. X  Set up continuous integration and delivery

**Implement backend services**
1. X  Create cloud functions to manage dealers and reviews
2. X  Create Django models and views to manage car model and car make
3. Create Django proxy services and views to integrate dealers, reviews, and cars together
        https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-CD0321EN-SkillsNetwork/labs/module_3_backend_services/3-instructional-labs-theia-django-proxy.md.html
 
**Add dynamic pages with Django templates**
1. X Create a page that shows all the dealers
2. X Create a page that show reviews for a selected dealer
3. X Create a page that let's the end user add a review for a selected dealer

**Containerize your application**
1. X Add deployment artifacts to your application
        https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-CD0321EN-SkillsNetwork/labs/module_5_containerize/1-instructional-labs-theia-containerize.md.html
2. Deploy your application
