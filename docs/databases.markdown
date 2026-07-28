---
layout: default
title: Databases
permalink: /databases/
---
{% include nav.html %}

## Databases
[Github Project Link](https://github.com/steelcd/CS-499/tree/module5-databases){:target="_blank"}

For this enhancement, I focused on the database changes needed to support authentication, authorization, and controlled access to the AAC Rescue application. Earlier enhancements had already added several database-related improvements, including MongoDB seed data, API-based CRUD operations, and rescue profile documents used by the scoring algorithm. The database enhancement completed the remaining user access work by replacing the hardcoded login with database-backed user records.

I added an `app_users` collection to store application users, password hashes, active status, roles, and shelter claims. The login process now queries MongoDB for an active user and validates the entered password against the stored hash. I originally started with Node’s built-in `crypto` library, but switched to `bcrypt` because it provided a cleaner pattern for hashing passwords and checking login attempts. This made the authentication code easier to understand while still supporting secure password storage.

The database enhancement also improved authorization. Users can now have roles such as admin, shelter admin, or user. The application checks those roles before allowing access to protected pages and routes. Shelter claims also allow a user to be associated with specific shelter records, which creates a better structure for managing access to animal data. This is important because different users may work in the same application but should not all have the same permissions.

The main database structures used in this enhancement are the animal records collection, rescue profile collection, and application user collection. Together, these collections support the main pieces of the system: animal data maintenance, rescue candidate scoring, and controlled user access. This improves the original artifact by moving user authentication and authorization into the database design instead of relying on a hardcoded account in the application code.

## Screenshots

### App User JSON

![App User seed records]({{ "/assets/images/app_user_json.png" | relative_url }})

### Shelter Login

![Login from shelter scoped user]({{ "/assets/images/shelter_login.png" | relative_url }})

### Scoped Shelter Admin Access

![Records filtered by shelter]({{ "/assets/images/scoped_shelter_access.png" | relative_url }})
