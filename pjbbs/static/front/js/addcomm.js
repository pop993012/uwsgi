
$(function () {
     $('#addpost').click(function (ev) {
         ev.preventDefault();
         var content = ue.getContent();
         var csrf=$("#csrf_token").attr("value")
         var post_id=$('#aa').attr("value")
        $.ajax({
            url:'/addcomm/',
            type:'post',
            data:{
                "csrf_token":csrf,
                'content':content,
                'post_id':post_id
            },
            success:function (data) {
                if(data.code==200){
                xtalert.alertSuccess("评论成功");
                window.location.href = '/showpost/?post_id='+post_id
                }else {
                    xtalert.alertError(data.msg)
                    window.location.href='/'
                }
            }
        })
     })
})

