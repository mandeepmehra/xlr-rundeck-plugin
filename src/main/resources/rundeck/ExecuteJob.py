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



# Validate job exist and get the UUID
# Not using findjobs as that matches a substring and retutns first match... !
# Job names are not unique hence iterating through list udner the project and finding the matched one

jobToRun  = None
jobs      = rundeck.getJobs(rundeckProject);

if rundeckJobGroup:
   rdjobFullName = "%s%s%s" % (rundeckJobGroup,"/",rundeckJobName)
else:
    rdjobFullName = rundeckJobName


for job in jobs:
    if job.getFullName() == rdjobFullName:
       jobToRun = job
       break

if jobToRun is None:
   raise TypeError("No job found with name:\"%s\" in project: \"%s\" \n" % (rdjobFullName, rundeckProject))
else:
     print "Job found: %s in project: %s \n" % (jobToRun.getFullName(),rundeckProject)

# Set the Job Options
rundeckJobName = jobToRun.getFullName()
runJob         = RunJobBuilder.builder().setJobId(jobToRun.id).setOptions(jobOptions.toProperties()).build()


# Either wait for execution or fire and forget
if rundeckdWaitForJob == True :
  execution           = rundeck.runJob(runJob)
  rundeckJobStatus    = execution.status.toString()
  rundeckJobDuration  = execution.duration
  rundeckExecutionId  = execution.id
  print "Execution #%s for job %s succeeded\n" % (rundeckExecutionId, rundeckJobName)

  # Task should fail if output is not SUCCEEDED
  if execution.status != RundeckExecution.ExecutionStatus.SUCCEEDED:
     raise TypeError("Execution #%s for job %s FAILED\n" % (rundeckExecutionId, rundeckJobName))

else:
   execution = rundeck.triggerJob(runJob)
   rundeckJobStatus   = "%s\n" % execution.url
   rundeckJobDuration = -1
   rundeckExecutionId = execution.id
   print rundeckJobStatus     


