![PassLock logo](img/logos/png/logo-line-color.png)
> NOTE: _on the master branch you will find the cli version, the GUI version is still in development in the GUI branch_
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
> NOTE: *Everything is encrypted, both keys and values, except for the keys `"Apps"`, `"HHint"` and `PM-hash` that are not*
## Commands
To learn more about the commands available goto the [documentation](./DOCS.md)
