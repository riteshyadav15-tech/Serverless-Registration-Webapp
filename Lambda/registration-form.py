import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('registration-table')

def lambda_handler(event, context):
    # Print the event to inspect its structure
    print("Event: ", event)
    
    # Check if the event contains a body (e.g., in case of an API Gateway request)
    if 'body' in event:
        # Parse the body from the string format to a dictionary
        body = json.loads(event['body'])
    else:
        # If there is no body, assume the event is already a dictionary
        body = event

    # Check if all required fields are present
    required_fields = ['email', 'name', 'phone', 'password']
    for field in required_fields:
        if field not in body:
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'message': f"Missing {field} in the request"})
            }

    # Create new item in DynamoDB table
    try:
        response = table.put_item(
            Item={
                'email': body['email'],
                'name': body['name'],
                'phone': body['phone'],
                'password': body['password']
            }
        )
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'message': 'Failed to register', 'error': str(e)})
        }

    # Return response
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({'message': 'Registration successful'})
    }
