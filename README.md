# 510 Data Catalog Portal

# Developer Documentation

## Prerequisite

- docker
- [make](https://stackoverflow.com/questions/32127524/how-to-install-and-use-make-in-windows)

## Steps to Run in Local environment

- Clone the repository
- Update the submodules by using `git submodule update --init --recursive`
- Copy the `.env.example` as `.env` and modify the variables in the file as per your need and replace the variables with the actual values of the environment.
- Run the make file to create the images (base image and the service image) by the `make` command. 
	- If you are using Windows, refer [below](#installing-supporting-tools) for instructions on setting up the `make` function.
    - Run `make` command
- Build the Development Environment for 510 Data Catalog using the docker-compose by `docker-compose -f docker-compose-dev.yml build`.
	- If you are using Windows, ensure that all the files are converted to LF line breaks before this step. This can be acheived using `dos2unix` script. For further instructions, refer [below](#installing-supporting-tools)
- Once the Build is done, run the project by `docker-compose -f docker-compose-dev.yml up`.
    - If DB related issue comes while setting up the environment, please exec into container using `docker exec -it ckan bash` and then run `ckan db init`

Once the project is up, you can browse the project using http://localhost:5000 or the `CKAN_SITE_URL` you used in `.env`

The development setup uses the `src/` directory for all the custom extensions and required extension (using git submodules) and mount it is as volume to docker so the changes made in `src/` will be directly updated in the docker setup. For more details, please follow [developer guide](documentation/developers_guide.md)

## Steps to Run using docker-compose

Follow the above steps mentioned in the [local environment setup](#steps-to-run-in-local-environment) but replace the `docker-compose-dev.yml` with `docker-compose.yml`

## Installing Supporting Tools

- **Make Command**: The `make` command should be available on all Linux systems. If you are developing on Windows, you can try one of these:
	- Installing any GNU Compiler system such as MinGW or Cygwin should provide the `make` command.
	- Install [Chocolatey](https://chocolatey.org/install) Package Manager and install its `make` package using the command below. This method is tested but will require administrator access to install Chocolatey.
	
	    ```
        choco install make
        ```
	
- **Dos2Unix**: Dos2Unix is a handy command-line utility to convert Windows text files (using CRLF line breaks) to Linux/UNIX text files (using LF line breaks).
	- Download [Dos2Unix]https://waterlan.home.xs4all.nl/dos2unix/dos2unix-7.4.2-win64.zip) ZIP file and extract its contents.
	- The zip contains a bin folder. Add the path up to the bin folder in your System's PATH environment variables to use the script in the terminal.
	- To convert all files in a folder and its subfolders from CRLF to LF format, open a terminal in the folder and run one of the following:
	
	  ```
	  // For GitBash Terminal Users
	  find . -type f -print0 | xargs -0 dos2unix
	  // For Windows Powershell Terminal users
	  Get-ChildItem .\ -Recurse -File | select FullName | % { dos2unix $_.FullName }
	  ```
	
	- The conversion process will take a few minutes to complete.

## Documentation to update Metadata fields for the dataset

To update the metadata fields please follow the [instructions](documentation/update_metadata_fields.md)

## Security Bugs and Vulnerability

For All security related issue please follow the [security guide](SECURITY.md)

## Developer's Guide

Please follow the [developer guide](documentation/developers_guide.md) for the components, usage and contribution to the project.

## Contributors

<a href="https://github.com/rodekruis/510-data-catalog/graphs/contributors"><img src="https://contributors-img.web.app/image?repo=rodekruis/510-data-catalog" /></a>

## Credits

Thanks to all the people who [contributed directly or indirectly.](documentation/credits.md)
