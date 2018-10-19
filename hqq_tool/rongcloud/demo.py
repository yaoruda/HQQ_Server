# -*- coding: utf-8 -*-
# __author__= "Ruda"
# Data: 2018/10/16

'''
import os
from rongcloud import RongCloud
app_key = os.environ['APP_KEY']
 app_secret = os.environ['APP_SECRET']
 rcloud = RongCloud(app_key, app_secret)

 r = rcloud.User.getToken(userId='userid1', name='username', portraitUri='http://www.rongcloud.cn/images/logo.png')
 print(r)
{'token': 'P9YNVZ2cMQwwaADiNDVrtRZKF+J2pVPOWSNlYMA1yA1g49pxjZs58n4FEufsH9XMCHTk6nHR6unQTuRgD8ZS/nlbkcv6ll4x', 'userId': 'userid1', 'code': 200}

 r = rcloud.Message.publishPrivate(
     fromUserId='userId1',
     toUserId={"userId2","userid3","userId4"},
     objectName='RC:VcMsg',
     content='{"content":"hello","extra":"helloExtra","duration":20}',
     pushContent='thisisapush',
     pushData='{"pushData":"hello"}',
     count='4',
     verifyBlacklist='0',
     isPersisted='0',
     isCounted='0')
 print(r)
{'code': 200}
'''
'''
More:

https://github.com/rongcloud/server-sdk-python

'''