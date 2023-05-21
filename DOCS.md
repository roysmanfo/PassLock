# Commands to use PassLock
A list of the commands that are used to interact with the app.

**Command**                     | **Description**
--------------------------------|--------------------------------
**help**                        | Show all commands available
**del KEY[.FIELD]**             | Delete the credentials of the specified app/field (i.e `del github.phone` or `del github`)
**rm KEY[.FIELD]**              | Delete the credentials of the specified app/field (i.e `rm github.phone` or `rm github`)
**add KEY**                     | Add the new app/apps to the vault (i.e `add github bitcoin work`)
**get KEY**                     | Get all credentials for the specified app (*case insensitive*)
**set KEY[.FIELD] VALUE**       | Add/Update the credentials for the specified app (i.e `set github.password password` )
**list [-s]**                   | List all app names. `-s` sorts the names based on the number of fields
**ls [-s]**                     | List all app names. `-s` sorts the names based on the number of fields
**rename KEY[.FIELD] VALUE**    | Rename a key or a field (i.e `rename work.code passkey` or `rename work job`)
**rnm KEY[.FIELD] VALUE**       | Rename a key or a field (i.e `rnm work.code passkey` or `rnm work job`)
**clear**                       | Clear the screen
**chpass**                      | Change the password master.
**sethint VALUE**               | Set a hint for when you forget the password master
