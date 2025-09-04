
UNAME=$(uname)

cd $SERVER_WWW_ROOT
tar zxvf /tmp/html.*.tar.gz

rm -rf /tmp/.env /tmp/html.*.tar.gz
