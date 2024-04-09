import subprocess as sp,sys

username=sys.argv[1]
password=sys.argv[2]
tenantid=sys.argv[3]
rg=sys.argv[4]
name=sys.argv[5]


def auth():
    authoutput=sp.getstatusoutput("az login --service-principal -u {} -p {} --tenant {}".format(username,password,tenantid))
    return authoutput

 
#Function to ShutDown Vm 
def start():
    str=sp.getoutput("az aks start --resource-group {}  --name {}".format(rg,name))
    print(str)
    sp.getoutput("az aks nodepool list --resource-group {} --cluster-name {}  --query \"[?mode=='System'].count\" -o tsv").format(rg,name)
    print("Sucessfully Started")


authout=auth()
if(authout[0]==0):
    print("Authentication is successed")
    start()
else:
    print("Authentication failed",authout[1])
