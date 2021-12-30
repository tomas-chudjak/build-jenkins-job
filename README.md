# Build jenkins job from GitHub Action :rocket:

This action builds/triggers a jenkins job, waiting it to be finished and enabling to pass job params.

## Inputs

### `jenkins-token`

**Required**
 
### `jenkins-url`

**Required** 

### `jenkins-user`

**Required** 

### `job-path`

**Required** 

E.g.
```
if job inside folder:
 "job/folder_name/job/job_name"

if job in jenkins root: 
 "job/job_name"
```

### `jenkins-port`

**Required**

### `job-params`

**Not mandatory**

Set jenkins params as JSON string:  

E.g.
```
 "{\"param1\": \"value1\", \"param2\": \"value2\"}"
``` 

### `is-secure`

**Not mandatory**

Set to true if you are trying to connect to a HTTPS server, default is false

## Outputs

###  `status/result`

* FAILURE
* SUCCESS
* ABORTED


## Example usage
```
    - name: "Trigger jenkins job"
      uses: Paloudi/build-jenkins-job@master
      with:
        jenkins-url: ${{ secrets.JENKINS_URL }}
        jenkins-port: ${{ secrets.JENKINS_PORT }}
        jenkins-token: ${{ secrets.JENKINS_TOKEN }}
        user: "jenkins-username"
        job-path: "job/folder_name/job/job_name"
        job-params: "{\"param1\": \"value1\", \"param2\": \"value2\"}"
        is-secure: true
        
    - name: Get job status
      run: echo "Job status is ${{ steps.job-build.outputs.job_status }}"
```
