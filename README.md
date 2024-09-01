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
> NOTE: *Everything is encrypted, both keys and values, except for the keys `"Apps"`, `"Hint"` and `PM-hash` that are not*
## Commands
To learn more about the commands available go to the [documentation](./DOCS.md)


## How is it secure

#### Password Master Hash
The hash is generated using the sha512 algorithm, which generates a 128byte output
> This algorithm is a little slower to compute than sha256, but it's large output size
> makes it less prone to collisions (if you want, you can switch over to another hashing algorithm)
When lost there is no way of recovery (only bruteforce, dictionary attacks and rainbow tables may save you here)

#### Hint
The hint is stored in plain text, as it is supposed to help you recover the password.  
**For this reason you should be careful about what you write here**  
It is reccomended to setup the hint as soon as you create a new vault.

#### Keys (Apps and Fields)
The keys are encrypted before being stored.
The algorithm used to encrypt the passwords is [Fernet](https://cryptography.io/en/latest/fernet/),
but another algorithms may be more suitable, I chose this one because it is beginner friendly,
so even if you just started working with the [cryptography](https://cryptography.io/en/latest)
module, you should know how it works

When you provide the right password, the key for Fernet is derivated using
[PBKDF2HMAC](https://cryptography.io/en/latest/hazmat/primitives/key-derivation-functions/#pbkdf2)