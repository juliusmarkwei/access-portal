# Access Portal Backend build with <a href="https://www.django-rest-framework.org/" target="_blank">Django Rest Framework</a> and <a href="https://docs.celeryq.dev/en/stable/index.html" target="_blank"> Celery

<a href="https://www.django-rest-framework.org/" target="_blank">
    <img src="./static/assests/logo.jpg" height=240px width=100% >
</a>

## Overview

The Access Key Manager is a web application developed for Micro-Focus Inc. to manage access keys for their multi-tenant school management platform. Schools can use this application to purchase access keys to activate their accounts. This project involves building a key manager that includes user authentication, key management, and integration capabilities.

## Project Objective

Micro-Focus Inc., a software company, has built a school management platform that is multi-tenant. Various schools can set up on the platform as if it was built specifically for them. They have chosen to use an access key-based approach for monetization rather than integrating payment features directly into the software. This project aims to develop a web application that schools can use to purchase and manage access keys to activate their accounts.

## Major Features <svg xmlns="http://www.w3.org/2000/svg" height="20px" width="30px" fill="white" viewBox="0 0 576 512"><path d="M0 80C0 53.5 21.5 32 48 32h96c26.5 0 48 21.5 48 48V96H384V80c0-26.5 21.5-48 48-48h96c26.5 0 48 21.5 48 48v96c0 26.5-21.5 48-48 48H432c-26.5 0-48-21.5-48-48V160H192v16c0 1.7-.1 3.4-.3 5L272 288h96c26.5 0 48 21.5 48 48v96c0 26.5-21.5 48-48 48H272c-26.5 0-48-21.5-48-48V336c0-1.7 .1-3.4 .3-5L144 224H48c-26.5 0-48-21.5-48-48V80z"/></svg>

### School IT Personnel <svg xmlns="http://www.w3.org/2000/svg" height="20px" width="30px" fill="white"  viewBox="0 0 640 512"><path d="M320 32c-8.1 0-16.1 1.4-23.7 4.1L15.8 137.4C6.3 140.9 0 149.9 0 160s6.3 19.1 15.8 22.6l57.9 20.9C57.3 229.3 48 259.8 48 291.9v28.1c0 28.4-10.8 57.7-22.3 80.8c-6.5 13-13.9 25.8-22.5 37.6C0 442.7-.9 448.3 .9 453.4s6 8.9 11.2 10.2l64 16c4.2 1.1 8.7 .3 12.4-2s6.3-6.1 7.1-10.4c8.6-42.8 4.3-81.2-2.1-108.7C90.3 344.3 86 329.8 80 316.5V291.9c0-30.2 10.2-58.7 27.9-81.5c12.9-15.5 29.6-28 49.2-35.7l157-61.7c8.2-3.2 17.5 .8 20.7 9s-.8 17.5-9 20.7l-157 61.7c-12.4 4.9-23.3 12.4-32.2 21.6l159.6 57.6c7.6 2.7 15.6 4.1 23.7 4.1s16.1-1.4 23.7-4.1L624.2 182.6c9.5-3.4 15.8-12.5 15.8-22.6s-6.3-19.1-15.8-22.6L343.7 36.1C336.1 33.4 328.1 32 320 32zM128 408c0 35.3 86 72 192 72s192-36.7 192-72L496.7 262.6 354.5 314c-11.1 4-22.8 6-34.5 6s-23.5-2-34.5-6L143.3 262.6 128 408z"/></svg>

1. **Signup & Login**: School IT personnel is able to sign up and log in with an email and password. Account verification and a reset password feature to recover lost passwords is included.
2. **Access Key Management**: Users is able to see a list of all access keys granted: active, expired, or revoked.
3. **Key Details**: For each access key, users is able to see the status, date of procurement, and expiry date.
4. **Key Constraints**: Users should not be able to obtain a new key if an active key is already assigned. Only one key can be active at a time.

### Micro-Focus Admin <svg xmlns="http://www.w3.org/2000/svg" height="20px" width="30px" fill="white" viewBox="0 0 448 512"><path d="M96 128a128 128 0 1 0 256 0A128 128 0 1 0 96 128zm94.5 200.2l18.6 31L175.8 483.1l-36-146.9c-2-8.1-9.8-13.4-17.9-11.3C51.9 342.4 0 405.8 0 481.3c0 17 13.8 30.7 30.7 30.7H162.5c0 0 0 0 .1 0H168 280h5.5c0 0 0 0 .1 0H417.3c17 0 30.7-13.8 30.7-30.7c0-75.5-51.9-138.9-121.9-156.4c-8.1-2-15.9 3.3-17.9 11.3l-36 146.9L238.9 359.2l18.6-31c6.4-10.7-1.3-24.2-13.7-24.2H224 204.3c-12.4 0-20.1 13.6-13.7 24.2z"/></svg>

1. **Admin Login**: Admins is able to log in with an email and password.
2. **Manual Key Revocation**: Admins is able to manually revoke an access key.
3. **Key Overview**: Admins is able to see all keys generated on the platform, including their status, date of procurement, and expiry date.
4. **Integration Endpoint**: Admins is able to access an endpoint that, given a school email, returns the status and details of the active key if any, or a 404 status if no active key is found. This allows integration with the school management software.

## Additions (top-ups)

1. School IT Personnel's key created must be activated by admin. Admins are notified via email if a key is created.
2. When status of a key changes, School IT Personnels are alerted via email by a custome mail template.

The project was inspired by the need for a robust and efficient way to manage access keys for a multi-tenant school management platform. Every aspect of this project required extensive research and careful planning to ensure seamless integration and functionality. The activities involved in this project are as follows:

