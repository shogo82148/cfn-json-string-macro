[![test](https://github.com/shogo82148/cfn-json-string-macro/actions/workflows/test.yml/badge.svg)](https://github.com/shogo82148/cfn-json-string-macro/actions/workflows/test.yml)

# DEPRECATED: cfn-json-string-macro

A CloudFormation Macro that converts a JSON to a string.

DEPRECATED: [`AWS::LanguageExtensions` transform](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-languageextension-transform.html) provides same function.
Please use [`Fn::ToJsonString` intrinsic function](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-ToJsonString.html) instead of cfn-json-string-macro.

## Motivation

Some AWS CloudFormation properties need to be specified the JSON as text.
For example, [LifecyclePolicyText](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-repository-lifecyclepolicy.html#cfn-ecr-repository-lifecyclepolicy-lifecyclepolicytext)
of [Amazon Elastic Container Registry Repository LifecyclePolicy](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-repository-lifecyclepolicy.html)
is a JSON, but we need to specify it as text.

```yaml
AWSTemplateFormatVersion: 2010-09-09
Resources:
  Repository:
    Type: AWS::ECR::Repository
    Properties:
      RepositoryName: awesome-application
      # a policy that expires untagged images older than 14 day
      LifecyclePolicy:
        LifecyclePolicyText: |
          {
              "rules": [
                  {
                      "rulePriority": 1,
                      "description": "Expire images older than 14 days",
                      "selection": {
                          "tagStatus": "untagged",
                          "countType": "sinceImagePushed",
                          "countUnit": "days",
                          "countNumber": 14
                      },
                      "action": {
                          "type": "expire"
                      }
                  }
              ]
          }
```

It may break syntax check and highlighting of editors.

```yaml
AWSTemplateFormatVersion: 2010-09-09
Transform: JSONString
Resources:
  # a policy that expires untagged images older than 14 day
  LifecyclePolicy:
    Type: JSON::String
    Properties:
      Value:
        rules:
          - rulePriority: 1 # now we can add comments in a policy!
            description: Expire images older than 14 days
            selection:
              tagStatus: untagged
              countType: sinceImagePushed
              countUnit: days
              countNumber: 14
            action:
              type: expire

  Repository:
    Type: AWS::ECR::Repository
    Properties:
      RepositoryName: awesome-application
      LifecyclePolicy:
        LifecyclePolicyText: !GetAtt LifecyclePolicy.Value
```

-----

DEPRECATED: I recommend you to migrate to `Fn::ToJsonString`.
It is officially supported by AWS.

```yaml
AWSTemplateFormatVersion: 2010-09-09
Transform: AWS::LanguageExtensions
Resources:
  LifecyclePolicy:
    Type: JSON::String
    Properties:
      Value:

  Repository:
    Type: AWS::ECR::Repository
    Properties:
      RepositoryName: awesome-application
      LifecyclePolicy:
        LifecyclePolicyText:
          # a policy that expires untagged images older than 14 day
          Fn::ToJsonString:
            rules:
              - rulePriority: 1 # now we can add comments in a policy!
                description: Expire images older than 14 days
                selection:
                  tagStatus: untagged
                  countType: sinceImagePushed
                  countUnit: days
                  countNumber: 14
                action:
                  type: expire
```

## Usage

### Deploy CloudFormation Macro into Your Account

[cfn-json-string-macro is available on AWS Serverless Application Repository](https://serverlessrepo.aws.amazon.com/applications/us-east-1/445285296882/cfn-json-string-macro).
[Deploy on AWS Management Console](https://console.aws.amazon.com/lambda/home?#/create/app?applicationId=arn:aws:serverlessrepo:us-east-1:445285296882:applications/cfn-json-string-macro),
or use the following [AWS SAM (AWS Serverless Application Model)](https://aws.amazon.com/serverless/sam/) snippet.

```yaml
cfnjsonstringmacro:
  Type: AWS::Serverless::Application
  Properties:
    Location:
      ApplicationId: arn:aws:serverlessrepo:us-east-1:445285296882:applications/cfn-json-string-macro
      SemanticVersion: 0.0.8
    Parameters:
      # The name of the cloudformation macro.
      MacroName: "JSONString"
      # The function name that handles cloudformation macros.
      # If it is empty, the name is auto generated.
      MacroFunctionName: ""
      # the function name that handles cloudformation custom resources.
      # If it is empty, the name is auto generated.
      ResourceFunctionName: ""
```

### Write Your Templates

```yaml
AWSTemplateFormatVersion: 2010-09-09
Transform: JSONString # add "JSONString" to the Transform section

Resources:
  JSON:
    Type: JSON::String # specify "JSON::String"
    Properties:
      Value:
        AccountId: !Ref AWS::AccountId
        Region: !Ref AWS::Region
        StackId: !Ref AWS::StackId

Outputs:
  JSON:
    # Get JSON string as an attribute
    Value: !GetAtt JSON.Value
```

```bash
aws cloudformation deploy --template-file example.yaml --stack-name json-macro-example CAPABILITY_AUTO_EXPAND
```

## Other Deployment Methods

### Deploy from GitHub Repository

Clone the repository, package the sources, and deploy.

```bash
git clone git@github.com:shogo82148/cfn-json-string-macro.git
cd cfn-json-string-macro
make all
aws cloudformation package --template-file template.yml --s3-bucket $YOUR_BUCKET_NAME --output-template-file packaged.yaml
aws cloudformation deploy --template-file packaged.yaml --stack-name json-macro --capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND
```

### Deploy from Pre-built Packages (Legacy)

Pre-built Packages are available on `https://shogo82148-cloudformation-template-$REGION.s3.$REGION.amazonaws.com/cfn-json.string-macro/latest.yaml`,
You can deploy cfn-json-string-macro the template directly.

```bash
# deploy the latest version
aws cloudformation create-stack \
    --template-url https://shogo82148-cloudformation-template-$REGION.s3.$REGION.amazonaws.com/cfn-json.string-macro/latest.yaml \
    --stack-name json-macro \
    --capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND

# deploy the specific version
aws cloudformation create-stack \
    --template-url https://shogo82148-cloudformation-template-$REGION.s3.$REGION.amazonaws.com/cfn-json.string-macro/v0.0.8.yaml \
    --stack-name json-macro \
    --capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND

# deploy v0.0.x
aws cloudformation create-stack \
    --template-url https://shogo82148-cloudformation-template-$REGION.s3.$REGION.amazonaws.com/cfn-json.string-macro/v0.0.yaml \
    --stack-name json-macro \
    --capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND

# deploy v0.x.x
aws cloudformation create-stack \
    --template-url https://shogo82148-cloudformation-template-$REGION.s3.$REGION.amazonaws.com/cfn-json.string-macro/v0.yaml \
    --stack-name json-macro \
    --capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND
```
