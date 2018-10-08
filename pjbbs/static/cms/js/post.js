$(function () {
    $('.btn').click(function (ev) {
        self=$(this)
        post_id=self.attr('data-id')
        r=self.attr('data-btn')
        alert(r)
        ev.preventDefault()
        csrf = $('meta[name=csrf_token]').attr("value");
        url=  '/cms/addqwe/'
        if ( r == 'aa'){
            url=  '/cms/deleteqwe/'
        }
        $.ajax({
            url:url,
            type:'post',
            data:{
                'post_id':post_id,
                'csrf_token':csrf
            },
            success:function (data) {
                if (data.code==200){
                    xtalert.alertSuccess('加精成功')
                    window.location.reload()
                }else {
                    xtalert.alertError(data.msg)
                }
            }

        })
    })


})