1. Database model (table) development and configurations
2. Writing the various API views for all the neccessary methods of each view
3. Admin panel management configurations.
4. Adding all the neccesary URL endpoints to for all the various views and thier methods. Not forgetting the admin panel too.
5. Writing tests for all the views and thier methods. I also used Postman for testing as well.
6. Including a <a href="" target="_blank">documentation</a> for the project API through a library called <a href="https://drf-spectacular.readthedocs.io/en/latest/index.html" target="_blank">drf-spectacular</a> by <a href="https://www.openapis.org/" target="_blank">OpenAPI Initiative</a>.
7. Deployment of the REST API to <a href="https://www.heroku.com/" target="_blank">heroku</a>

## Image of the Browsable API

<a href="" target="_blank" title="Visit live">
    <img src="./static/assests/image of api.png" height="450px" width="100%" >
</a>

## Technologies utilized in developing the system

1. <a href="https://www.django-rest-framework.org/" target="_blank">**Django rest Framework**</a> for handling API views, and routes.
2. <a href="https://docs.celeryq.dev/en/stable/index.html#" target="_blank">**Celery**</a> was utilized for managing and executing asynchronous background tasks, ensuring that long-running processes do not block the main application.
3. <a href="" target="_blank">**Celery Beat**</a> was employed as a scheduler to automate the execution of periodic tasks, enabling tasks to run at defined intervals without manual intervention.
4. <a href="https://redis.io/" target="_blank">**Redis**</a> as a message broker for Celery to manage and schedule background tasks.
5. <a href="https://www.postgresql.org/" target="_blank">**Postgres Database**</a> as the primary database for storing application data securely and efficiently.
6. <a href="https://drf-spectacular.readthedocs.io/en/latest/index.html" target="_blank">**DRF Spectacular**</a> for generating and maintaining OpenAPI documentation for the Django REST Framework API.

## Frontend technoloies used

1. <a href="https://nextjs.org/" target="_blank">**Next.js**</a> for building the frontend, providing server-side rendering and static site generation for a seamless user experience.
2. <a href="https://nextjs.org/" target="_blank">**Vercel**</a> was used host the frontend application, ensuring fast and reliable hosting with seamless integration for continuous deployment.

## Images of the Frontend

<h3>1. Admin View</h3>
<hr/>
<a href="" target="_blank" title="Admin panel"> 
<img src="./static//assests/admin panel.png" width="100%" height="360px"></img>
</a>
<br/>
<h3>2. School IT Personnel View</h3>
<hr/>
<a href="" target="_blank" title="School IT Personnel View"> 
<img src="./static//assests/school IT personnel page.png" width="100%" height="360px"></img>
</a>
<br/><br/>

-   Frontend reposotory can be found <a href="https://github.com/juliusmarkwei/access-portal-fe" target="_blank" title="frontend github repo"> <strong>`here`</strong><svg xmlns="http://www.w3.org/2000/svg" height="12px" width="30px" fill="red" viewBox="0 0 576 512"><path d="M64 0C28.7 0 0 28.7 0 64V352c0 35.3 28.7 64 64 64H240l-10.7 32H160c-17.7 0-32 14.3-32 32s14.3 32 32 32H416c17.7 0 32-14.3 32-32s-14.3-32-32-32H346.7L336 416H512c35.3 0 64-28.7 64-64V64c0-35.3-28.7-64-64-64H64zM512 64V288H64V64H512z"/></svg></a>

## Prerequisites

```
    python -> 3.10
    django -> 5.0.4
    djanforestframework -> 3.15.1
    celery -> 5.4.0
    redis -> 5.0.4
```

## Installation

1. #### Clone this repository

```
    git clone https://github.com/juliusmarkwei/access-portal.git
    cd access-portal/
```

2. #### Install all the neccessary packages/dependencies

```
    pip install -r requirements.txt
```

3. #### Environment Variables

-   Create a <strong>`.env`</strong> preferrably inside the root directory <strong>access-portal/</strong>. Inside the <strong>.env</strong> add a SECRET_KEY and your database configurations of the database of your choice. You can generate a <strong>`SECRET_KEY`</strong> using the following code snippet:

```
    from django.core.management.utils import get_random_secret_key
    print(get_random_secret_key())
```

-   Check the complete list of the <strong>`.env`</strong> file content <a href="https://textdoc.co/QYoKIEHRc0wF84MG" target="_blank">here</a>. It should look like the variables below:

```
    SECRET_KEY=your_secret_key_here
    DB_HOST=your_db_host
    DB_USER=your_db_user
    DB_PASSWORD=your_db_password
    DB_NAME=your_db_name
    DB_PORT=your_db_port
    DB_ENGINE=your_db_engine
```

4. In the root directory of the project, create a superuser to manage all the users of the application. be sure python is installed before you proceed with this stage.

```
    python3 manage createsuperuser
```

5. #### Run the program with the following command

```
    python3 manage runserver
```

## Get Involved

I welcome contributions and participation from the community to help make this backend API even better! Whether you're looking to fix bugs, add new features, or improve documentation, your help is greatly appreciated. Here's how you can get involved:

### Reporting Issues 🚩

If you encounter any bugs or issues, please report them using the <a href="https://github.com/juliusmarkwei/ecommerce-backend/issues"> Issues</a> section of my GitHub repository. When reporting issues, please include:

-   A clear and descriptive title.
-   A detailed description of the problem, including steps to reproduce it.
-   Any relevant logs or error messages.
    Your environment details (e.g., Django version, DRF version, database, etc.).

### Contributing Code 💁🏼

I love receiving pull requests from the community! If you have an improvement or a new feature you'd like to add, please feel free to do so 👍
