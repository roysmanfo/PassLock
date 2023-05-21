# PassLock

Save all your password in a secure way on your local device.

## How does it work

Password after being encrypted, get stored in a JSON file with the following format:

```json
{
  "PM-hash": "...",
  "Hint": "A non encrypted sentence choosed by you displayed when login fails 3 times",
  "Apps": {
    "website-name": {
      "username": "your encrypted username",
      "password": "your encrypted password"
    },

    "app-name": {
      "password": "your encrypted password"
    },

    "website-name": {
      "email": "your encrypted email address",
      "password": "your encrypted password"
    }
  }
}
```
As you can see, there are multiple ways to save your data  
NOTE: *Everything is encrypted, both keys and values, except for the keys `"Apps"` and `PM-hash` that are not*
## Commands
To learn more about the commands available goto the [documentation](./DOCS.md)
