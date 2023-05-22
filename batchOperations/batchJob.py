from azureml.core import Workspace
from azureml.core.webservice import BatchEndpoint

# Load workspace configuration from the config.json file in the current folder.
ws = Workspace.from_config()


# Get the batch endpoint by name
batch_endpoint = BatchEndpoint.get(ws, "my-batch-endpoint")

# Submit a batch job
job = batch_endpoint.submit_job(
input_data="https://myaccount.blob.core.windows.net/mycontainer/myinputdata.csv",
output_data="https://myaccount.blob.core.windows.net/mycontainer/myoutputdata.csv"
)

# Wait for the job to complete
job.wait_for_completion(show_output=True)