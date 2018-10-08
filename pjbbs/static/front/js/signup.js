$(function () {
    $("#send_sms_code_btn").click(function (ev) {
        telephone = $('input[name=telephone]').val()
        csrf = $('meta[name=csrf_token]').attr("value");
        ev.preventDefault();
        $.ajax({
            url:'/code/',
            type:'post',
            data:{
                'telephone':telephone,
                'csrf_token':csrf
            },
            success:function (data) {
                if (data.code == 200) {
                    xtalert.alertSuccessToast("发送短信验证码成功")
                } else {  // 提示出错误
                    xtalert.alertErrorToast(data.msg)
                }
            }
        })
    })
    $('#code').click(function (ev) {
        self=$(this)
        ev.preventDefault()
        r=Math.random()
        url=self.attr('aa')+'?a='+r
        self.attr('src',url)
    })
    $('#signup_btn').click(function (ev) {
        ev.preventDefault()
        telephone = $('input[name=telephone]').val();
        csrf = $('meta[name=csrf_token]').attr("value");
        smscode = $('input[name=smscode]').val();
        username = $('input[name=username]').val();
        password = $('input[name=password]').val();
        password1 = $('input[name=password1]').val();
        captchacode = $('input[name=captchacode]').val();
        $.ajax({
            url:/sigup/,
            type:'post',
            data:{
                'telephone':telephone,
                'csrf_token':csrf,
                'smscode':smscode,
                'username':username,
                'passwprd':password,
                'password1':password1,
                'captchacode':captchacode
            },
            success:function (data) {
                if (data.code==200){
                    window.location = '/'

                }else {
                    xtalert.alertError(data.msg)
                }
            }


        })
    })



})


