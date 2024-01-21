import subprocess as sp , sys, os
# Get the all arguments
username=sys.argv[1]
password=sys.argv[2]
tenantid=sys.argv[3]
print("Starting Automation cluster")
def auth():
    authoutput=sp.getstatusoutput("az login --service-principal -u {} -p {} --tenant {}".format(username,password,tenantid))
    return authoutput

def stop():
     str=sp.getoutput("az aks start --resource-group automation-rg --name automation-aks   --output json")
     return str



authout=auth()
if(authout[0]==0):
    print("Authentication Done")
    res=stop()
    count=sp.getoutput("az aks nodepool list --resource-group automation-rg  --cluster-name automation-aks  --query \"[?mode=='System'].count\" -o tsv") 
    print(count)
    print("Started sucessfully")
else:
    print("Authentication failed",authout[1])
