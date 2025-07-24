# Flask Blog

This is a simple Flask-based blog application that uses the GitHub API to create new posts. The application is set up for deployment on Vercel.

## Features

- Create new blog posts using a web form.
- Posts are saved as Markdown files in the `api/contents` directory.
- Uses the GitHub API to commit new posts to the repository.

## Running Locally

To run the application locally, you can use the `run.sh` script:

```bash
./run.sh
```

This will create a virtual environment, install the dependencies, and run the Flask application.

## Deployment

This application is configured for deployment on Vercel. The `vercel.json` file contains the necessary configuration.

## Environment Variables

To run the application, you will need to create a `.env` file in the root of the project. You can copy the `.env.example` file to create a new `.env` file:

```bash
cp .env.example .env
```

Then, you will need to fill in the following variables:

- `GHTOKEN`: A GitHub personal access token with the `repo` scope. You can create a new token in your GitHub developer settings.
- `REPO_OWNER`: Your GitHub username.
- `REPO_NAME`: The name of the repository where you want to store the blog posts.



