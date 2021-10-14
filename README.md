510 Data Catalog Portal
==========================
----------------------------------------------------------------
### Developer Documentation

#### Installation to Run in Local environment

- Clone the repository
- Run the make file to create the images by `make` command.
- Copy the `.env.example` as `.env` and modify as per your need.
- Start the CKAN using the docker-compose by `docker-compose -f docker-compose.yml up`.

The above setup will use the `src/` directory and mount it is as volume to docker so the changes made in `src/` will be directly updated in the docker setup.

#### Documentation to update Metadata fields for the dataset and resource

To update the metadata fields please follow the instructions in [a relative link](documentation/update_metadata_fields.md)
