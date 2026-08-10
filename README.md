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

## Media Architecture & Folder Structure

```text
media/
├── hls/
│   └── <video_id>/
│       ├── 480p/       <-- index.m3u8 & segment_xxx.ts
│       ├── 720p/
│       └── 1080p/
├── thumbnails/          <-- video_<video_id>.jpg
└── videos/              <-- Original uploaded MP4 files
```



## Installation & Setup (Backend)

### Prerequisites

- [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)
- [Git](https://git-scm.com/)

### 1. Clone the Repository & Configure Environment Variables

Bash

```
mkdir videoflix_backend
cd videoflix_backend
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

| **Action**                     | **Command**                                                  |
| ------------------------------ | ------------------------------------------------------------ |
| **Stop containers**            | `docker compose down`                                        |
| **Reset containers & volumes** | `docker compose down -v`                                     |
| **View worker logs**           | `docker compose logs -f videoflix_worker`                    |
| **Make database migrations**   | `docker compose exec videoflix_backend python manage.py makemigrations` |

## License & Authors

Developed as part of the Videoflix project.