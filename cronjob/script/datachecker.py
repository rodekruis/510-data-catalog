import requests
from multiprocessing import Pool

from components.config import ENV, APIS
from components.logger import logger
from components.controllers import DatalakeController, DatabaseController
from components.send_email import generate_email_content, send_mail

headers = {
    "Authorization": ENV["CKAN_API_KEY"],
}
invalid_resources = []


def get_path(resource):
    try:
        resource_paths = {
            "database": lambda resource: "/".join(
                [
                    resource["database_connection"],
                    resource["schema_name"],
                    resource["table_name"],
                ]
            ),
            "datalake": lambda resource: "/".join(
                [
                    resource["datalake_data"]["container"],
                    resource["datalake_data"]["file_path"],
                ]
            ),
            "url": lambda resource: resource["url"],
        }
        return resource_paths[resource["resource_type"]](resource)
    except Exception as e:
        logger.error(e)


def generate_ckan_url(dataset_name, resource_id):
    ckan_url = ""
    try:
        ckan_url = "{}/dataset/{}/resource/{}".format(
            ENV["CKAN_SITE_URL"], dataset_name, resource_id
        )
    except Exception as e:
        logger.error(e, exc_info=True)
    finally:
        return ckan_url


def check_resource(resource):
    result = None
    try:
        logger.info(resource["name"])
        if resource["resource_type"] == "datalake":
            datalake_service_client = DatalakeController()
            datalake_service_client.create_client()
            result = datalake_service_client.find_file_or_directory(
                resource["datalake_data"]["container"],
                resource["datalake_data"]["file_path"],
            )

        elif resource["resource_type"] == "database":
            result = True
            database_service_client = DatabaseController()
            database_service_client.create_client(
                resource["database_connection_type"], resource["database_connection"]
            )
            result = database_service_client.find_table(
                resource["schema_name"], resource["table_name"]
            )
        else:
            result = True
    except Exception as e:
        logger.error(e, exc_info=True)
    finally:
        return result


def handle_package_job(package):
    invalid_res_sublist = []
    logger.info("Handling package: " + package["dataset_name"])
    try:
        if len(package["resources"]) > 0:
            for resource in package["resources"]:
                result = check_resource(resource)
                if not result:
                    resource_data = {
                        "name": resource["name"],
                        "ckan_url": generate_ckan_url(
                            package["name"], resource["id"]
                        ),
                        "resource_type": resource["resource_type"],
                        "data_source_path": get_path(resource),
                        "package_name": package["dataset_name"],
                        "dataset_owner_email": package["dataset_owner_email"],
                    }
                    invalid_res_sublist.append(resource_data)
    except Exception as e:
        logger.error(e, exc_info=True)
    finally:
        return invalid_res_sublist


def dispatch_workers(data, no_of_workers, target):
    result_list = []
    try:
        with Pool(processes=no_of_workers) as p:
            result_list = p.map(target, data)
    except Exception as e:
        logger.error(e, exc_info=True)
    finally:
        return result_list


if __name__ == "__main__":
    package_list = []
    try:
        rows = 10
        start = 0
        stop_api = False
        url = ENV["CKAN_SITE_URL"] + APIS["PACKAGE_SEARCH"]
        while not stop_api:
            try:
                response = requests.get(
                    url,
                    headers=headers,
                    params={"rows": rows, "start": start,
                            "include_private": True}
                )
            except Exception as e:
                raise e
            if response.json()["success"]:
                response = response.json()
                results = response["result"]["results"]
                if len(results) > 0:
                    package_list.extend(results)
                    start += rows
                else:
                    stop_api = True
        logger.info("Found {} packages.".format(str(len(package_list))))
        if len(package_list) > 0:
            invalid_resource_list = dispatch_workers(
                package_list, 5, handle_package_job
            )
            for resource_list in invalid_resource_list:
                invalid_resources.extend(resource_list)
            logger.info(invalid_resources)
            if len(invalid_resources) > 0:
                for resource_info in invalid_resources:
                    email_content = generate_email_content(
                        resource_info["name"],
                        resource_info["data_source_path"],
                        resource_info["ckan_url"],
                    )
                    print(email_content)
                    response = send_mail(
                        [resource_info["dataset_owner_email"], ENV["TEAMS_CHANNEL_EMAIL"]],
                        email_content,
                    )
    except Exception as e:
        logger.error(e, exc_info=True)
