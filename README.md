# Project Name: Item Catalogue

The following tool is a web application that catalogues items under different categories. Each item added is secured with authentication and authorisation measures.

## Requirements

* Terminal Application
* VirtualBox
* vagrant
* Vagrant configuration file as provided by Udacity
* Python
* PostgreSQL
* pyscopg2 library


For this project a Virtual Machine (VM) is provided setup with Vagrant which contains the PostgreSQL database and support software required for the project.

##### Use a terminal

You will require a Unix-style terminal on your computer for this project.
* Mac of Linux: The built in terminal program is sufficient.
* Windows: You can use the Git Bash terminal that comes with the Git software. If you don't already have Git installed, download Git from [git-scm.com](https://git-scm.com/downloads).

##### Install VirtualBox

VirtualBox is the program used to run the VM simulating the Linux server of the site. You can [download it from virtualbox.org, here](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1).

> Install the platform package for your operating system. You do not need the extension pack or the SDK. You do not need to launch VirtualBox after installing it; Vagrant will do that. Currently (October 2017), the supported version of VirtualBox to install is version 5.1. Newer versions do not work with the current release of Vagrant.

> Ubuntu users: If you are running Ubuntu 14.04, install VirtualBox using the Ubuntu Software Center instead. Due to a reported bug, installing VirtualBox from the site may uninstall other software you need.

##### Install Vagrant

Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's filesystem. Download it from [vagrantup.com](https://www.vagrantup.com/downloads.html). Install the version for your operating system.

> Windows users: The Installer may ask you to grant network permissions to Vagrant or make a firewall exception. Be sure to allow this.

If Vagrant is successfully installed, you will be able to run `vagrant --version` in your terminal to see the version number.

##### Download the VM configuration

There are a couple of different ways you can download the VM configuration.

You can download and unzip this file: [FSND-Virtual-Machine.zip](https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip) This will give you a directory called `/FSND-Virtual-Machine`. It may be located inside your Downloads folder. Alternately, you can use [Github to fork and clone the repository](https://github.com/udacity/fullstack-nanodegree-vm).

Either way, you will end up with a new directory containing the VM files. Change to this directory in your terminal with `cd`. Inside, you will find another directory called `/vagrant`.

##### Running the database

The PostgreSQL database server will automatically be started inside the VM. You can use the psql command-line tool to access it and run SQL statements.

##### Logging out and in

If you type `exit` (or Ctrl-D) at the shell prompt inside the VM, you will be logged out, and put back into your host computer's shell. To log back in, make sure you're in the same directory and type `vagrant ssh` again. To stop vagrant running in the background you can use `vagrant halt` once you're back into your host computer's terminal. If you reboot your computer, you will need to run `vagrant up` to restart the VM.


## How to use

##### Start the virtual machine

From your terminal, inside the vagrant subdirectory, run the command `vagrant up`. This will cause Vagrant to download the Linux operating system and install it. This may take quite a while (many minutes) depending on how fast your Internet connection is.

![running vagrant up screenshot](/sc_vagrant_up.png)

Once it's finished running, you will get your shell prompt back. At this point, you can run `vagrant ssh` to log in to your newly installed Linux VM!

![running vagrant ssh screenshot](/sc_vagrant_ssh.png)

If you are now looking at a shell prompt that starts with the word **vagrant** then congratulations you're now logged in to your Linux VM.

##### Navigate to the main directory

Inside the VM, change directory to `/vagrant`. The files you see here are the same as the ones in the `/vagrant` subdirectory on your computer (where you started Vagrant from). Any file you create/edit in one will be automatically shared to the other. Please keep in mind that the PostgreSQL database itself lives only inside the VM.


![changing to the vagrant directory screenshot](/sc_vagrant_folder.png)

##### Setup the Database

With the terminal of your VM in focus run the following command:

```
python database_setup.py
```
![running python database_setup.py screenshot](/sc_dbpy.png)

This will run the code to setup the database and the next command will start the server.

#### Obtain a Client ID for securing the application

Visit `https://console.developers.google.com` and setup a new application. Download the JSON app secrets file to the `/vagrant` directory and rename it to **client_secrets.json**.


#### Run the program

```
python application.py
```
![running python application.py screenshot](/sc_app_py.png)

You can finally access the app using:

```
http://localhost:8000/
```
