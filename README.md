## API Endpoint

* `http://localhost:8000/api/auth/login/` (POST)
    * In Headers:
        {"Content-Type": "application/json"}
    * Body:
        {
            "username": "viral",
            "password": "pass@123"
        }

    * Response:
        {
            "key": "5baaa7c35bf3a57854dcf6722844e0043f7e0fa4"
        }

        * `Note` Save this key for further use

* `http://localhost:8000/api/auth/logout/` (GET)
    * In Headers:
        {
            "Content-Type": "application/json",
            "Authorization": "Token 5baaa7c35bf3a57854dcf6722844e0043f7e0fa4" # <== (key received while loggin in)
        }
    * Body:
        No Body required

    * Response:
        {
            "detail": "Successfully logged out."
        }

        * `Note` Show login page next time instead of Homepage after logout

(Only for Website)
* `http://localhost:8000/api/auth/Register/` (POST)
    * In Headers:
        {
            "Content-Type": "application/json",
        }
    * Body:
        {
            "username": "viral",
            "email": "fake@gmail.com"
            "password": "pass@123"
        }

    * Response:
        {
            "key": "5baaa7c35bf3a57854dcf6722844e0043f7e0fa4"
        }

        * `Note` Save this key for further use

(On Homepage)
Use this for now, i will update OTP api by tommorrow
* `http://localhost:8000/api/auth/user/` (GET)
    * In Headers:
        {
            "Content-Type": "application/json",
            "Authorization": "Token 5baaa7c35bf3a57854dcf6722844e0043f7e0fa4" # <== (key received while loggin in)
        }
    * Body:
        No Body required

    * Response:
        {
            "pk": 1,
            "username": "viral",
            "email": "",
            "first_name": "",
            "last_name": ""
        }

        * `Note` Show login page next time instead of Homepage after logout
