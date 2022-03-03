#!/bin/bash

# set variables
CORE_NAME="__CORE_NAME__"
REGION="__REGION__"
POLICY="__POLICY__"

# updates
sudo apt-get update
sudo apt install default-jre -y
sudo apt install unzip -y
sudo apt install python3-pip -y
sudo apt install awscli -y
sudo apt install jq -y
pip3 install awscrt
pip3 install awsiotsdk

# download and unpack dependencies
curl -s https://d2s8p88vqu9w66.cloudfront.net/releases/greengrass-nucleus-latest.zip > greengrass-nucleus-latest.zip \
&& unzip greengrass-nucleus-latest.zip -d GreengrassCore

# install greengrass
sudo -E java -Droot="/greengrass/v2" -Dlog.store=FILE -jar ./GreengrassCore/lib/Greengrass.jar \
--aws-region ${REGION} \
--thing-name ${CORE_NAME} \
--thing-group-name GreengrassQuickStartGroup \
--component-default-user ggc_user:ggc_group \
--provision true --setup-system-service true --deploy-dev-tools true

# generate certificate for device
mkdir /home/ubuntu/certs
ARN=$(aws iot create-keys-and-certificate --set-as-active --certificate-pem-outfile /home/ubuntu/certs/certificate.pem.crt --public-key-outfile /home/ubuntu/certs/public.pem.key --private-key-outfile /home/ubuntu/certs/private.pem.key --region eu-west-2 | jq -r '.certificateArn')

# debug vars
echo "Region: ${REGION} Device: ${CORE_NAME} Cert IAM Policy: ${POLICY} ARN: ${ARN}" > /home/ubuntu/vars

# attach to thing
aws iot attach-thing-principal \
--thing-name ${CORE_NAME} \
--principal ${ARN} \
--region ${REGION}
# attach existing policy to certificate
aws iot attach-policy \
--target ${ARN} \
--policy-name=${POLICY} \
--region ${REGION}


# get example content from s3
aws s3 cp s3://smf-shared-resources/generate_data.py /home/ubuntu
aws s3 cp s3://smf-shared-resources/monitor_temp.py /home/ubuntu
aws s3 cp s3://smf-shared-resources/AmazonRootCA1.pem /home/ubuntu/certs

sudo chmod -R 777 /home/ubuntu/certs

# run generate data script in background
nohup python3 /home/ubuntu/generate_data.py &
