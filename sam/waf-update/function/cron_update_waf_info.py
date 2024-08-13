import boto3
import json
import os

def lambda_handler(event, context):
    # 作業ディレクトリ
    workdir = "/tmp/events"
    os.makedirs(workdir, exist_ok=True)
    
    wafv2_client = boto3.client('wafv2', region_name='us-east-1')
    
    # WAFv2 の Web ACL をリストする
    response = wafv2_client.list_web_acls(Scope='CLOUDFRONT')
    
    for web_acl in response.get('WebACLs', []):
        name = web_acl['Name']
        web_acl_id = web_acl['Id']
        print(f"Processing Web ACL: {name} (ID: {web_acl_id})")
        
        # 各 Web ACL の詳細を取得して JSON ファイルに保存する
        web_acl_details = wafv2_client.get_web_acl(
            Name=name,
            Scope='CLOUDFRONT',
            Id=web_acl_id
        )
        
        # Web ACL のルールを名前でマッピングする
        web_acl_details['WebACL']['Rules'] = {
          rule['Name']: rule for rule in web_acl_details['WebACL']['Rules']
        }
        
        # Web ACL のスコープを CLOUDFRONT に固定する
        web_acl_details['WebACL']['Scope'] = 'CLOUDFRONT'
        
        # JSON ファイルに書き込む
        file_path = os.path.join(workdir, f"{name}.json")
        with open(file_path, 'w') as f:
            json.dump(web_acl_details, f, indent=2)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Processing completed successfully.')
    }
