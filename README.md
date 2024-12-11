# Gift Finder - README

![py](http://ForTheBadge.com/images/badges/made-with-python.svg)
![love](http://ForTheBadge.com/images/badges/built-with-love.svg)

## Overview

**Gift Finder** is a Django application designed to help users find and recommend gifts. The app offers social features, such as following other users and viewing their wishlists (if public), and a search engine to identify gifts based on various filters (age, gender, origin, hobbies).

Here there are all the instructions to install, configure, and run the application, along with details on the libraries used, `Makefile` commands, and guidelines for testing and maintaining the code.

## Main Features

- **Gift search** based on age, gender, location, and interests/hobbies.
- **Public/Private wishlist**: users can make their wishlist public.
- **Social features**: follow other users to see their interests, wishlists, and hobbies.
- **Suggested gifts**: the app suggests some gifts that can fit the logged user, it also avoids suggesting gifts the user already owns.
- **Gift creation**: users can suggest and update gifts.
- **Forum**: users can talk to each other creating and commenting posts.

## Architecture and Technologies

- **Django 5.0.7**: Main web framework.
- **Python 3**: Programming language.
- **SQLite**: Database.
- **Crispy Forms with Tailwind**: For consistent and responsive forms.
- **django-compressor**: To compress and manage static files.
- **dal (Django Autocomplete Light)**: For autocomplete fields (e.g., hobbies).
- **tailwindcss**: For modern and responsive page styling.
- **Font Awesome**: Icons for enriching the interface.
- **Django Messages**: For user feedback.

## Project Structure

- `users/`: Handles user management, profiles, following, public wishlist, and user settings.
- `gifts/`: Manages gifts, including creation, editing, suggestions, and search filters.
- `forum/`: Forum section for writing messages, comments, and social interactions.
- `hobbies/`: Handles hobbies as a model with autocomplete functionality.
- `pages/`: Static pages or simple views (e.g., home).

Templates are organized in their respective directories (`pages/templates/pages`, `gifts/templates/gifts`, `forum/templates/forum`, `users/templates/users`) with some partials (`partials/`).

## Requirements

- **Python 3.x**
- **pip** (for Python package installation)
- **Node.js and npm** (for TailwindCSS)
- **Git** (recommended for repository management)
- **SQLite** (default DB, no additional configuration required)

## Installation and Setup

1.  **Clone the repository:**

    ```bash
    git clone git@github.com:carru93/GiftFinder.git
    cd GiftFinder
    ```

2.  **Create a virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Python dependencies:**

    ```bash
    make install
    ```

    The `make install` command runs `pip install -r requirements.txt` and `pre-commit install`.

4.  **Install Node.js dependencies:** Ensure `node` and `npm` are installed.
    Run:

    ```bash
    npm install
    ```

5.  **Compile CSS with Tailwind:**

    ```bash
    make compile-css
    ```

    This runs TailwindCSS and generates `output.css` from `input.css`.

6.  **Initialize the database and load initial data:**

    ```bash
    make init-db
    ```

    This command runs migrations and loads initial data for categories and hobbies.

7. **Start the application locally**

    ```bash
    make start-dev
    ```

## Makefile Commands

The `Makefile` provides shortcuts for common operations:

- `make install`: Installs dependencies from `requirements.txt` and sets up pre-commit.
- `make test`: Runs Django tests (`python3 manage.py test`).
- `make compile-css`: Compiles CSS with Tailwind.
- `make watch-css`: Starts Tailwind in watch mode to recompile CSS automatically on changes.
- `make clear-css`: Removes the `output.css` file.
- `make start-dev`: Runs Django's development server and Tailwind watch in parallel.
  Press Ctrl+C to stop both.
- `make polish`: Runs pre-commit on all files.
- `make init-db`: Initializes the DB, applies migrations, and loads initial data.

## Running in Development

To launch the development server and see real-time changes (including CSS via Tailwind), run:

```bash
make start-dev
```

This starts `python3 manage.py runserver` and `make watch-css` in parallel.

Open [http://localhost:8000](http://localhost:8000) to view the app.

## Testing

Run tests with:

```bash
make test
```

## Django Messages Configuration

Messages are configured to provide user feedback. In `base.html`, containers for messages are defined. Messages appear at the top-right corner and automatically disappear after a few seconds (or can be manually closed).

## Crispy Forms & Tailwind

The project uses `crispy_forms` and `crispy_tailwind` for uniform and appealing forms. Forms use `FormHelper` and `Layout` to arrange fields into columns, add buttons, and manage labels and CSS classes.

## Autocomplete with django-autocomplete-light (dal/dal_select2)

For fields like `hobbies`, we use `dal` and `dal_select2` for intelligent autocompletion. Simply define widgets such as `ModelSelect2Multiple` in forms and ensure the autocomplete URL is properly configured.

## Code Cleanliness

We use `pre-commit` to maintain consistent code style. You can run it manually with:

```bash
make polish
```

This runs configured checks (flake8, black, etc.) on all files.
