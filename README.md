# CS-499

Computer Science Capstone project for AAC Rescue.

## Project Overview

This project enhances the AAC Rescue animal shelter application as part of the SNHU CS-499 Computer Science Capstone portfolio. The original artifact was a Python Dash dashboard connected to MongoDB animal shelter data; this version expands it into a fuller Docker-based application with an Express.js server, a Vue admin interface, API-driven animal data management, rescue candidate scoring, authentication, authorization, and MongoDB-backed seed data.

The capstone portfolio describes the project across the required enhancement categories:

| Portfolio Page | Focus |
| --- | --- |
| [Portfolio Home](https://steelcd.github.io/CS-499/) | Overall capstone context and project purpose. |
| [Code Review](https://steelcd.github.io/CS-499/codereview/) | Review of the original implementation and planned improvements. |
| [Software Design and Engineering](https://steelcd.github.io/CS-499/softwaredesign/) | Full-stack structure, Express routing, Vue admin CRUD workflows, authentication scaffolding, and HTTPS reverse proxy setup. |
| [Algorithms and Data Structures](https://steelcd.github.io/CS-499/algorithms/) | Profile-driven rescue candidate scoring using MongoDB rescue profiles, weighted rules, and ranked API results. |
| [Databases](https://steelcd.github.io/CS-499/databases/) | MongoDB-backed users, bcrypt password hashes, roles, shelter claims, and controlled access to animal data. |
| [Original Project](https://github.com/steelcd/CS340) | Original AAC Rescue dashboard artifact used as the basis for enhancement. |

## Requirements

Docker Desktop

## Application Services

Docker Compose starts four services:

| Service | Purpose |
| --- | --- |
| `nginx` | HTTPS entry point for the application. |
| `nodejs` | Express application, server-rendered pages, API routes, authentication, and the built Vue admin app. |
| `dash` | Candidate dashboard served through the Express `/dashboard/` proxy. |
| `mongo` | MongoDB database seeded with animal, rescue profile, and development user data. |

## Setup

Clone the repository\
Create a `.env` file in the project root if one is not already present:

```env
MONGO_ROOT_USER=mongo_user
MONGO_ROOT_PASSWORD=mongo_password
MONGO_PORT=27017
NODE_PORT=3000
```

## Run

Start the application with Docker Compose:

```bash
docker compose up -d
```

After the containers start, open:

```text
https://127.0.0.1
```

The browser may warn about the local self-signed certificate. Accept the warning to continue for local testing.

## Routes

| Route | Description | Access |
| --- | --- | --- |
| `/login` | Login page. | Public |
| `/index` | Main application page. | Logged-in users |
| `/dashboard/` | Candidate dashboard. | Logged-in users |
| `/admin/` | Vue admin interface for animal records. | `admin` or `shelter_admin` |

The Admin navigation link is only shown to users with the `admin` or `shelter_admin` role. Users with the `shelter_admin` role can only view and manage animal records for shelters listed in their `shelter_claims`.

## Seed Users

The MongoDB seed data includes development and testing users in the `app_users` collection:

| Username | Password | Role | Shelter Claims |
| --- | --- | --- | --- |
| admin@aac.com | admin | admin | All |
| shelter1@aac.com | shelter1 | shelter_admin | Shelter 1 |
| user@aac.com | user | user | None |

These seeded users are only for development and testing. In production, this seeded information should not be used; the `app_users` collection would be replaced with production-managed user records.

## Seed Data

MongoDB is seeded during first container initialization with:

| Collection | Source |
| --- | --- |
| `animals` | `mongo/src/aac_shelter_outcomes.csv` |
| `rescue_profiles` | `mongo/src/rescue_profiles.json` |
| `app_users` | `mongo/src/app_users.json` |

Seed files are imported only when the MongoDB data volume is initialized. If seed data changes after the first run, remove the volumes and start again:

```bash
docker compose down -v
docker compose up -d --build
```

## Development Notes

The Vue admin app is built during the `nodejs` Docker image build and served under `/admin/`. Rebuild the `nodejs` image after changing files in `nodejs/src/app-admin`:

```bash
docker compose up -d --build nodejs nginx
```

## Stop

Stop the containers:

```bash
docker compose down
```

To remove the MongoDB data volumes and reseed from scratch:

```bash
docker compose down -v
```

## NGINX

Certificate is self signed and would not be used in production, a CA-Issued certificate would be used and the key wouldn't be committed to a repo.
