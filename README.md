# CS-499

Computer Science Capstone project for AAC Rescue.

## Requirements

Docker Desktop

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

The browser may warn about the local self-signed certificate. Accept the warning to continue for local testing.\
\
A test admin account is loaded for now:  
Email: admin@aac.com  
Password: password  

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
