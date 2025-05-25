# Real-Time Chat Application

## Description

A simple real-time chat application built with Python, featuring a FastAPI WebSocket backend and a Flet frontend. This allows for multi-platform deployment (desktop and potentially web).

## Features

- Real-time messaging between connected clients.
- FastAPI backend for handling WebSocket connections and message broadcasting.
- Flet frontend for a reactive user interface.
- Multi-platform compatibility thanks to Flet.

## Technologies Used

- **Backend**:
    - Python 3.x
    - FastAPI (for WebSocket handling and API)
    - Uvicorn (ASGI server to run FastAPI)
    - WebSockets
- **Frontend**:
    - Python 3.x
    - Flet (for the GUI)
- **General**:
    - `requirements.txt` for managing dependencies.

## Prerequisites

- Python 3.7+
- Pip (Python package installer)

## Setup and Installation

1.  **Clone the repository (if you haven't already):**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**
    -   On Windows:
        ```bash
        venv\Scripts\activate
        ```
    -   On macOS and Linux:
        ```bash
        source venv/bin/activate
        ```

4.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

You need to run the backend and frontend separately.

1.  **Run the Backend:**
    Open a terminal, navigate to the project root, and run:
    ```bash
    uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
    ```
    The backend server will start, typically at `http://localhost:8000`. The `--reload` flag enables auto-reloading on code changes.

2.  **Run the Frontend:**
    Open another terminal, navigate to the project root, ensure your virtual environment is activated, and run:
    ```bash
    python frontend/main.py
    ```
    The Flet application window should open.

## Project Structure

```
.
├── backend/
│   └── main.py         # FastAPI backend application
├── frontend/
│   └── main.py         # Flet frontend application
├── .gitignore          # Specifies intentionally untracked files that Git should ignore
├── README.md           # This file
└── requirements.txt    # Project dependencies
```

## Future Improvements

-   **Add Unit and Integration Tests**: Implement tests for both backend and frontend logic.
-   **User Identification**: Allow users to set usernames instead of generic "You" and "Other".
-   **Persistent Storage**: Implement message history storage (e.g., using a database).
-   **Error Handling**: More sophisticated error display and handling on the frontend.
-   **UI Enhancements**: Improve the overall look and feel of the chat interface.
-   **Configuration**: Make backend/frontend URLs and ports configurable via environment variables or a settings file.
-   **Containerization**: Add Dockerfile for easier deployment.
```
