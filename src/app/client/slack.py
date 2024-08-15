import requests

from app.core.logger import my_logger
from app.core.settings import my_settings


def post_alarm(info, thread_ts=None, input0=None, output0=None):
    try:
        text = f"[SCP-AISLIDER-APP] {my_settings.my_name} {my_settings.my_stage} ({my_settings.aws.region}) \n{info}"
        if input0 is not None:
            text += f"\ni: {input0}"
        if output0 is not None:
            text += f"\no: {output0}"

        header = {'Content-Type': 'application/x-www-form-urlencoded'}  # application/json
        body = {
            'channel': my_settings.slack.slack_channel,
            'token': my_settings.slack.slack_token,
            'text': text
        }
        if thread_ts is not None:
            body['thread_ts'] = thread_ts
        response = requests.post('https://slack.com/api/chat.postMessage', headers=header, data=body, timeout=10)
        if response is None:
            raise Exception(f"response is None")
        if response.status_code != requests.codes.ok:
            raise Exception(f"response is {response.status_code} {response.headers} {response.text} {response.content}")
        response = response.json()
        response = response['ts'] if isinstance(response, dict) and 'ts' in response else None
    except Exception as e:
        my_logger.error(f"slack.post_alarm() : e={e}")
        return None
    return response
