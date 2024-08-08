import tkinter as tk
from tkinter import messagebox
# pip install tk
from azure.devops.connection import Connection
# pip install azure-devops
from msrest.authentication import BasicAuthentication
from azure.devops.v7_0.work_item_tracking import JsonPatchOperation
from azure.devops.v7_0.work_item_tracking.models import Wiql
# pip install beautifulsoup4
from bs4 import BeautifulSoup
from selenium import webdriver
# pip install selenium
import webbrowser
from storage import readData
# from accToken import token as personal_access_token

# personal_access_token = readData()['userToken'] if readData()['userToken'] else ''
# personal_access_token = '' #Place your token here

# # Azure DevOps organization URL and personal access token (PAT)
organization_url = 'https://dev.azure.com/ExactGroup'

project_name = 'Exact-Globe-Plus'
# work_item_type = 'Task'
# # Create a connection to Azure DevOps
credentials = None
connection = None
# wit_client = connection.clients.get_work_item_tracking_client()

# title = " "
# Function to retrieve Bug work item from Azure DevOps    
def getBug(bugTitle):
    personal_access_token = readData()['userToken'] if readData()['userToken'] else ''
    credentials = BasicAuthentication('', personal_access_token) if personal_access_token != '' else None
    connection = Connection(base_url=organization_url, creds=credentials) if credentials else None
    wit_client = connection.clients.get_work_item_tracking_client()

    # Escape single quotes in bugTitle for Wiql query
    bugTitle_for_query = bugTitle.replace("'", "''")

    # print(bugTitle_for_query)
    
    # Define your query using the bugTitle variable
    query = Wiql(query=f"SELECT [System.Id], [System.AssignedTo], [System.State], [System.Title], [System.Tags] FROM WorkItems WHERE [System.WorkItemType] = 'Bug' AND [Custom.SynergyRequestID] = '{bugTitle_for_query}'")

    # Execute the query
    try:
        work_items = wit_client.query_by_wiql(query).work_items
        if work_items:
            for work_item in work_items:
                # print(f"Bug ID: {str(work_item['System.AssignedTo'])}")
                work_item2 = wit_client.get_work_item(work_item.id)
                return [work_item.id, work_item2.fields['System.AssignedTo']['displayName'], work_item2.fields['System.Title']]
        else:
            return None
    except Exception as ex:
        print(f"Error executing query: {ex}")
        return None

def open_work_item_in_browser(bug_work_item_id, organization_url, project_name):
    if bug_work_item_id:
        work_item_url = f"{organization_url}/{project_name}/_workitems/edit/{bug_work_item_id}"
        webbrowser.open(work_item_url)
    else:
        messagebox.showwarning("Error", "Bug ID not found or request not approved.")

# def on_submit():
#     url = entry_url.get()

#     # Initialize Selenium WebDriver (Chrome)
#     driver = webdriver.Chrome()
#     driver.get(url)

#     # Wait for the page to load (adjust the sleep time as needed)
#     driver.implicitly_wait(10)  # Wait up to 10 seconds for elements to appear

#     # Create a BeautifulSoup object with JavaScript rendered content
#     soup = BeautifulSoup(driver.page_source, 'html.parser')
  
#     # Find the element using the specific CSS selector
#     try:
#         element = soup.select_one('#_Header > table > tbody > tr > td:nth-child(1) > span')
#         name = soup.select_one('#nano-content > table.WorkflowBlock > tbody > tr:nth-child(2) > td:nth-child(3) > a')
#         desc = soup.find(id ='Description')
#         if name:
#             if element and desc:
#                 # Extract the numbers using regex
#                 match = re.search(r'\b\d+\.\d+\.\d+\b', element.text)
#                 title = desc.text.strip()
#                 userName = name.text.strip()
#                 if match :
#                     br_id.set(match.group())
#                     bug_work_item_id = getBugID(match.group(), organization_url, personal_access_token)
#                     if bug_work_item_id and title and userName:
#                         bug_id.set(bug_work_item_id)
                        
#                         # Define fields for the new work items
#                         new_work_item_coding = [
#                             JsonPatchOperation(
#                                 op="add",
#                                 path="/fields/System.Title",
#                                 value= "[CODING]" + title
#                             ),
#                             JsonPatchOperation(
#                                 op="add",
#                                 path="/fields/System.AssignedTo",
#                                 value= userName
#                             ),
#                                 JsonPatchOperation(
#                                 op="add",
#                                 path="/relations/-",
#                                 value={
#                                     "rel": "System.LinkTypes.Hierarchy-Reverse",
#                                     "url": f"{organization_url}/_apis/wit/workItems/{bug_work_item_id}"
#                                 }
#                             ),
#                             # Add more fields as needed
#                         ]
                        
