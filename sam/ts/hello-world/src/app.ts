import { APIGatewayProxyEvent, APIGatewayProxyResult } from 'aws-lambda';

/**
 *
 * Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format
 * @param {Object} event - API Gateway Lambda Proxy Input Format
 *
 * Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
 * @returns {Object} object - API Gateway Lambda Proxy Output Format
 *
 */

export const lambdaHandler = async (event: APIGatewayProxyEvent): Promise<APIGatewayProxyResult> => {
    // if (!event.body) {
    //     return {
    //         statusCode: 400,
    //         body: JSON.stringify({
    //             message: "Body is required"
    //         })
    //     }
    // }

    // const uppercaseBody = event.body.toUpperCase();
    const message = "hello ts world!".toUpperCase();

    return {
        statusCode: 200,
        body: JSON.stringify({
            // uppercase: uppercaseBody,
            message: message
        })
    }
};

