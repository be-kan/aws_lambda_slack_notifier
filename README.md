# aws_lambda_slack_notifier
slackのslash commandからAWS lambda使って色々してみる

# 手順
* slash commandの登録
  * Lambdaを起動するURLを用意していない状態なら、適当なURLを入れておく。
  * 登録の際のTokenをメモしておく
* KMSの設定
  * AWS IAMの設定から、暗号化キーを作成
  * AWS CLIからslash commandのtokenを暗号化
  * `aws kms encrypt --key-id alias/[暗号化キーのエイリアス] --plaintext=[トークン] --profile [暗号化キーで暗号化できるユーザー]`
  * 暗号化したTokenをメモしておく（CiphertextBlobの値）
  * Tokenを復号化できるロールを作成
* Lambda関数の作成
  * https://github.com/be-kan/aws_lambda_slack_notifier/blob/master/index.py 参考
  * 環境変数に、暗号化したキーなどを登録
  * Tokenを復号化できるロールを指定
* APIの用意
  * API Gatewayにて、リソースとメソッド（POST）の作成
  * slackからのリクエストをマッピングする
  * 作成したメソッドをLambdaのトリガにする
  * デプロイして、呼び出しURLをメモ
  * URLをskash commandに登録
