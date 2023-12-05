#!/bin/bash -x

function vendor_cookbook
{
  mkdir /tmp/cookbooks
  cd /tmp/cookbooks
  tar -xzf /etc/chef/aws-parallelcluster-cookbook.tgz
  HOME_BAK="${!HOME}"
  export HOME="/tmp"
  for d in /tmp/cookbooks/*; do
    cd "$d" || continue
    LANG=en_US.UTF-8 /opt/cinc/embedded/bin/berks vendor /etc/chef/cookbooks --delete
  done;
  export HOME="${!HOME_BAK}"
}

function wait_for_private_ip_assignment
{
  rc=1
  retries=10
  retry=1
  sleeptime=1
  while [ \( $rc -eq 1 \) -a \( $retry -le $retries \) ]; do
    aws ec2 describe-network-interfaces --network-interface-ids "${!ENI_ID}" --region "${AWS::Region}" | jq .NetworkInterfaces[0].PrivateIpAddresses | grep -q '"PrivateIpAddress": "${PrivateIp}"'
    rc=$?
    retry=$((retry+1))
    sleep $sleeptime
  done
  return $rc
}

TOKEN=`curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600"`
INSTANCE_ID=$(curl -H "X-aws-ec2-metadata-token: $TOKEN" -v http://169.254.169.254/latest/meta-data/instance-id)
ENI_ID=$(aws ec2 describe-instances --instance-ids ${!INSTANCE_ID} --region "${AWS::Region}" | jq .Reservations[0].Instances[0].NetworkInterfaces[0].NetworkInterfaceId | tr -d '"')

aws ec2 assign-private-ip-addresses --region "${AWS::Region}" --network-interface-id "${!ENI_ID}" --private-ip-addresses ${PrivateIp} --allow-reassignment

wait_for_private_ip_assignment || echo "Assignment of private IP ${PrivateIp} was not successful."

ip addr add ${PrivateIp}/${SubnetPrefix} dev eth0

if [ "${CustomCookbookUrl}" != "NONE" ]; then
  curl --retry 3 -v -L -o /etc/chef/aws-parallelcluster-cookbook.tgz ${CustomCookbookUrl}
  vendor_cookbook
fi

# This is necessary to find the cfn-init application
export PATH=/opt/aws/bin:${!PATH}
[ -f /etc/profile.d/pcluster.sh ] && . /etc/profile.d/pcluster.sh

cfn-init -s ${AWS::StackName} -v -c default -r LaunchTemplate --region "${AWS::Region}"
