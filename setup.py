from azureml.core import Workspace, ComputeTarget, Datastore, Dataset

ws = Workspace.from_config()

# #alternate way to configure workspace
# ws = Workspace.get(name='0f644ff4-434a-4446-a414-16ddb2b713ee',
#                     subscription_id='rg-sbihackathon',
#                     resource_group='ml-demo-explore')
print('\n\n')
print('Compute Targets:')
for compute_name in ws.compute_targets:
    compute = ws.compute_targets[compute_name]
    # compute = ComputeTarget._get(ws, compute_name)
    print("\t",compute.name, ":", compute.type)

print('Datastores:')
for datastore_name in ws.datastores:
    # datastore = ws.datastores[datastore_name]
    datastore = Datastore.get(ws, datastore_name)
    print("\t",datastore.name, ':', datastore.datastore_type)
    
print('Datasets:')
for dataset_name in list(ws.datasets.keys()):
    dataset = Dataset.get_by_name(ws, dataset_name)
    print('\t',dataset.name)

#
# define aml compute target(s) to create
# amlcomputes = {
#     "cpu-cluster": {
#         "vm_size": "STANDARD_DS3_V2",
#         "min_nodes": 0,
#         "max_nodes": 3,
#         "idle_seconds_before_scaledown": 1200,
#     }
# }

# create aml compute targets
# for ct_name in amlcomputes:
#     if ct_name not in ws.compute_targets:
#         compute_config = AmlCompute.provisioning_configuration(**amlcomputes[ct_name])
#         ct = ComputeTarget.create(ws, ct_name, compute_config)
#         ct.wait_for_completion(show_output=True)

# from azureml.core.runconfig import RunConfiguration
# from azureml.core.compute import AmlCompute
# list_vms = AmlCompute.supported_vmsizes(workspace=ws)
# for vm in list_vms:
#     print(vm)

# compute_config = RunConfiguration()
# compute_config.target = "amlcompute"
# compute_config.amlcompute.vm_size = "STANDARD_D1_V2"
    
# from azureml.core.conda_dependencies import CondaDependencies

# dependencies = CondaDependencies()
# dependencies.add_pip_package("scikit-learn")
# dependencies.add_pip_package("numpy==1.15.4")
# compute_config.environment.python.conda_dependencies = dependencies

# -------------------------------------------------------------------------------------------------------------------------
# 1. Creating Workspace using SDK    

# 2. Creating Cpmoute Instance using SDK
"""
OFFICIAL STEPS TO CREATE COMPUTE INSTANCE

Creating a compute instance is a one time process for your workspace. You can reuse the compute as a development workstation or as a compute target for training. You can have multiple compute instances attached to your workspace.

https://learn.microsoft.com/en-us/azure/machine-learning/how-to-create-manage-compute-instance?view=azure-ml-py&tabs=python 

"""
# get a handle to the workspace
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential

# #details of your AML workspace
subscription_id = "<SUBSCRIPTION_ID>"
resource_group = "<RESOURCE_GROUP>"
workspace = "<AML_WORKSPACE_NAME>"

ml_client = MLClient(
    DefaultAzureCredential(), subscription_id, resource_group, workspace
)
# --------------------------------------------------------------------
from azure.ai.ml.entities import ComputeInstance, AmlCompute
import datetime
# Compute Instances need to have a unique name across the region.
# Here we create a unique name with current datetime
# setting up compute instace unique name with datetime
ci_basic_name = "buf-basic-ci" + datetime.datetime.now().strftime("%Y%m%d%H%M")
# --------------------------------------------------------------------
# creating compute intsance schedule
from azure.ai.ml.constants import TimeZone
from dateutil import tz
from azure.ai.ml.entities import ComputeSchedules, ComputeStartStopSchedule, RecurrencePattern, RecurrenceTrigger

mytz = tz.gettz("Asia/Kolkata")
now = datetime.datetime.now(tz = mytz)
starttime = now + datetime.timedelta(minutes=25)

triggers = RecurrenceTrigger(frequency="day", interval=1, schedule=RecurrencePattern(hours=17, minutes=30))
myschedule = ComputeStartStopSchedule(start_time=starttime, time_zone=TimeZone.INDIA_STANDARD_TIME, trigger=triggers, action="Stop")
com_sch = ComputeSchedules(compute_start_stop=[myschedule])
# --------------------------------------------------------------------
# creating compute instace with schedule
ci_basic = ComputeInstance(name=ci_basic_name, size="Standard_D2a_v4", schedules=com_sch, idle_time_before_shutdown_minutes=90)
ml_client.begin_create_or_update(ci_basic).result()