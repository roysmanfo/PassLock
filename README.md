# PassLock

Save all your password in a secure way on your local device.


## Wow does it work
Password after being encrypted, get stored in a JSON file with the following format:

```json
// As you can see, there are multiple ways to save your data
{
    "website-name": {
        "username": "your encrypted username",
        "password": "your encrypted password"
    },

    "app-name": {
        "password": "your encrypted password"
    },

    "website-name": {
        "email": "your encrypted email address",
        "password": "your encrypted password",
    }
}

```