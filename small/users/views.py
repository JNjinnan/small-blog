from django.shortcuts import render

# Create your views here.

from django.views import View

class RegisterView(View):
    """用户注册"""

    def get(self, request):
        """
        提供注册界面
        :param request: 请求对象
        :return: 注册界面
        """
        return render(request, 'register.html')


from django.http.response import HttpResponseBadRequest
from libs.captcha.captcha import captcha
from django_redis import get_redis_connection
from django.http import HttpResponse

class ImageCodeView(View):

    def get(self, request):

        # 1.接收前端传递过来的uuid
        uuid=request.GET.get('uuid')
        # 2.判断uuid是否获取到
        if uuid is None:
            return HttpResponseBadRequest('没有传递uuid')
        # 3.通过调用captcha来生成图片验证码（图片二进制和图片内容）
        text,image=captcha.generate_captcha()
        # 4.将图片内容保存在redis中 uuid作为一个key,图片内容作为value，同时我们可以设置一个时效
        redis_conn=get_redis_connection('default')
        # key设置为uuid
        # seconds设置过期秒数，设为300秒，即5分钟过期时间
        # value 设置为text
        redis_conn.setex('img:%s'%uuid,300,text)
        # 5.返回图片二进制
        return HttpResponse(image,content_type='image/jpeg')



