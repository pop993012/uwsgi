$(function () {
    $('#bbtn').click(function (ev) {
        self=$(this)
        ev.preventDefault()
        email = $('#inputEmail').val();
        csrf = $('meta[name=csrf_token]').attr("value")
        $.ajax({
            url:'/cms/oo/',
            type:'post',
            data:{
                'email':email,
                'csrf_token':csrf
            },
            success:function (data) {
                if (data.code ==200){
                    xtalert.alertSuccess('发送成功')
                    self.attr('disabled', true);
                    var time = 5;
                    self.html(time + "s")
                    var timer = setInterval(function () {
                        self.html(--time + 's');
                        if (time <= 0) {
                            clearInterval(timer);
                            self.html("再次发送");
                            self.attr('disabled', false);
                        }
                    }, 1000);
                }
            }

        })
    })

    $('#aBtn').click(function (ev) {
        email = $('#inputEmail').val();
        emailcode = $('#rember').val();
        csrf = $('meta[name=csrf_token]').attr("value")
        ev.preventDefault();
        $.ajax({
            url:'/cms/ii/',
            type:'post',
            data:{
                'email':email,
                'emailcode':emailcode,
                'csrf_token':csrf,
            },
            success:function (data) {
                if (data.code == 200) {
                    alert(11)
                    window.location = '/cms/index/'
                } else {  // 提示出错误
                    alert(22)
                    xtalert.alertErrorToast(data.msg)
                }
            }
        })
    })
})