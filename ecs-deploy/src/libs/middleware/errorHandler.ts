import { WebClient } from '@slack/web-api'

export const errorHandler = () => {
  const onError = async (request) => {
    const slackClient = new WebClient(request.context.SLACK_BOT_TOKEN_OF_ALERT)

    await slackClient.chat.postMessage({
      channel: 'C032N1GK3KK', // platform channel
      blocks:  [
        {
          type: "section",
          text: { type: "plain_text", text: "ECS-Deploy-Lambda でエラーが発生しました。" }
        },
        {
          type: "section",
          text: { type: "mrkdwn", text: "```" + request.error.stack + "```" }
        }
      ]
    })
  }

  return {
    onError: onError,
  }
}
