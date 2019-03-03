[![Build Status](https://travis-ci.com/shogo82148/cfn-json-string-macro.svg?branch=master)](https://travis-ci.com/shogo82148/cfn-json-string-macro)

# cfn-json-string-macro
A CloudFormation Macro that converts a JSON to a string

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
      Text:
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
        LifecyclePolicyText: !GetAtt LifecyclePolicy.Text
```

## Usage

### Deploy CloudFormation Macro into Your Account

You can deploy cfn-json-string-macro from [AWS Serverless Application Repository](https://serverlessrepo.aws.amazon.com/applications/arn:aws:serverlessrepo:us-east-1:445285296882:applications~cfn-json-string-macro).
Open it and click the deploy button.

### Write Your Templates

```yaml
AWSTemplateFormatVersion: 2010-09-09
Transform: JSONString # add "JSONString" to the Transform section

Resources:
  JSON:
    Type: JSON::String # specify "JSON::String"
    Properties:
      Text:
        AcountId: !Ref AWS::AccountId
        Region: !Ref AWS::Region
        StackId: !Ref AWS::StackId

Outputs:
  JSON:
    # Get JSON string as an attribute
    Value: !GetAtt JSON.Text
```
