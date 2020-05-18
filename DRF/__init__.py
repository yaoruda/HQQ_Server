from __future__ import absolute_import, unicode_literals

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app
import logging
import os
from hqq_tool.plantform_push.huawei_push.huawei_push import HuaweiPush
from hqq_tool.plantform_push.xiaomi_push.xiaomi_push import XiaomiPush
from hqq_tool.plantform_push.oppo_push.oppo_push import OppoPush

__all__ = ('celery_app',)
logger = logging.getLogger('hqq_dev')

os.environ.setdefault('HQQ_ADMIN', 'remote')  # local or remote

try:
    HuaweiPush()
    XiaomiPush()
    OppoPush()
except Exception as e:
    logger.error('[推送错误{} (DRF.init)]'.format(e))
    print(e)