#                         new_work_item_testing = [
#                             JsonPatchOperation(
#                                 op="add",
#                                 path="/fields/System.Title",
#                                 value= "[TESTING]" + title
#                             ),
#                             JsonPatchOperation(
#                                 op="add",
#                                 path="/fields/System.AssignedTo",
#                                 value= " "
#                             ),
#                             JsonPatchOperation(
#                                 op="add",
#                                 path="/fields/Microsoft.VSTS.Common.Activity",
#                                 value="Testing"
#                             ),
#                                 JsonPatchOperation(
#                                 op="add",
#                                 path="/relations/-",
#                                 value={
#                                     "rel": "System.LinkTypes.Hierarchy-Reverse",
#                                     "url": f"{organization_url}/_apis/wit/workItems/{bug_work_item_id}"
#                                 }
#                             ),
#                         ]
                        
#                         # Uncomment when you want to create task:

#                         # Create the work items
#                         try:
#                             created_work_item_coding = wit_client.create_work_item(
#                                 document=new_work_item_coding,
#                                 project=project_name,
#                                 type=work_item_type
#                             )
#                             print(f"Created Coding work item with ID: {created_work_item_coding.id}")
                        
#                             created_work_item_testing = wit_client.create_work_item(
#                                 document=new_work_item_testing,
#                                 project=project_name,
#                                 type=work_item_type
#                             )
#                             print(f"Created Testing work item with ID: {created_work_item_testing.id}")
                        
#                         except Exception as e:
#                             print(f"Failed to create work items: {str(e)}")
                        
#                         def update_work_item(wit_client, work_item_id, project_name):
#                             update_patch_document = [
#                                 JsonPatchOperation(
#                                     op="replace",  # Use "replace" to update an existing field
#                                     path="/fields/System.State",
#                                     value="Done"
#                                 ),
#                             ]
                        
#                             try:
#                                 updated_work_item = wit_client.update_work_item(
#                                     document=update_patch_document,
#                                     id=work_item_id,
#                                     project=project_name
#                                 )
#                                 print(f"Updated work item with ID: {updated_work_item.id}")
#                             except Exception as e:
#                                 print(f"Failed to update work item: {str(e)}")
                        
#                         # Example usage
#                         update_work_item(wit_client, created_work_item_coding.id, project_name)
#                     else:
#                         bug_id.set("Bug ID not found or request not approved.")
#                         messagebox.showwarning("Error", "Bug ID not found or request not approved.")
#                 else:
#                     br_id.set("BR ID not found in the element.")
#             else:
#                 br_id.set("Element not found.")
#         else:
#             br_id.set("Name not found.Please make sure BR approved.")
#     except Exception as e:
#         br_id.set(f"An error occurred: {e}")

#     # Close the WebDriver
#     driver.quit()

# # Create the main window
# root = tk.Tk()
# root.title("Auto Magic Core")
# root.geometry("600x400")

# # Set background color to red
# root.configure(bg="red")

# # Create labels and entry fields with red color
# label_url = tk.Label(root, text="Enter URL:", bg="red", fg="white", font=("Arial", 12, "bold"))
# label_url.pack(pady=10)
# entry_url = tk.Entry(root, width=60)
# entry_url.pack()

# # Button to submit URL
# btn_submit = tk.Button(root, text="Submit", command=on_submit, bg="black", fg="white", font=("Arial", 12, "bold"))
# btn_submit.pack(pady=10)

# # Label and text variable for BR ID
# label_br_id = tk.Label(root, text="BR ID:", bg="red", fg="white", font=("Arial", 12, "bold"))
# label_br_id.pack(pady=5)
# br_id = tk.StringVar()
# br_id.set("")
# label_br_id_value = tk.Label(root, textvariable=br_id, bg="red", fg="white", font=("Arial", 12))
# label_br_id_value.pack()

# # Label and text variable for Bug ID
# label_bug_id = tk.Label(root, text="Bug ID:", bg="red", fg="white", font=("Arial", 12, "bold"))
# label_bug_id.pack(pady=5)
# bug_id = tk.StringVar()
# bug_id.set("")
# label_bug_id_value = tk.Label(root, textvariable=bug_id, bg="red", fg="white", font=("Arial", 12))
# label_bug_id_value.pack()

# # Button to open work item in browser
# btn_open = tk.Button(root, text="Open Work Item", command=lambda: open_work_item_in_browser(bug_id.get(), organization_url, project_name), bg="black", fg="white", font=("Arial", 12, "bold"))
# btn_open.pack(pady=10)

# # Run the main loop
# root.mainloop()