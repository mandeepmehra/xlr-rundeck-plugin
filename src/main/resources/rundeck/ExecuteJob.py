from org.rundeck.api import RundeckClient
from org.rundeck.api import RunJobBuilder
from org.rundeck.api import OptionsBuilder
from org.rundeck.api.domain import RundeckExecution


# Intialize variables and objects
rdUsername  = rundeckServer['username']
rdPassword  = rundeckServer['password']
rdUrl       = rundeckServer['url']
rdAuthToken = rundeckServer['rundeckAuthToken']
jobOptions  = OptionsBuilder()
nodeFilters = OptionsBuilder()
rundeck     = None

# Build the job options 
for key,value in rundeckJobOptions.iteritems():
    jobOptions.addOption(key,value)

# Authenticate either using username/apssword or use auth token
if rdAuthToken:
     rundeck = RundeckClient.builder().url(rdUrl).token(rdAuthToken).build() 
else:
     rundeck = RundeckClient.builder().url(rdUrl).login(rdUsername, rdPassword).build()

runJob     = RunJobBuilder.builder().setJobId(rundeckJobIdentifier).setOptions(jobOptions.toProperties()).build()

# Fetch t he job details - name , group etc.
rundeckJobName = rundeck.getJob(rundeckJobIdentifier).getFullName()


# Either wait for execution or fire and forget
if rundeckdWaitForJob == True :
  execution           = rundeck.runJob(runJob)
  rundeckJobStatus    = execution.status.toString()
  rundeckJobDuration  = execution.duration
  rundeckExecutionId  = execution.id
  print "Execution #%s for job %s succeeded" % (rundeckExecutionId, rundeckJobName)

  # Task should fail if output is not SUCCEEDED
  if execution.status != RundeckExecution.ExecutionStatus.SUCCEEDED:
     raise TypeError("Execution #%s for job %s FAILED" % (rundeckJobName,rundeckExecutionId))

else:
   execution = rundeck.triggerJob(runJob)
   rundeckJobStatus   = "Execution started, check status at : %s" % execution.url
   rundeckJobDuration = -1
   rundeckExecutionId = execution.id
   print rundeckJobStatus     

