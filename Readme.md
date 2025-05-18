> [!IMPORTANT]
>The repository is only for learning. Do not use this code in production.

# Sprachbot
This project involves developing a voice bot using Azure services to create user accounts.
The bot will engage in natural language conversations to collect necessary user data, including personal, address, and contact information.
Successful implementation will demonstrate proficiency in cloud technologies, speech processing, and database integration.

## Structure

![Cloud Structure of Sprachbot](img/structure.png)

## Bot
TODO Describe used botframework

## Dashboard
The dashboard is build with React and Tailwind.
This dashboard provides a comprehensive overview of user data, featuring a detailed table with user information and a visual representation of user distribution across cities.  
It allows for efficient management and analysis of user-related data.  

## API
The API is a small Service written in Python using flask.
Need `AZURE_KEY_VAULT_URL` environment variable to the Key Value store of Azure.
The App Service need an enabled Identity

In the Key Value, store must provide the `Key Vault Certificate User` to the App Service.
The following Secrets are needed: 

  - `DATABASE-URL`: Contains the string for the connection to the database. (this contains user, password, URL, etc.)
  - `SECRET-KEY`: The Flask secret key is used to secure session data (sessions), to sign cookies and to protect against CSRF attacks.

## Database
The database is a mssql database on Azure.

TODO: Add Scheme

## Key Vault
Key Value was used by Azure.
The user must also be given the `Key Vault Data Access Administrator` role in the access control (IAM) in order to create secrets.