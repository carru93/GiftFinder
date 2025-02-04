# Gift Finder - README

![py](http://ForTheBadge.com/images/badges/made-with-python.svg)
![love](http://ForTheBadge.com/images/badges/built-with-love.svg)

## Overview

**Gift Finder** is a Django application designed to help users find and recommend gifts. The app offers a range of social features, such as following other users and viewing their wishlists (if public), and a search engine to identify gifts based on various filters like age, gender, origin, and hobbies. Additionally, it includes functionalities like reviewing gifts, interacting through a forum, real-time chat between friends, and a comprehensive notification system to keep users updated on interactions related to their activities.

This document provides all the instructions to install, configure, and run the application, along with details on the libraries used, `Makefile` commands, and guidelines for testing and maintaining the code.

## Main Features

- **Gift Search**: Search for gifts based on age, gender, location, and interests/hobbies + various sorting criteria
- **Public/Private Wishlist**: Users can make their wishlist public or private.
- **Social Features**: Follow other users to see their interests, wishlists, and hobbies.
- **Suggested Gifts**: The app suggests gifts that fit the logged-in user, avoiding gifts the user already owns.
- **Gift Creation**: Users can suggest and update gifts.
- **Gift Detail & Reviews**: Detailed gift pages where users can review gifts using a star system (1-5), including image uploads.
- **Upvote-Downvote Reviews**: Registered users can upvote or downvote reviews to highlight helpful feedback.
- **Forum**: Users can create and comment on posts to engage in discussions.
- **Moderators in Forum**: Moderators have the ability to delete posts or comments to maintain community standards.
- **Real-Time Chat**: Chat functionality between friends using Django Channels.
- **Notifications**: Each user has a notification box receiving updates on interactions with their resources (gifts, reviews, posts).
- **Saved Searches & Notifications**: Users can subscribe to specific searches and receive notifications when new gifts matching those searches are added.
- **Email Notifications Settings**: Users can choose whether to receive notifications via email in their user settings.

## Architecture and Technologies

- **Django 5.0.7**: Main web framework.
- **Python 3**: Programming language.
- **SQLite**: Database.
- **Crispy Forms with Tailwind**: For consistent and responsive forms.
- **django-compressor**: To compress and manage static files.
- **dal (Django Autocomplete Light)**: For autocomplete fields (e.g., hobbies).
- **TailwindCSS**: For modern and responsive page styling.
- **Font Awesome**: Icons for enriching the interface.
- **Django Messages**: For user feedback.
- **Django Channels**: For real-time chat functionality.
- **Daphne**: ASGI server for handling real-time communication.
- **django-decouple**: To manage environment variables via `.env` files.

## Project Structure

- `users/`: Handles user management, profiles, following, public wishlist, and user settings.
- `gifts/`: Manages gifts, including creation, editing, suggestions, reviews, and search filters.
- `forum/`: Forum section for writing messages, comments, and social interactions, including moderator functionalities.
- `hobbies/`: Handles hobbies as a model with autocomplete functionality.
- `chat/`: Manages real-time chat functionality between friends.
- `pages/`: Static pages or simple views (e.g., home).
- `management/`: Handles scripts and commands

Templates are organized in their respective directories with some partials (`partials/`).

## Requirements

- **Python 3.x**
- **pip** (for Python package installation)
- **Node.js and npm** (for TailwindCSS and other frontend dependencies)
- **Git** (recommended for repository management)
- **SQLite** (default DB, no additional configuration required)

## Installation and Setup

1. **Clone the repository:**

   ```bash
   git clone git@github.com:carru93/GiftFinder.git
   cd GiftFinder
   ```

2. **Create a virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Python dependencies:**

   ```bash
   make install
   ```

   The `make install` command runs `pip install -r requirements.txt` and `pre-commit install`.

4. **Install Node.js dependencies:** Ensure `node` and `npm` are installed.
   Run:

   ```bash
   npm install
   ```

5. **Compile CSS with Tailwind:**

   ```bash
   make compile-css
   ```

   This runs TailwindCSS and generates `output.css` from `input.css`.

6. **Initialize the database and load initial data:**

   ```bash
   make init-db
   ```

   This command runs migrations and loads initial data for categories and hobbies.

7. **Configure Environment Variables:**

   - Create a `.env` file in the project root.
   - Add necessary environment variables. For example:

     ```env
     EMAIL_HOST_USER = 'xxx'
     EMAIL_HOST_PASSWORD = 'xxx'
     SITE_URL = "http://localhost:8000"
     ```

8. **Start the application locally:**

   ```bash
   make start-dev
   ```

   This runs Django's development server and Tailwind watch in parallel.

9. **Seed** (optional)

   ```bash
   make seed
   ```

   This command will seed the database with some initial random data.

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
- `make seed`: Seeds the database with initial random data.

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

## Autocomplete with Django Autocomplete Light (dal/dal_select2)

For fields like `hobbies`, we use `dal` and `dal_select2` for intelligent autocompletion. Simply define widgets such as `ModelSelect2Multiple` in forms and ensure the autocomplete URL is properly configured.

## Real-Time Chat with Django Channels

The chat feature uses Django Channels and Daphne for handling WebSocket connections, allowing real-time communication between friends.

## Notifications System

Users receive notifications for interactions with their resources (gifts, reviews, posts) in a notification box. The notification system utilizes context processors and custom models to manage notifications efficiently.

## Moderation Features in Forum

Moderators can delete posts and comments in the forum to maintain community standards. This is managed via group permissions and custom mixins in class-based views.

## Sorting and Pagination

Gifts can be sorted by various criteria, with the default sorting by rating. Ratings are updated dynamically as new reviews are added. Pagination is implemented to enhance user navigation through gift listings.

## Upvote-Downvote System for Reviews

Registered users can upvote or downvote reviews, helping to surface the most helpful and relevant feedback.

## Saved Searches and Subscriptions

Users can subscribe to specific searches and receive notifications when new gifts matching their criteria are added.

## Email Notification Preferences

In user settings, users can choose whether to receive notifications via email, allowing personalized control over their notification preferences.

## Code Cleanliness

We use `pre-commit` to maintain consistent code style. You can run it manually with:

```bash
make polish
```

This runs configured checks (flake8, black, etc.) on all files.

## License

[MIT License](LICENSE)
