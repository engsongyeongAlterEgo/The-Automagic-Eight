from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from azure.devops.v7_1.work_item_tracking import JsonPatchOperation
from pathway import userName
import requests
 
# Azure DevOps organization URL and personal access token (PAT)
organization_url = 'https://dev.azure.com/ExactGroup'
personal_access_token = ''
 
# Project and work item type
project_name = 'Exact-Globe-Plus'
work_item_type = 'Task'
 
# Assigned Retrieved Bug ID to this variable
bug_work_item_id = 0
title = " "
bug_id = " "
bug_type = " "
 
# Create a connection to Azure DevOps
credentials = BasicAuthentication('', personal_access_token)
connection = Connection(base_url=organization_url, creds=credentials)
 
# Get a client for working with work items
wit_client = connection.clients.get_work_item_tracking_client()
 
# Define fields for the new work items
new_work_item_coding = [
    JsonPatchOperation(
        op="add",
        path="/fields/System.Title",
        value= "[CODING]{title}"
    ),
    JsonPatchOperation(
        op="add",
        path="/fields/System.AssignedTo",
        value= userName
    ),
        JsonPatchOperation(
        op="add",
        path="/relations/-",
        value={
            "rel": "System.LinkTypes.Hierarchy-Reverse",
            "url": f"{organization_url}/_apis/wit/workItems/{bug_work_item_id}"
        }
    ),
    # Add more fields as needed
]
 
new_work_item_testing = [
    JsonPatchOperation(
        op="add",
        path="/fields/System.Title",
        value= "[TESTING] }{title}"
    ),
    JsonPatchOperation(
        op="add",
        path="/fields/System.AssignedTo",
        value= userName
    ),
    JsonPatchOperation(
        op="add",
        path="/fields/Microsoft.VSTS.Common.Activity",
        value="Testing"
    ),
        JsonPatchOperation(
        op="add",
        path="/relations/-",
        value={
            "rel": "System.LinkTypes.Hierarchy-Reverse",
            "url": f"{organization_url}/_apis/wit/workItems/{bug_work_item_id}"
        }
    ),
]
 
# Create the work items
try:
    created_work_item_coding = wit_client.create_work_item(
        document=new_work_item_coding,
        project=project_name,
        type=work_item_type
    )
    print(f"Created Coding work item with ID: {created_work_item_coding.id}")
 
    created_work_item_testing = wit_client.create_work_item(
        document=new_work_item_testing,
        project=project_name,
        type=work_item_type
    )
    print(f"Created Testing work item with ID: {created_work_item_testing.id}")
 
except Exception as e:
    print(f"Failed to create work items: {str(e)}")
 
def update_work_item(wit_client, work_item_id, project_name):
    update_patch_document = [
        JsonPatchOperation(
            op="replace",  # Use "replace" to update an existing field
            path="/fields/System.State",
            value="Done"
        ),
    ]
   
    try:
        updated_work_item = wit_client.update_work_item(
            document=update_patch_document,
            id=work_item_id,
            project=project_name
        )
        print(f"Updated work item with ID: {updated_work_item.id}")
    except Exception as e:
        print(f"Failed to update work item: {str(e)}")
 
# Example usage
update_work_item(wit_client, created_work_item_coding.id, project_name) 