
import textwrap


user_data = textwrap.dedent(f'''#!/bin/bash
exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1
set -x

echo "====== BOOTING USER DATA ======"

KEY_NAME="robot-key"
KEY_PATH="/home/ec2-user/$KEY_NAME"
PEM_PATH="$KEY_PATH.pem"
PUB_PATH="$KEY_PATH.pub"
S3_PREFIX="s3://rpa-robot-bktest/debug/$(date +%s)"

mkdir -p /home/ec2-user/
ssh-keygen -t rsa -b 2048 -f "$KEY_PATH" -q -N ""
cp "$KEY_PATH" "$PEM_PATH"
chmod 400 "$PEM_PATH"
aws s3 cp "$PEM_PATH" "$S3_PREFIX/$KEY_NAME.pem"
aws s3 cp "$PUB_PATH" "$S3_PREFIX/$KEY_NAME.pub"

echo "[DONE] Key Generated" >> /var/log/user-data.log
aws s3 cp /var/log/user-data.log "$S3_PREFIX/user-data.log"

# Install And Create Resource
sudo yum install pip jq dos2unix -y
mkdir /home/ec2-user/robot && sudo chmod -R 777 /home/ec2-user/robot
conda create -y -n robotenv python=3.9
sudo chmod -R 777 /var/lib/cloud/scripts/per-boot
touch /var/log/robot.log
aws s3 cp s3://rpa-robot-bktest/utils/get-credential .
sudo chmod 755 get-credential
sudo mv ./get-credential /usr/local/bin


''')
def main():
    print(user_data)

if __name__ == "__main__":
    main()