import subprocess as sp , sys
from datetime import datetime
import requests
import time 

# Get the all arguments
username=sys.argv[1]
password=sys.argv[2]
tenantid=sys.argv[3]
key=sys.argv[4]
val=sys.argv[5]
webhooks_url=sys.argv[6]
q1="[?tags.{}==\`{}\`].name".format(key,val)
q2="[].name"

main_output=('Azure machines list\n\n')
main_output+=(f"VM Name \t Resource Group \t Age \n")
def auth():
    authoutput=sp.getstatusoutput("az login --service-principal -u {} -p {} --tenant {}".format(username,password,tenantid))
    return authoutput

def filter():
     str=sp.getoutput("az vm list --query {} -o tsv".format(q1))
     l=list(str.split())
     return l

    
    
    
def list_all_vm():
     str=sp.getoutput("az vm list --query {} -o tsv".format(q2))
     l=list(str.split())
     return l
time.sleep(20)
vm_list=list_all_vm()
l=filter()
filter_array= [item for item in vm_list if item not in l]


def time_format(create_timestamp):
    print(type(create_timestamp))
    current_time=datetime.now()
    #print(current_time)
    print(create_timestamp,current_time)
    right_format=current_time-(datetime.strptime(create_timestamp[:19],'%Y-%m-%dT%H:%M:%S'))
    return right_format

authout=auth()
if(authout[0]==0):
    print("Authentication is successed")
    time.sleep(30)
    print("List of All Vm \n")
    for i in range(len(filter_array)):
        q3="[?name==\`{}\`].resourceGroup".format(filter_array[i])
        q4="[?name==\`{}\`].timeCreated".format(filter_array[i])
        rg=sp.getoutput("az vm list --query {}  -o tsv".format(q3))
        tm=sp.getoutput("az vm list --query {}  -o tsv".format(q4))
        time=time_format(tm)
        print(f"Resoure Group of {filter_array[i]} is :{rg}")
        print(f"Time created : {time}")
        main_output+=(f'{filter_array[i]} : \t {rg} : \t {time}\n\n')
    print(main_output)
    resp = requests.post(
                webhooks_url,
                data={
                    'content':"```\n"+main_output+"\n```",
                },
            )    
else:
    print("Authentication failed",authout[1])
