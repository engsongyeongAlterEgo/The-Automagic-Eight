from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from azure.devops.v7_1.work_item_tracking import JsonPatchOperation
from azure.devops.v7_1.work_item_tracking.models import WorkItem
 
# from azure.devops.v6_0.work_item_tracking.models import JsonPatchOperation
 
# Azure DevOps organization URL and personal access token (PAT)
organization_url = 'https://dev.azure.com/ExactGroup'
personal_access_token = ''
 
# Project and work item type
project_name = 'Exact-Globe-Plus'
work_item_type = 'Task'
 
# Create a connection to Azure DevOps
credentials = BasicAuthentication('', personal_access_token)
connection = Connection(base_url=organization_url, creds=credentials)
 
# Get a client for working with work items
wit_client = connection.clients.get_work_item_tracking_client()
 
# Define fields for the new work item
new_work_item = [
    JsonPatchOperation(
        op="add",
        path="/fields/System.Title",
        value="Sample task 1"
    ),
    JsonPatchOperation(
        op="add",
        path="/fields/System.AssignedTo",
        value=" "
    ),
    # Add more fields as needed
]
 
# Create the work item
created_work_item = wit_client.create_work_item(
    document=new_work_item,
    project=project_name,
    type=work_item_type
)
 
print(f"Created work item with ID: {created_work_item.id}")
 
