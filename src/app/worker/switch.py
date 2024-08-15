from fastapi import HTTPException

from app.core.logger import my_logger
from app.core.settings import my_settings
from app.worker.inference.inference_worker import inject_inference_worker


def adapt(event):
    try:
        case = event['case'] if 'case' in event else None
        if case == 'post_inference':
            inference_worker = inject_inference_worker()
            inference_worker.post_inference(event['user_id'], event['slide_id'])
        else:
            raise Exception(f"else case {case}")

    except HTTPException as e:
        err = f"worker.{case}() : e={e.detail}"
        my_logger.error(err)
        raise e
    except BaseException as e:
        err = f"worker.{case}() : e={e}"
        my_logger.error(err)
        raise e
    return
