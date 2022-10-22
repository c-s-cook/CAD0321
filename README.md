
Cloud Foundry link:
        https://cad0321.us-south.cf.appdomain.cloud/djangoapp/


# Final Project Template

The final project for this course has several steps that you must complete. 
To give you an overview of the whole project, all the high-level steps are listed below. 
The project is then divided into several smaller labs that give the detailed instructions for each step. 
You must complete all the labs to successfully complete the project.

## Project Breakdown

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
1. ?  Create cloud functions to manage dealers and reviews
2. X  Create Django models and views to manage car model and car make
3. Create Django proxy services and views to integrate dealers, reviews, and cars together
        https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-CD0321EN-SkillsNetwork/labs/module_3_backend_services/3-instructional-labs-theia-django-proxy.md.html
 
**Add dynamic pages with Django templates**
1. Create a page that shows all the dealers
2. Create a page that show reviews for a selected dealer
3. Create a page that let's the end user add a review for a selected dealer

**Containerize your application**
1. Add deployment artifacts to your application
        https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-CD0321EN-SkillsNetwork/labs/module_5_containerize/1-instructional-labs-theia-containerize.md.html
2. Deploy your application
