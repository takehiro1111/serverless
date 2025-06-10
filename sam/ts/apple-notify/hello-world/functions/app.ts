import { APIGatewayProxyHandler, APIGatewayProxyEvent } from 'aws-lambda';
import axios from 'axios';

// App Store ConnectからのWebhookペイロードの型（主要なもののみ）
interface AppStoreNotification {
    notificationType: string;
    payload: {
        data: {
        type: string;
        id: string;
        attributes: {
            status: string; // 例: 'READY_FOR_SALE', 'REJECTED'
        };
        relationships: {
            app: {
            data: {
                type: 'apps';
                id: string; // App ID
            };
            };
        };
        };
        included?: Array<{ // includedにアプリ情報が含まれることが多い
        type: 'apps';
        id: string;
        attributes: {
            name: string;
            bundleId: string;
        };
        }>;
    };
}

export const handler: APIGatewayProxyHandler = async (event: APIGatewayProxyEvent) => {
  const { SLACK_WEBHOOK_URL } = process.env;
  if (!SLACK_WEBHOOK_URL) {
    console.error('FATAL: SLACK_WEBHOOK_URL environment variable is not set.');
    return { statusCode: 500, body: 'Internal Server Error: Webhook URL not configured.' };
  }

  if (!event.body) {
    console.warn('Request received without a body.');
    return { statusCode: 400, body: 'Bad Request: No body found.' };
  }

  try {
    const notification: AppStoreNotification = JSON.parse(event.body);

    const { status } = notification.payload.data.attributes;
    const appId = notification.payload.data.relationships.app.data.id;
    const appInfo = notification.payload.included?.find(item => item.type === 'apps' && item.id === appId);
    const appName = appInfo ? appInfo.attributes.name : `App ID: ${appId}`;

    const statusEmoji = {
      'READY_FOR_SALE': '✅',
      'REJECTED': '❌',
      'IN_REVIEW': '⏳',
      'PENDING_DEVELOPER_RELEASE': '⏰',
    }[status] || '🔔';

    const message = {
      text: `${statusEmoji} App Store Connect Status Update`,
      attachments: [
        {
          color: status === 'REJECTED' ? '#ff0000' : '#36a64f',
          fields: [
            {
              title: "App Name",
              value: appName,
              short: true,
            },
            {
              title: "New Status",
              value: status,
              short: true,
            },
          ],
          ts: Math.floor(Date.now() / 1000).toString(),
        },
      ],
    };

    await axios.post(SLACK_WEBHOOK_URL, message);

    return {
      statusCode: 200,
      body: JSON.stringify({ status: 'success', message: 'Notification sent.' }),
    };
  } catch (error) {
    console.error('Error processing request:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({ status: 'error', message: 'Failed to process request.' }),
    };
  }
};
