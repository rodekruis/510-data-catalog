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
      - Run `make` command
- Build the Development Environment for 510 Data Catalog using the docker-compose by `docker-compose -f docker-compose-dev.yml build`.
- Once the Build is done, run the project by `docker-compose -f docker-compose-dev.yml up`.
    - If DB related issue comes while setting up the environment, please exec into container using `docker exec -it ckan bash` and then run `ckan db init`

Once the project is up, you can browse the project using http://localhost:5000 or the `CKAN_SITE_URL` you used in `.env`

The development setup uses the `src/` directory for all the custom extensions and required extension (using git submodules) and mount it is as volume to docker so the changes made in `src/` will be directly updated in the docker setup. For more details, please follow [developer guide](documentation/developers_guide.md)

## Steps to Run using docker-compose

Follow the above steps mentioned in the [local environment setup](#steps-to-run-in-local-environment) but replace the `docker-compose-dev.yml` with `docker-compose.yml`

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
