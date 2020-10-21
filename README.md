# get-plc-data-from-keyence

動作するためには、ftp-kubeでftpサーバを立てることが必要

（サーバ側のYAMLファイルとこれのDockerファイルで、NAME,PWを合わせる）

実行すると常時起動し、3秒毎にKeyencePLCの結果を次工程にKanban出力する
