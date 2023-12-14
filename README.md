# DejaView


## Introduction

DejaView is a Django-based platform that allows clients to upload recordings of live events/shows, which users can then pay to watch. Clients have a dedicated page with videos, merchandise, and announcements of upcoming live events. The home page features recently uploaded videos, popular videos, from the clients.

## Installation

To set up DejaView on your local machine, follow these steps:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/viictoo/dejaView.git
   ```

2. **Navigate to the Project Directory:**
   ```bash
   cd dejaView
   ```

3. **Create a Virtual Environment:**
   ```bash
   python -m venv venv
   ```

4. **Activate the Virtual Environment:**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

5. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

6. **Apply Migrations:**
   ```bash
   python manage.py migrate
   ```

7. **Create Superuser (for Admin Access):**
   ```bash
   python manage.py createsuperuser
   ```

8. **Run the Development Server:**
   ```bash
   python manage.py runserver
   ```

9. **Access the Application:**
   Open your web browser and go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Usage

- **Homepage:**
  - The homepage displays recently uploaded videos, popular videos, and a list of clients.

- **User Registration and Login:**
  - Users can register and log in to access premium content.

- **Video Playback:**
  - Users can pay to watch videos securely through integrated payment gateways.
    
  ## Blog
  An article by the developer on this project can be accessed at [My Blog](https://vlogs.hashnode.dev/everything-you-need-to-know-about-setting-up-a-paid-video-on-demand-streaming-platform)
  

## Contributing

Contributions are welcome! To contribute to DejaView, follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature-name`.
3. Make your changes and commit them: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature/your-feature-name`.
5. Submit a pull request.

## Related Projects

- [Django Official Documentation](https://docs.djangoproject.com/)
- [Django Rest Framework](https://www.django-rest-framework.org/)
- [Mpesa API Documentation](https://daraja.safaricom.com/api)
- [Bootstrap](https://getbootstrap.com/)

## Licensing

This project is licensed under the [MIT License](LICENSE).

---
