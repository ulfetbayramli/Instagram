# Instagram Follower and Following Scraper

This application allows users to retrieve follower and following information from their Instagram accounts. Users can log in to their account and add multiple Instagram accounts to fetch data from. The application uses Selenium to automate the login process and fetch the required information.

# Features
Login to Instagram accounts and securely store account credentials.
Add multiple Instagram accounts to fetch follower and following data.
Periodically update follower and following information every 1 hour using a Celery task scheduled with RabbitMQ.
View the fetched data in the application's dashboard.

# Usage
Create an account and log in to the application.
Add Instagram accounts by providing the username and password.
The application will automatically fetch follower and following data for the added Instagram accounts every 1 hour.
View the fetched data in the application's dashboard.

# Future Improvements
Here are some possible enhancements that could be made to the application:

Implement a user interface for managing Instagram accounts and viewing follower/following data.
Add error handling and logging to improve application stability.
Implement authentication mechanisms to ensure secure account management.
Explore alternative scraping methods for improved performance and reliability.
Provide options for exporting and analyzing the fetched data.
Allow users to customize the task scheduling intervals.
Feel free to contribute any of these improvements or come up with your own ideas!
