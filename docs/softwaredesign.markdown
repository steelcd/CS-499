---
layout: default
title: Software Design and Engineering
permalink: /softwaredesign/
---

## Software Design and Engineering
[Github Project Link]("https://github.com/steelcd/CS-499/tree/module3-software-engineering")


For the software design and engineering enhancement, I expanded the original application into a more complete full-stack system. The project now separates responsibilities across multiple services, including an Express.js web application, a Vue.js admin interface, a Dash analytics dashboard, a MongoDB database, and an NGINX reverse proxy.

One major improvement was restructuring the Express application into clearer layers. Server-side routes, controllers, middleware, services, views, and API logic are separated by responsibility. This makes the application easier to maintain because authentication logic, route handling, database API operations, and rendered views are no longer concentrated in a single file.

I also added a REST-style API layer for working with animal records in MongoDB. The API supports create, read, update, and delete operations for animal data. This allows the application to separate data access from the user interface and supports both the Vue.js admin page and future application features.

The Vue.js admin interface provides a dedicated management area for animal records. It includes a data table view, create functionality, update functionality, and delete actions. A reusable animal form component is used for both creating and updating records, reducing duplicated code and making the interface easier to extend.

The application also includes a basic authentication and authorization structure. Express sessions are used to track logged-in users, and middleware protects routes that should only be available after login. The current authentication service uses temporary stubbed credentials, but it is structured so that it can later be replaced with database-backed users and hashed passwords.

To support secure communication, I added NGINX as a reverse proxy and configured HTTPS with a local self-signed certificate. This allows the application to demonstrate encrypted browser communication in a local Docker environment. In a production deployment, this certificate would be replaced with a certificate issued by a trusted certificate authority.

Docker Compose is used to run the application as a set of coordinated services. This improves portability because the project can be cloned and started with a standard Docker command. MongoDB data is stored in named Docker volumes so that data persists across container restarts.

Overall, these changes improve modularity, maintainability, security, and usability. The enhanced application demonstrates stronger software engineering practices by separating concerns, organizing the codebase into logical layers, supporting CRUD operations, adding authentication structure, and deploying the system through containerized services.