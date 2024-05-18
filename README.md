# Access Portal Backend build with <a href="https://www.django-rest-framework.org/" target="_blank">Django Rest Framework</a> and <a href="https://docs.celeryq.dev/en/stable/index.html" target="_blank"> Celery

<a href="https://www.django-rest-framework.org/" target="_blank">
    <img src="./static/assests/logo.jpg" height=200px width=100% >
</a>

## Overview

The Access Key Manager is a web application developed for Micro-Focus Inc. to manage access keys for their multi-tenant school management platform. Schools can use this application to purchase access keys to activate their accounts. This project involves building a key manager that includes user authentication, key management, and integration capabilities.

## Project Objective

Micro-Focus Inc., a software company, has built a school management platform that is multi-tenant. Various schools can set up on the platform as if it was built specifically for them. They have chosen to use an access key-based approach for monetization rather than integrating payment features directly into the software. This project aims to develop a web application that schools can use to purchase and manage access keys to activate their accounts.

## Features <svg xmlns="http://www.w3.org/2000/svg" height="20px" width="30px" fill="green" viewBox="0 0 576 512"><path d="M0 80C0 53.5 21.5 32 48 32h96c26.5 0 48 21.5 48 48V96H384V80c0-26.5 21.5-48 48-48h96c26.5 0 48 21.5 48 48v96c0 26.5-21.5 48-48 48H432c-26.5 0-48-21.5-48-48V160H192v16c0 1.7-.1 3.4-.3 5L272 288h96c26.5 0 48 21.5 48 48v96c0 26.5-21.5 48-48 48H272c-26.5 0-48-21.5-48-48V336c0-1.7 .1-3.4 .3-5L144 224H48c-26.5 0-48-21.5-48-48V80z"/></svg>

### School IT Personnel

1. **Signup & Login**: School IT personnel is able to sign up and log in with an email and password. Account verification and a reset password feature to recover lost passwords is included.
2. **Access Key Management**: Users is able to see a list of all access keys granted: active, expired, or revoked.
3. **Key Details**: For each access key, users is able to see the status, date of procurement, and expiry date.
4. **Key Constraints**: Users should not be able to obtain a new key if an active key is already assigned. Only one key can be active at a time.

### Micro-Focus Admin

1. **Admin Login**: Admins is able to log in with an email and password.
2. **Manual Key Revocation**: Admins is able to manually revoke an access key.
3. **Key Overview**: Admins is able to see all keys generated on the platform, including their status, date of procurement, and expiry date.
4. **Integration Endpoint**: Admins is able to access an endpoint that, given a school email, returns the status and details of the active key if any, or a 404 status if no active key is found. This allows integration with the school management software.

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
    <img src="./static/assests/image of api.png" height="350px" width="100%" >
</a>

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

-   Add the following line listed below to the <strong>`.env`</strong> file:

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

4. #### Access the Application

-   Once the application (container) is running, access the application running on port 8000 via http://localhost:8000.

## Get Involved

We welcome contributions and participation from the community to help make this e-commerce backend API even better! Whether you're looking to fix bugs, add new features, or improve documentation, your help is greatly appreciated. Here's how you can get involved:

### Reporting Issues 🚩

If you encounter any bugs or issues, please report them using the <a href="https://github.com/juliusmarkwei/ecommerce-backend/issues"> Issues</a> section of my GitHub repository. When reporting issues, please include:

-   A clear and descriptive title.
-   A detailed description of the problem, including steps to reproduce it.
-   Any relevant logs or error messages.
    Your environment details (e.g., Django version, DRF version, database, etc.).

### Contributing Code 💁🏼

I love receiving pull requests from the community! If you have an improvement or a new feature you'd like to add, please feel free to do so 👍
