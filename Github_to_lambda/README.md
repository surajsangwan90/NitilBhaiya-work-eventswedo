# github-to-lambda Function Deploy.
Step 1: make a repository on github and Create a lambda function with the same name on git hub
step 2: Clone a repository in your directory **clone (path of github repository)**
Step 3: Use VS Code, write Lambda file by the name of **lambda_function.py** and function name by the **lambda_handler**
Step 4: add all the dependencies in a file **requirements.txt**
step 5: Add a file **buildspec.yml**
in this step, we have to write down all the commands in three phase: Installation(Pre-Build), Build, and Post Build
**version: 0.2
batch:
  fast-fail: false
phases:
  install: 
    runtime-versions:
      python: 3.8
    commands: 
      - echo "installing dependencies...."
      - pip install -r requirements.txt -t lib       #(Install all the dependencies and save in to the lib folder)
  build: 
    commands:
      - echo "zippling deployment package.."
      - cd lib
      - zip -r ../deployment_package.zip .           #(Create a zip folder) 
      - cd ..
      - zip -g deployment_package.zip Pandas.py      #(Add the Pandas.py file to the root of the .zip file.)
  post_build:
    commands:
      - echo "Updating lambda function.."
      - aws lambda update-function-code --function-name github-to-lambda --zip-file fileb://deployment_package.zip  #(Deploy .zip file to the function)
      - echo "Successful Done!!"**
 
 Step 6: Add all file in a git hub **git add .**
 Step 7: git commit -am "message"
 Step 8: git push origin main
 Step 9: create a codebuild file and add connect github with them.
 Step 10. Build started
