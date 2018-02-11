
# WHK MyNetwork

A private network writed in python using a own tcp/protocol.


## Advantage

- It does not require a special client, it only communicates via sockets.
- Not need HTTP, out of WEB spiders like as Google.
- You do not need special privileges or complex requirements for its execution.
- It is not monitored by the Appliances due to the use of its own protocol.
- It does not require the use of standard ports.
- Support for multiple users with permission levels for the execution of each task or access.
- Support for different groups and access levels.
- The functionalities you create yourself!
- You do not need to restart the server to enable new modules.


## How to use?

Run server with:  `$ python main.py` This will leave listener a service on port 9777 (can be modified):

    whk@machine:~$ python main.py 
    ➤ MyNetwork 1.2.1 by WHK
    + Starting server ...
    + Listen on port: 9777
    + Log format:
      [DATE] [REMOTE ADDRESS:REMOTE PORT] [USER] Message
    ────────────────────────────────────────────────────────────────────────────────

From now on, each client must connect directly using telnet or netcat depending on the system:

    whk@machine:~$ nc -v localhost 9777
    Connection to localhost 9777 port [tcp/*] succeeded!
    ➤ MyNetwork 1.2.1 by WHK
    Type "help" to get help or type "login" to log in.
    MyNet >

It's that easy.


## Native commands available

Each user group have a specific modules available. An example of the use:

    whk@machine:~$ nc -v localhost 9777
    Connection to localhost 9777 port [tcp/*] succeeded!
    ➤ MyNetwork 1.2.1 by WHK
    Type "help" to get help or type "login" to log in.
    MyNet > help
      Use     : [module] [arguments]
      Example : test a b c
      To see the available modules, type: mods
      To show the help of each module write:
          module --help
          module -h
    MyNet > mods
    Available modules (5):
     • exit
     • help
     • login
     • mods
     • version
    To know the operation of each one, write the name of the module followed by the help argument: "-h"
    By example: mods -h
    MyNet > login
    Login to the system
    Username : admin
    Password : admin
    Welcome admin!, you have new modules available, write "mods" to see them.
    admin@MyNet > mods
    Available modules (7):
     • exit
     • help
     • logout
     • mods
     • passwd
     • useradd
     • version
    To know the operation of each one, write the name of the module followed by the help argument: "-h"
    By example: mods -h
    admin@MyNet >

The modules are:

    whk@machine:/MyNetwork/mods/all$ ls -la
    total 48
    drwxr-xr-x 2 whk whk 4096 feb 10 23:15 .
    drwxr-xr-x 4 whk whk 4096 feb 11 01:23 ..
    -rw-r--r-- 1 whk whk  769 feb 11 00:06 exit.py
    -rw-r--r-- 1 whk whk 1033 feb 11 00:07 help.py
    -rw-r--r-- 1 whk whk 1319 feb 11 01:20 __init__.py
    -rw-r--r-- 1 whk whk 2151 feb 11 00:06 login.py
    -rw-r--r-- 1 whk whk 1035 feb 11 00:06 logout.py
    -rw-r--r-- 1 whk whk 1827 feb 11 00:06 mods.py
    -rw-r--r-- 1 whk whk 3653 feb 11 00:10 passwd.py
    -rw-r--r-- 1 whk whk 2396 feb 11 01:17 useradd.py
    -rw-r--r-- 1 whk whk  921 feb 11 01:17 userdel.py
    -rw-r--r-- 1 whk whk  786 feb 11 01:18 version.py

To manage permisions, each user have a group, each group have a specific directory:

    whk@machine:/MyNetwork/mods/byusergroups$ ls -la | grep dr
    drwxr-xr-x 5 whk whk 4096 feb 11 01:23 .
    drwxr-xr-x 4 whk whk 4096 feb 11 01:23 ..
    drwxr-xr-x 2 whk whk 4096 feb 11 01:24 admin
    drwxr-xr-x 2 whk whk 4096 feb 10 23:15 basic
    drwxr-xr-x 2 whk whk 4096 feb 11 01:24 guest

The `admin`, `basic` and `guest`, into each directory have a symbolic links with the available module fot the user group, by example:

    whk@machine:/MyNetwork/mods/byusergroups/admin$ ls -la | grep .py\ -
    lrwxrwxrwx 1 whk whk   17 feb 10 23:15 exit.py -> ../../all/exit.py
    lrwxrwxrwx 1 whk whk   17 feb 10 23:15 help.py -> ../../all/help.py
    lrwxrwxrwx 1 whk whk   21 feb 10 23:15 __init__.py -> ../../all/__init__.py
    lrwxrwxrwx 1 whk whk   19 feb 10 23:15 logout.py -> ../../all/logout.py
    lrwxrwxrwx 1 whk whk   17 feb 10 23:15 mods.py -> ../../all/mods.py
    lrwxrwxrwx 1 whk whk   19 feb 10 23:15 passwd.py -> ../../all/passwd.py
    lrwxrwxrwx 1 whk whk   20 feb 10 23:15 useradd.py -> ../../all/useradd.py
    lrwxrwxrwx 1 whk whk   20 feb 10 23:15 version.py -> ../../all/version.py

Now, you are ready for make you new modules for your system!


## Howto make a new modules?

Make a new python file into `mods/all` directory, this is a example of a basic module (`mods/all/hello.py`):

    #!/usr/bin/env python
    # -*- coding: utf-8 -*-
      
     
    class hello:
        
        def __init__(self, ctx):
            self.ctx = ctx
            self.info = {
                'name'        : self.__class__.__name__,
                'version'     : [1, 0, 0],
                'description' : 'Display a hello message.'
            }
            self.ctx.args.setModuleInfo(self.info)
            self.ctx.args.appendArgument(a_short='h', a_long='help', description='Show this help message')
            self.ctx.args.appendArgument(a_short='n', a_long='name', description='Use a specific name')
        
        
        def callFromMain(self):
            # Check if more information about the module has been requested
            if self.ctx.args.isCalled('help'):
                self.ctx.sendToClient(self.ctx.args.getHelpMessage())
            
            # Normal execution
            else:
                if self.ctx.auth.user.isLogged():
              
                    if self.ctx.args.isCalled('name'):
                        name = self.ctx.args.getMain(0).strip()
                    else:
                        name = self.ctx.auth.user.getName()
             
                    self.ctx.sendToClient('Hello ' + str(username) + '!')
              
                else:
                    self.ctx.sendToClient('You are not authenticated.')

- See, the class name is same of the filename.
- `self.info` contains the basic module information. 
- `self.ctx.args.appendArgument` append a each argument for the call module.
- `callFromMain`  is the main function, it will be called every time it is necessary.
- `if self.ctx.auth.user.isLogged():` Verify is the user is logged.
- `self.ctx.args.isCalled('name')` Check if the `name` argument is invoked.
- `self.ctx.args.getMain(0).strip()` Get the value of the first argument (name).
- `self.ctx.sendToClient` Send to client the specific message.

Now, nedd make a symbolic link for enable module in specific user group into `mods/byusergroups`, if need make a new usergroup need make a new folder, by example: `mods/byusergroups/develops`.

For more help, see the source code or write a email to [me](mailto:whk@elhacker.net)


## How to contribute?

|METHOD                 |WHERE                                                                                        |
|-----------------------|---------------------------------------------------------------------------------------------|
|Donate                 |[Paypal](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=KM2KBE8F982KS) |
|Find bugs              |Using the [Issues tab](https://github.com/WHK102/MyNetwork/issues)                           |
|Providing new ideas    |Using the [Issues tab](https://github.com/WHK102/MyNetwork/issues)                           |
|Creating modifications |Using the [Pull request tab](https://github.com/WHK102/MyNetwork/pulls)                      |
