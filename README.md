# Build jenkins job from GitHub Action :rocket:

This action creates/triggers a Jenkins job, waits for it to finish, and allows you to pass job parameters.
This action also supports HTTPS and a custom port for Jenkins.

## Inputs

### `jenkins-token`

Your Jenkins token. See [this post](https://stackoverflow.com/questions/45466090/how-to-get-the-api-token-for-jenkins#45466184) for information on how to generate one

**Required**
 
### `jenkins-url`

The URL should look like this: `github.com` and not `https://github.com` or `github.com:8080`

**Required** 

### `jenkins-user`

The Jenkins user to use

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

The jenkins server port, the default port for HTTP (non-secure) is 80 and 443 for HTTPS (secure)

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
