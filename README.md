# Videoflix Backend

A high-performance video streaming backend platform built with **Django**, **Django REST Framework**, **Redis**, and **FFmpeg**. The project handles asynchronous video processing, automatic thumbnail generation, and multi-resolution HLS stream preparation.

---

## Features

* **HLS Video Streaming**: Automatic conversion of uploaded MP4 videos into HLS playlists (`index.m3u8` & `.ts` segments) across multiple resolutions.
* **Asynchronous Task Processing**: Video conversion runs in the background using **Django-RQ** & **Redis**, keeping the main application responsive.
* **Automatic Thumbnail Extraction**: FFmpeg automatically extracts a JPEG preview image at 00:00:01 upon video upload.
* **HTTP 206 Partial Content Streaming**: Supports direct MP4 video streaming with Range Requests (enabling scrubbing/seeking).
* **Django Admin Integration**: Custom admin upload form featuring a real-time progress bar built with Vanilla JS.
* **Automatic File Cleanup**: A custom Django `post_delete` signal removes all associated media files and HLS folders from the filesystem when a video is deleted.
* **Dockerized Infrastructure**: Seamless setup using Docker Compose for the Backend, RQ Worker, and Redis.

---

## Folder Structure & Media Architecture

```text
videoflix/
│
├── content/                        # Django App for Video Management & Streaming
│   ├── migrations/                 # Database Migration Files
│   ├── static/
│   │   └── content/
│   │       └── js/
│   │           └── upload_progress.js  # Custom Vanilla JS Admin Upload Progress Bar
│   ├── __init__.py
│   ├── admin.py                    # Custom Admin Configuration & Media Definitions
│   ├── apps.py
│   ├── models.py                   # Video Model & post_delete Cleanup Signals
│   ├── serializers.py              # DRF Serializers for Video Data
│   ├── tasks.py                    # FFmpeg HLS & Thumbnail Processing Tasks
│   ├── urls.py                     # API Routing for Video Endpoints
│   └── views.py                    # API Views (e.g., VideoStreamView, VideoListView)
│
├── media/                          # Uploaded & Generated Media Files (Git ignored)
│   ├── hls/                        # Generated HLS Streams
│   │   └── <video_id>/             # Subdirectory per Video ID
│   │       ├── 480p/               # index.m3u8 & segment_000.ts files
│   │       ├── 720p/
│   │       └── 1080p/
│   ├── thumbnails/                 # Extracted JPEG Previews (video_<video_id>.jpg)
│   └── videos/                     # Original Uploaded MP4 Source Files
│
├── static/                         # Collected Static Files (via collectstatic)
│
├── core/                           # Django Core Project Configuration
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py                 # Core Settings (MEDIA_ROOT, RQ_QUEUES, etc.)
│   ├── urls.py                     # Root URL Dispatcher
│   └── wsgi.py
│
├── .env                            # Environment Variables (SECRET_KEY, DEBUG, etc.)
├── .gitignore                      # Git Ignore Rules (media/, *.pyc, .env, etc.)
├── Dockerfile                      # Container Build Instructions for Backend & Worker
├── docker-compose.yml              # Services Orchestration (Backend, Worker, Redis)
├── manage.py                       # Django CLI Utility
├── README.md                       # Project Documentation
└── requirements.txt                # Python Dependencies (Django, djangorestframework, django-rq, Pillow, etc.)
```



## Installation & Setup (Backend, Windows)

### Prerequisites

- [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)
- [Git](https://github.com/Developer-Akademie-Backendkurs/material.videoflix-docker-files/blob/main/.env.template)

### 1. Clone the Repository & Configure Environment Variables

Bash

```
mkdir videoflix
cd videoflix
git clone https://github.com/alex202-sys/Videoflix.git .
```

Create a `.env` file in the root directory:

```python
cp .env.template .env
```

Enviroment in .env

```
DEBUG=True
SECRET_KEY=your_django_secret_key
ALLOWED_HOSTS=localhost,127.0.0.1
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

(Note: If your `SECRET_KEY` contains a `$`, escape it as `$$` for Docker Compose. If emails are output directly to the Docker terminal—using the console instead of SMTP!).*

### 2. Start the Docker Containers

Bash

```
docker compose up -d --build
```

### 3. Run Database Migrations & Create Superuser

Bash (you can use 'web' instead of 'videoflix_backend'.)

```
# Apply database migrations
docker compose exec videoflix_backend python manage.py migrate

# Create an administrative user
docker compose exec videoflix_backend python manage.py createsuperuser

# Collect static files (required for the admin upload progress bar)
docker compose exec videoflix_backend python manage.py collectstatic --noinput
```

The backend API is now running at `http://127.0.0.1:8000/`.

Access the Django Admin panel at `http://127.0.0.1:8000/admin/`.

## Frontend Installation

The corresponding frontend repository can be found here:

🔗 **[https://github.com/Developer-Akademie-Backendkurs/project.Videoflix](https://github.com/Developer-Akademie-Backendkurs/project.Videoflix)** 

Refer to the `README.md` in the frontend repository for local setup instructions and integration details.

The CORS in settings.py have already been adjusted to work with frontend port 5500 and backend port 8000. No additional adjustments are needed on the frontend and the backend.

## Useful Commands

| **Action**                                  | **Command**                                                  |
| ------------------------------------------- | ------------------------------------------------------------ |
| **Stop containers**                         | `docker compose down`                                        |
| **Reset containers & volumes**              | docker compose down -v`                                      |
| **View worker logs**<br />**View web logs** | `docker compose logs -f videoflix_worker`<br />`docker compose logs -f web` |
| **Make database migrations**                | `docker compose exec videoflix_backend python manage.py makemigrations` |

## License & Authors

Developed as part of the Videoflix project.