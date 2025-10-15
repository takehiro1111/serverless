import middy from '@middy/core'
import ssm   from '@middy/ssm'

import { errorHandler } from '@libs/middleware/errorHandler'

export const middyfy = (handler) => {
  return middy(handler)
    .use(ssm({
      fetchData: {
        GITHUB_APP_ID:            '/common/prod/deploy/github_app_id',
        GITHUB_SECRET_KEY:        '/common/prod/deploy/github_secret_key',
        SLACK_BOT_TOKEN:          '/common/prod/deploy/slack_bot_token',
        SLACK_BOT_TOKEN_OF_ALERT: '/common/prod/deploy/slack_bot_token_of_alert',
        SLACK_VERIFICATION_TOKEN: '/common/prod/deploy/slack_verification_token'
      },
      setToContext: true
    }))
    .use(errorHandler())
}
