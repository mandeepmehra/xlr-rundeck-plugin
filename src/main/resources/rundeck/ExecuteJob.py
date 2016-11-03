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

# Find the job in rundeck
job    = rundeck.findJob(rundeckProject, rundeckJobGroup, rundeckJobName)
runJob = RunJobBuilder.builder().setJobId(job.id).setOptions(jobOptions.toProperties()).build()


# Either wait for execution or fire and forget
if rundeckdWaitForJob == True :
  execution           = rundeck.runJob(runJob)
  rundeckJobStatus    = execution.status.toString()
  rundeckJobDuration  = execution.duration
  print "Exececution of job %s succeeeded" % rundeckJobName

  # Task should fail if output is not SUCCEEDED
  if execution.status != RundeckExecution.ExecutionStatus.SUCCEEDED:
     raise TypeError("Job %s execution failed" % rundeckJobName)

else:
   execution = rundeck.triggerJob(runJob)
   rundeckJobStatus   = "Execution started, check status at : %s" % execution.url
   rundeckJobDuration = -1
   print rundeckJobStatus     

