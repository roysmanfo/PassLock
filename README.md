![PassLock logo](img/logos/png/logo-line-color.png)
> NOTE: _on the master branch you will find the cli version, the GUI version is still in development in the GUI branch_
## Installation

There are multiple ways to install passlock, If one option does not work for you, try the other ones.

### Method 1 - Using the release binaries
In the [release](https://github.com/roysmanfo/PassLock/releases/latest) section there are binaries for Windows (.zip) and Linux (.tar.gz and .tar.xz)

**Windows installation**  
- Download and extract `passlock-{version}.zip`
- Place the contents of the archive where you want on disk (can be inside `C:\Programs\`)

To be able to search and passlock from the windows search bar

- create a new shortcut to the executable `passlock.exe`
- place the shurtcut in `C:\Users\{your_user_name}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs`

Now passlock is installed, you can search it in the search bar and run it.

> Windows may detect block the execution and flag it as dangerous,
> as the program is not signed and does not contain some metadata
> that Windows will look for. Just allow to execute it.

**Linux installation**
- Download and extract either `passlock-{version}.tar.gz` or `passlock-{version}.tar.xz` (note that `.tar.xz` is lighter and faster to download)
- Place the contents of the archive in the `/usr/share/passlock` folder
- create a symlink to the `passlock` executable
```
ln /usr/share/passlock/passlock passlock 
```
- place the symlink in the `/usr/bin` folder

Now passlock is installed, you can type `passlock` in the terminal run it.

> You may have to add the `x` flag to the executable to run it.  
> You can do so with `chmod +x /usr/share/passlock/passlock`


### Method 2 - Installing from source
- You need to install [python](https://python.org/downloads/) (_and add it to PATH_)
- You need to install [git](https://git-scm.com/downloads)
- Clone this repository on your machine
```
git clone https://github.com/roysmanfo/PassLock
```
- Install the application using `pip`
```
pip install -r requirements.txt
pip install ./PassLock
```


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
