#!/bin/bash

# BACKEND STACK
STACK_NAME="terraform-backend"
TEMPLATE="./infrastructure/cloudFormation/tf-backend.yaml"
S3_BUCKET="tf-state-backend-tech42"
DYNAMO_TABLE="tf-state-lock"

# OIDC STACK
OIDC_STACK_NAME="oidc-provider-stack"
OIDC_TEMPLATE="./infrastructure/cloudFormation/oidc-role.yaml"
REPOS=("repo:rcanelav/realtime-stock-prices:*")
REPO_LIST=$(IFS=','; echo "${REPOS[*]}") # Convert array to comma-separated string


create_stack() {
  echo "Creating CloudFormation stack..."
  aws cloudformation create-stack \
    --stack-name $STACK_NAME \
    --template-body file://$TEMPLATE \
    --parameters ParameterKey=S3BucketName,ParameterValue="$S3_BUCKET" ParameterKey=DynamoDBTableName,ParameterValue="$DYNAMO_TABLE"
  aws cloudformation wait stack-create-complete --stack-name $STACK_NAME
  echo "Stack created successfully."
  read -p "Press enter to continue..."
}

update_stack() {
  echo "Updating CloudFormation stack..."
  aws cloudformation update-stack \
    --stack-name $STACK_NAME \
    --template-body file://$TEMPLATE \
    --parameters ParameterKey=S3BucketName,ParameterValue="$S3_BUCKET" ParameterKey=DynamoDBTableName,ParameterValue="$DYNAMO_TABLE"
  echo "Stack update initiated."
  read -p "Press enter to continue..."
}

delete_stack() {
  echo "Deleting CloudFormation stack..."
  aws cloudformation delete-stack --stack-name $STACK_NAME
  aws cloudformation wait stack-delete-complete --stack-name $STACK_NAME
  echo "Stack deleted successfully."
  read -p "Press enter to continue..."
}

get_outputs() {
  echo "Fetching stack outputs..."
  aws cloudformation describe-stacks \
    --stack-name $STACK_NAME \
    --query "Stacks[0].Outputs"
  read -p "Press enter to continue..."
}

create_oidc_stack() {
  echo "Creating OIDC CloudFormation stack with repositories: $REPO_LIST"
  aws cloudformation create-stack \
    --stack-name $OIDC_STACK_NAME \
    --template-body file://$OIDC_TEMPLATE \
    --parameters 'ParameterKey=Repos,ParameterValue="'"$REPO_LIST"'"' \
    --capabilities CAPABILITY_IAM
  aws cloudformation wait stack-create-complete --stack-name $OIDC_STACK_NAME
  echo "OIDC stack created successfully."
 read -p "Press enter to continue..."
}

update_oidc_stack() {
  echo "Updating OIDC CloudFormation stack with repositories: $REPO_LIST"
  aws cloudformation update-stack \
    --stack-name $OIDC_STACK_NAME \
    --template-body file://$OIDC_TEMPLATE \
    --parameters 'ParameterKey=Repos,ParameterValue="'"$REPO_LIST"'"' \
    --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM
  echo "OIDC stack update initiated."
  read -p "Press enter to continue..."
}

case $1 in
  create)
    create_stack
    ;;
  update)
    update_stack
    ;;
  delete)
    delete_stack
    ;;
  outputs)
    get_outputs
    ;;
  oidc)
    create_oidc_stack
    ;;
  oidc-update)
    update_oidc_stack
    ;;
  *)
    echo "Usage: $0 {create|update|delete|outputs}"
    ;;
esac
