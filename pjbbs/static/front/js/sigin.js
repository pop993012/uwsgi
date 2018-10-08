$(function () {
    $('#signin_btn').click(function (ev) {
        ev.preventDefault()
        telephone=$('#a1').val()
        password=$('#a2').val()
        csrf = $('meta[name=csrf_token]').attr("value");
        $.ajax({
            url:/sigin/,
            type:'post',
            data:{
                'telephone':telephone,
                'password':password,
                'csrf_token':csrf
            },
            success:function (data) {
                if (data.code==200){
                    window.location =$('#local').attr('value')
                }else {
                    xtalert.alertError(data.msg)
                }
            }

        })
    })
})