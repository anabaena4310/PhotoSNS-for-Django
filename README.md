# Photo Sharing SNS - Django Application

project is under development.

This project is a photo-sharing social networking service (SNS) built using Django. The app allows users to follow each other, view a personalized timeline, and explore posts based on their preferences. It includes user registration, login, and photo posting functionalities, along with a detailed post view where users can follow or unfollow the post author.

## Features
- User Registration & Login: Users can sign up, log in, and choose their areas of interest, which will personalize their recommended timeline.
- Photo Posting: Users can upload photos with captions and tags, which will be displayed on their own profile and shared with followers.
- Following Timeline: Users can view posts from the accounts they follow.
Recommended Timeline: Posts from users with similar preferences or relevant tags are recommended to users.
- Post Detail View: Clicking on a photo in the timeline takes the user to a detailed view of the post, where they can see the caption, tags, and the option to follow/unfollow the author.
- Responsive Design: The web application is designed to be responsive, ensuring a smooth experience on both desktop and mobile.

## Installation
1. Clone the repository:

```
git clone https://github.com/yourusername/photo-sharing-sns.git
cd photo-sharing-sns
```

2. Create a virtual environment and activate it:
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required dependencies:
```
pip install -r requirements.txt
```
4. Apply migrations:
```
python manage.py migrate
```
5. Create a superuser for admin access:
```
python manage.py createsuperuser

```
6. Start the development server:
```
python manage.py runserver
```
7. Open the app in your browser at http://127.0.0.1:8000.

## Usage
- After registration, users can log in and begin uploading photos with captions and tags.
- Users can view their timeline with posts from users they follow.
- Recommended posts will be based on the user’s interests and tags from other users' posts.
- On the post detail page, users can follow or unfollow the author of the post.
## Contributing
If you'd like to contribute to this project, please fork the repository and submit a pull request with your changes.

## License
This project is licensed under the MIT License.