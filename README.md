# sie-backend

## Cloud Functions Tutorial 

https://cloud.google.com/functions/docs/first-python

## Setup development environment

* ### Clone the repository 
    

* ### Installing dependencies
    

* ### Installing Google SDK
    

* ### Deploying function to Google Cloud
    


## Branching and Merging

When working out on a new feature or fix, checkout out to the `master` branch and pull the new code from the remote repository:

```
$ git checkout master
$ git pull
```

Once you do this, create a new branch by running

```
$ git checkout -b feature/PROJECT-#-short-label

OR

$ git checkout -b hotfix/PROJECT-#-short-label
```

The `PROJECT` and `#` should match the project code and Jira ticket number you are currently on, like `SIE-4-create-cloud-function`; this will let your teammates know which feature your working on and review your work against the JIRA ticket number.

When your work is ready, open a PR into `master` and select __<u>at least one teammate</u>__ (ideally it should be the issue reporter) to review your work. Please format the PR title like this: `SIE-XX Description`, this will link your PR to the corresponding JIRA task. If you run into conflicts, resolve them before passing your work onto someone else for review. Once your PR has been approved, it can be merge into the `master` branch and be integrated into the code base.

Whenever a PR is approved, make sure you delete your branch to keep the repo clean and organized.

Try to keep your PR short since it will be faster and easier for the reviewer to give appropriate feedback. Otherwise try to divide the task into sub tasks and follow.


## Code Review guidelines

Reviewers are expected to actually take time to inspect the reviewee's work and flag any potential issue and/or oversight included in the branch. Similarly reviewees are expected to aknowledge any feedback and make adjustments accordingly. Since the PR might be acting as a blocker for other team members, please be mindful and do code reviews as soon as possible (ideally within 24 hours).


