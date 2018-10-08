$(function () {
    $('#signin_btn').click(function (ev) {
        ev.preventDefault()
        telephone=$('#a1').val()
        password=$('#a2').val()
        password1=$('#a3').val()
        code=$('#a4').val()
        csrf = $('meta[name=csrf_token]').attr("value");
        $.ajax({
            url:/regist/,
            type:'post',
            data:{
                'telephone':telephone,
                'password':password,
                'password1':password1,
                'csrf_token':csrf,
                'code':code
            },
            success:function (data) {
                if (data.code==200){
                    window.location =/sigin/
                }else {
                    xtalert.alertError(data.msg)
                }
            }

        })
    })
     $("#getcode").click(function (ev) {
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
})