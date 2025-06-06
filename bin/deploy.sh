#!/bin/bash

script_dir=`dirname $0`
env_file="$script_dir/../.env"
server_side_deploy_script="server-side-deploy.sh"

source $env_file

timestamp=`date +'%Y%m%D_%H%M%S'`
random_postfix=`cat /dev/urandom | LANG=C tr -c -d 'A-Za-z0-9' | head -c 8`

tmp_name="${timestamp}_${random_poxtfix}"

mkdir -p /tmp/${tmp_name}
cp -pr $HTML_DIR /tmp/${tmp_name}

tar zcvf ${tmp_name}.tar.gz /tmp/${tmp_name}

scp -r ${tmp_name}.tar.gz $SERVER_NAME:/tmp/
scp "$scrit_dir/$server_side_deploy_script" $SERVER_NAME:/tmp/

set +u
if [ "$TMP_OPTION" != "" ]; then
    DEPLOY_OPTION=$TMP_OPTION
elif [ "$DEPLOY_OPTION" = "" ]; then
    DEPLOY_OPTION=""
fi
set -u

ssh $SERVER_NAME "bash -eux /tmp/$server_side_deploy_script $DEPLOY_OPTION $tmp_name"
