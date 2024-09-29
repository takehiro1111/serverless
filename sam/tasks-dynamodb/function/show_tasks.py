import json 
import boto3


dynamodb = boto3.resource('dynamodb')
table_name = 'tasks'
table = dynamodb.Table(table_name)

def lambda_handler(event,context):
  primary_key = event.get("pathParameters",{}).get("id")

  if not primary_key:
    return{
      'statusCode':404,
      'body':json.dumps('ID does not exist')
    }

  try:
    response = table.get_item(
      Key={
        'id': primary_key
      }
    ) 
    Item = response.get('Item')
    if not  Item:
      return {
        'statusCode':404,
        'body':json.dumps(f'Item not Found')
      }
    
  except Exception as e:
    return {
      'statusCode':500,
      'body':json.dumps(f'Error_not_found:{str(e)}')
    }
  
  return {
    'statusCode':200,
    'body':json.dumps({
      'message':f'Task Get Item Successfully!',
      'tasks': Item
    })
  }
