# Disaster-Management-System

#### 1. Project Overview

The Disaster Management System is a web-based application developed as part of the Information Technology Project Management (ITPM) academic project. The main purpose of the system is to provide a centralized platform for managing and communicating important information during disaster situations. The application allows users to report disaster incidents, view emergency alerts, access information about emergency shelters, and view available disaster response teams. Administrators can monitor incidents, publish and remove emergency alerts, update incident statuses, and monitor registered users.

## 2. Objectives

The primary objective of this project is to develop a simple and centralized disaster management platform that can support effective communication and coordination during emergency situations. The system aims to make disaster reporting easier for users and provide important emergency information in an organized manner. It also helps administrators monitor reported incidents and manage emergency alerts. The project demonstrates how information technology and project management concepts can be applied to address real-world disaster management challenges.

## 3. System Description

The system provides separate functionalities for normal users and administrators. Users can register themselves and log in to the application using their credentials. After logging in, users can access a dashboard containing information about reported incidents, emergency alerts, shelters, and response teams. Users can also report new disaster incidents by providing information such as the type of incident, location, severity, and description. The reported information is stored in the database and can be monitored by the administrator.

The administrator has additional privileges to monitor and manage disaster-related information. Through the administrative monitoring section, the administrator can view all reported incidents, registered users, and published emergency alerts. The administrator can create new emergency alerts to communicate important information to users. Published alerts can also be removed when they are no longer required. In addition, the administrator can update the status of reported incidents as Pending, In Progress, or Resolved.

## 4. Emergency Alerts

The emergency alert module is designed to provide users with important disaster-related warnings and instructions. Each alert can contain a title, message, severity level, location, and creation date. Administrators can publish alerts based on the situation and remove outdated alerts when necessary. This functionality helps ensure that users can access relevant emergency information through the system.

## 5. Incident Reporting

The incident reporting module allows users to report disaster situations through the web application. Users can provide the incident type, location, severity, and a detailed description of the situation. The system records the information along with the reporter's details and the time of reporting. Administrators can then monitor these incidents and update their status according to the progress of emergency response activities.

## 6. Emergency Shelters and Response Teams

The system provides information about emergency shelters that may be useful during disaster situations. Shelter information includes the shelter name, location, total capacity, and available capacity. The response-team module provides information about teams involved in emergency response activities, including their team name, type, location, and current status. These modules provide users with useful information that can support decision-making during emergencies.

## 7. User and Administrator Roles

The system consists of two main types of users: normal users and administrators. Normal users can register, log in, access the dashboard, report incidents, view alerts, view shelters, and view response teams. Administrators have additional access to the monitoring system, where they can manage emergency alerts, monitor incidents, update incident statuses, and view registered users. Role-based access control ensures that administrative functions are restricted to authorized administrators.

## 8. Technology Used

The application is developed using Python and Flask for the backend and application logic. SQLite is used as the database for storing user information, incident reports, emergency alerts, shelter information, and response-team details. HTML5 is used to structure the web pages, while CSS3 is used for designing and styling the user interface. Jinja2 templates are used to dynamically display information from the Flask application. Werkzeug is used for password hashing and authentication-related functionality.

## 9. Database

The system uses an SQLite database to manage the information required by the application. The major database tables include users, incidents, alerts, shelters, and response teams. The users table stores registration and role information, while the incidents table stores disaster reports. The alerts table stores emergency warnings and messages. The shelters table stores emergency shelter information, and the response teams table stores information about teams involved in disaster response activities.

## 10. Project Management

This project applies various concepts from Information Technology Project Management. Project planning includes identifying project activities, milestones, dependencies, and project duration. Network analysis techniques such as Activity-on-Node (AON), Activity-on-Arrow (AOA), Critical Path Method (CPM), PERT, Total Float, Free Float, and Independent Float are used for project scheduling and analysis. Risk management is also considered by identifying technical, scope, people, budget, external, and security risks and developing appropriate mitigation strategies.

## 11. Case Study Background

The development of the system is supported by disaster-management case studies, including the study of coastal Odisha and other disaster scenarios. These case studies helped in understanding the challenges associated with disaster preparedness, emergency communication, incident reporting, shelter management, and response coordination. The observations from the case studies were used to identify important requirements for the proposed Disaster Management System.

## 12. Security

The system implements basic security features such as user authentication, password hashing, session management, and role-based administrator access. Administrative routes are protected so that normal users cannot access administrative functions. Database queries use parameterized values to reduce the risk of SQL injection. Since the current application is an academic prototype, additional security measures such as environment-based secret keys, HTTPS, CSRF protection, and secure deployment configurations can be implemented for production use.

## 13. Installation and Execution

To run the project locally, Python should be installed on the system. After downloading or cloning the repository, the project directory can be opened in a terminal. A virtual environment can be created and activated, followed by installation of the required Python packages. The Flask application can then be started using the python app.py command. Once the application is running, it can be accessed through the local Flask server using http://127.0.0.1:5000/.

## 14. Project Structure

The project contains the main Flask application file along with HTML templates, static files, and the SQLite database. The app.py file contains the application logic, routes, authentication, database operations, incident management, alert management, shelter information, response-team information, and administrative monitoring functionality. The templates folder contains the HTML pages used by the application, while the static folder contains the CSS and other static resources.

## 15. Testing

The application can be tested using different functional test cases to verify its major features. These include user registration, login authentication, incident reporting, viewing incidents, creating emergency alerts, removing alerts, viewing shelters, viewing response teams, updating incident status, administrator authentication, and logout functionality. Testing helps ensure that the major modules work according to the expected requirements.

## 16. Limitations

The current system is developed primarily as an academic prototype and therefore has some limitations. It does not currently integrate live government disaster information, GPS-based tracking, SMS or email notification services, or real-time weather and cyclone data. The application also uses SQLite, which is suitable for a lightweight academic application but may not be appropriate for a large-scale production system with many concurrent users. The accuracy of disaster information also depends on the information entered into the system.

## 17. Future Scope

The Disaster Management System can be further enhanced by integrating real-time disaster information, interactive maps, GPS-based incident tracking, SMS and email notifications, weather and cyclone data, artificial intelligence-based disaster prediction, automatic incident severity classification, response-team assignment, shelter navigation, multilingual support, mobile application support, cloud-based databases, and advanced disaster analytics. These improvements could transform the current academic prototype into a more comprehensive disaster-response platform.

## 18. Conclusion

The Disaster Management System provides a centralized web-based platform for reporting and monitoring disaster incidents and communicating emergency information. The system combines user management, incident reporting, emergency alerts, shelter information, response-team information, and administrative monitoring into a single application. Through this project, various ITPM concepts such as project planning, scheduling, risk management, network analysis, and software implementation have been applied to a practical real-world problem. The current system provides a foundation that can be further enhanced with real-time data, advanced technologies, and additional emergency-response capabilities.

## 19. Academic Project

This project was developed as part of the Information Technology Project Management (ITPM) academic coursework. The project focuses on applying project management and software development concepts to the domain of disaster management and emergency response.
