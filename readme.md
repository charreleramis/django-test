



Run the project
pipenv shell
python manage.py runserver


Run the seeder to seed data
python manage.py seed_data



http://127.0.0.1:8000/api/users/signin/
http://127.0.0.1:8000/api/users/signup/


Add the cookie the authentication header


http://127.0.0.1:8000/api/rides/?page=5&page_size=1
http://127.0.0.1:8000/api/rides/?email=<email>
http://127.0.0.1:8000/api/rides/?status=completed

Sort ride list by distance
http://127.0.0.1:8000/api/rides/?sort=distance&lat=40.7128&lon=-74.0060

Sort ride list by pickup time
http://127.0.0.1:8000/api/rides/?sort=2026-02-16 01:00:24.300705