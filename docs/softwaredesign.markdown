---
layout: default
title: Software Design and Engineering
permalink: /softwaredesign/
---
{% include nav.html %}

## Software Design and Engineering
[Github Project Link]("https://github.com/steelcd/CS-499/tree/module3-software-engineering")

For this enhancement, I focused on turning the original AAC Rescue dashboard into a more complete full-stack application. The original project worked as a Python Dash dashboard connected to MongoDB, but it was mainly focused on displaying and filtering shelter data. For the capstone, I wanted to keep that original dashboard intact while building a stronger application structure around it.

The biggest change was adding an Express.js application layer. Express now acts as the main entry point for the app and handles routing, the login flow, API requests, static pages, and proxying to the Dash dashboard. I also split the server-side code into separate areas for routes, controllers, services, middleware, views, and API logic. This makes the project easier to follow because each part has a more specific job instead of having everything handled in one place.

I also added a Vue.js admin interface for managing animal records. This gives the project a dedicated area for CRUD operations instead of only viewing records through the dashboard. The admin view can display animal data from the API and includes create, update, and delete workflows. I created a reusable animal form component so the create and update pages can share the same fields and input structure instead of duplicating the form code.

Security and deployment were also part of this enhancement. I added a basic authentication structure using Express sessions, with middleware to protect routes that should only be available after login. The current login uses a stubbed user for now, but the code is organized so it can later be replaced with database-backed users and hashed passwords. I also added NGINX as a reverse proxy with HTTPS using a local self-signed certificate, which lets the project demonstrate encrypted communication in the Docker environment. Overall, this enhancement makes the app easier to maintain, easier to expand, and closer to the structure of a real full-stack application.