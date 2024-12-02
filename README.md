# DejaView


## Introduction

DejaView is a video streaming platform that empowers content creators to upload and monetize their media assets. Clients can set prices for videos, sell merchandise, and engage with their audience through announcements and events. The app also features a blog for entertainment news and reviews, while offering adaptive, secure streaming with HLS and encrypted media for a seamless viewing experience. Built with Django and Bootstrap, the platform combines ease of use with robust functionality for both creators and users.


## App Screenshots

<div style="overflow-x: auto; white-space: nowrap; padding: 10px 0;">
   <img src="https://github.com/viictoo/dejaView/blob/main/assets/webp/welcome.webp" alt="Welcome Screenshot" style="width: 300px; margin-right: 10px; display: inline-block;">
   <img src="https://github.com/viictoo/dejaView/blob/main/assets/webp/list-view.webp" alt="List View Screenshot" style="width: 300px; margin-right: 10px; display: inline-block;">
   <img src="https://github.com/viictoo/dejaView/blob/main/assets/webp/detail-view.webp" alt="Detail View Screenshot" style="width: 300px; margin-right: 10px; display: inline-block;">
   <img src="https://github.com/viictoo/dejaView/blob/main/assets/webp/create-new-user.webp" alt="Create New User Screenshot" style="width: 300px; margin-right: 10px; display: inline-block;">
   <img src="https://github.com/viictoo/dejaView/blob/main/assets/webp/search.webp" alt="Search Screenshot" style="width: 300px; margin-right: 10px; display: inline-block;">
   <img src="https://github.com/viictoo/dejaView/blob/main/assets/webp/pay-view.webp" alt="Pay View Screenshot" style="width: 300px; margin-right: 10px; display: inline-block;">
   <img src="https://github.com/viictoo/dejaView/blob/main/assets/webp/user-list-view.webp" alt="User List View Screenshot" style="width: 300px; margin-right: 10px; display: inline-block;">
   <img src="https://github.com/viictoo/dejaView/blob/main/assets/webp/blog-detail-view.webp" alt="Blog Detail View Screenshot" style="width: 300px; margin-right: 10px; display: inline-block;">
   <img src="https://github.com/viictoo/dejaView/blob/main/assets/webp/blog-list-view.webp" alt="Blog List View Screenshot" style="width: 300px; margin-right: 10px; display: inline-block;">
</div>

## Features

### 1. **Media Asset Upload & Sales**
   - Clients can easily **upload media assets** (videos, films, shows, etc.) to the platform.
   - Set a **price** for each uploaded asset, allowing users to **purchase and stream** the desired content.
   - **Secure payment system** to handle transactions seamlessly.

### 2. **Client Profile Pages**
   - Each client gets a **personalized profile page** to manage and showcase their media assets.
   - **Post announcements** for upcoming events, promotions, or new releases.
   - **Sell merchandise** directly from their profile page.
   - A dedicated section to view and manage all their **uploaded media assets**.

### 3. **Streaming & Playback**
   - Content is streamed using **HLS (HTTP Live Streaming)** with **Adaptive Bitrate Streaming (ABR)** for optimal viewing experience across different devices and network conditions.
   - Media is **securely streamed** with **encrypted media extensions**, ensuring content protection.
   - **Smooth playback** with support for high-definition quality streams.

### 4. **Blog Section**
   - A built-in **blog** section to share news, updates, and reviews related to the entertainment industry.
   - Clients can also post **news about their upcoming events** or announcements.
   - **Regular updates** about the streaming platform itself, including feature rollouts, maintenance schedules, and new updates.

### 5. **Responsive & User-Friendly Design**
   - Built with **Django MVC architecture** to ensure scalability and maintainability.
   - **Responsive UI** using **Bootstrap**, ensuring compatibility across all screen sizes and devices.
   - **User-centric design** for easy navigation and a seamless experience.

### 6. **Search & Discoverability**
   - Advanced **search functionality** to discover media assets based on titles, genres, and other filters.
   - Users can browse and **scroll through** the content to find their desired movies, shows, or clips.

### 7. **Content Protection & Security**
   - **Encrypted content delivery** with HLS ensures protection from piracy.
   - Secure login and user authentication systems to protect user data.

### 8. **Secure Payment Gateways**
   - **Seamless integration** with MPESA for quick secure transactions.

### 9. **Cross-Platform Support**
   - The application is fully responsive for use on **web browsers**, **mobile devices**, and various **smart TVs** for a universal viewing experience.

### 10. **Admin Dashboard**
   - **Admin control panel** for platform moderators to manage users, content, and payments.
   - **Content moderation** features for flagged or inappropriate media.
   - Manage **client profiles**, **merchandise**, and **event announcements**.

## Data Flow Diagram

![data flow on video upload](https://lh7-us.googleusercontent.com/62CWQK9WBPAH5T0nBcFDRr8_SxvG9GJSfw4hfEzuIp-kKM5_WgEQOMxThZwWU-qx0haynE3WBUC-zmmdNO4SbI78OZBWFsKChJqtscN_HOYzV73ZEvOBj14KW0dGuGPIBRD_BByyAKATc5hrCzw4v_zbjQ=s2048)

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


