#!/bin/bash -eu

# .env がある場所で実行すること
if [ ! -f ./.env ]; then
    echo ".env file not found!"
    exit 1
fi

# サーバ側デプロイ用スクリプト名
server_side_deploy_script="/server-side-deploy.sh"

# .env ファイルを読み込み、環境変数にセットするため
# ハイフン前後のスペースを除去し、テンポラリディレクトリに保存
temp_dir=$(mktemp -d)
cat ./.env | perl -lne 'print "export $1=\"$2\"" if ( /^([^=\s]+)\s*=\s*(.*)$/ )' > $temp_dir/.env

# 環境変数を読み込む
source $temp_dir/.env

# index.html より新しいファイルの tar ball を作る
# 新しい記事を追加すれば、かならず index.html も更新される
# (ただし、CSSやJavaScript を買えたときは動作しない……)
timestamp=$(date +%Y%m%d%H%M%S)
tarball=$temp_dir/html.${timestamp}.tar.gz
tar zcvf --newer-file $WWW_ROOT/index.html $tarball -C $WWW_ROOT .

# 変更したファイルの tar ball とサーバ側デプロイ用スクリプトを転送
# .env ファイルも転送する
scp -r $tarball $SERVER_NAME:/tmp/
scp "./bin/$server_side_deploy_script" $SERVER_NAME:/tmp/
scp "$temp_dir/.env" $SERVER_NAME:/tmp/

# サーバ側デプロイ用スクリプトの実行と削除
ssh $SERVER_NAME "bash -eu /tmp/$server_side_deploy_script; rm -rf /tmp/$server_side_deploy_script"

# ローカル側の一時ディレクトリを削除
# trap で正常終了時と異常終了時の両方で削除するようにする
trap "rm -rf $temp_dir" EXIT ERR
