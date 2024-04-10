---
date: 2024-04-10T11:09:25.467957
author: AutoGPT <info@agpt.co>
---

# Prompt Refiner

To create a single API endpoint for refining LLM prompts using the OpenAI GPT4 API, follow these steps using our selected tech stack. First, ensure you have Python installed, as it's our primary programming language. With Python, use FastAPI to handle HTTP requests due to its simplicity and performance benefits for building APIs. FastAPI integrates seamlessly with Pydantic for request validation, making it a robust choice for our endpoint.

Next, integrate PostgreSQL for database solutions. Although this specific task might initially not require database interactions, having PostgreSQL set up ensures scalability for feature addition, such as logging users' requests or storing refined prompts for analysis. Use Prisma as the Object-Relational Mapping (ORM) tool, which simplifies interactions with the PostgreSQL database by allowing model definitions and queries in a language idiomatic to Python.

Here's a step-by-step guide to achieve the task:
1. Install the necessary libraries and tools: FastAPI, Uvicorn (ASGI server), Psycopg2 (PostgreSQL adapter), and Prisma.
2. Define a Pydantic model to validate incoming requests, ensuring they contain a string LLM prompt.
3. Create a FastAPI endpoint that accepts a POST request with the LLM prompt in JSON format.
4. Use the prompt refining instructions provided ('You are a prompt refiner. Use advanced prompt engineering techniques to refine the user's prompt.') to implement the logic for processing the user's prompt.
5. Call the OpenAI GPT4 API with the processed prompt, capturing the refined prompt in the response.
6. Return the refined prompt to the user in the response body.

Ensure to include error handling for bad requests and failures in calling the OpenAI GPT4 API. It's also wise to implement logging for request and response data for future analysis. This approach leverages our tech stack efficiently, creating a scalable and maintainable solution for refining LLM prompts.

## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'Prompt Refiner'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
