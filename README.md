## Python Installation Guide
Python (3.7 Above) : Install via Microsoft Store / Online 
To check is Python installed, Run "pip -V" in command prompt
If it's not found try:
1.  Search on bottom left : "Edit the system environment variables"
2.  Click on "Environment Variables..."
3.  Double Click Row "Path" in User variables for Username
4.  Add on "C:\Users\Username\AppData\Local\Programs\Python\Python Version"
5.  Add on "C:\Users\Username\AppData\Local\Programs\Python\Python Version\Scripts"

## Personal access tokens (DevOps)
1. Create tokens following [Personal access tokens Guide](https://learn.microsoft.com/en-us/azure/devops/organizations/accounts/use-personal-access-tokens-to-authenticate?view=azure-devops&tabs=Windows)
2. Save the created token anywhere safe
3. Enter the token in "accToken.py" token variable
For example:  token = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

## Overall Package Needed
pip install watchdog psutil tk azure-devops beautifulsoup4 selenium
