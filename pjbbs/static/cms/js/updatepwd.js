$(function () {
    $('#aBtn').click(function (ev) {
        oldpwd = $('#inputEmail').val();
        pwd = $('#inputPassword').val();
        pwd2 = $('#rember').val();
        csrf = $('meta[name=csrf_token]').attr("value")
        ev.preventDefault();
        $.ajax({
            url:'/cms/cc/',
            type:'post',
            data:{
                'oldpwd':oldpwd,
                'pwd':pwd,
                'csrf_token':csrf,
                'pwd2':pwd2
            },
            success:function (data) {
                if (data.code == 200) {
                    alert(11)
                    xtalert.alertSuccess('修改成功')
                } else {  // 提示出错误
                    alert(22)
                    xtalert.alertErrorToast(data.msg)
                }
            }
        })
    })
})