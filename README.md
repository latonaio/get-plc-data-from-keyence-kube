# get-plc-data-from-keyence-kube

キーエンス製のPLCのデータを取得するマイクロサービスです。  
本マイクロサービスを実行すると常時起動し、3秒毎にKeyencePLCの結果をkanbanに出力して次工程に渡します。  
本マイクロサービスを動作させるためには、別途ftp-kubeでftpサーバを立てることが必要です。  
（サーバ側のYAMLファイルと本レポジトリのDockerファイルで、NAME,PWを合わせます）  

## 動作環境  

OS: Linux  
CPU: ARM/AMD/Intel  

