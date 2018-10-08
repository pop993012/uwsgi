
$(function () {
     $('#addpost').click(function (ev) {
         ev.preventDefault();
         var title = $('#a');
         var boarder_id = $('#b').val()
         alert(boarder_id)
         var content = ue.getContent();
         var csrf=$("#csrf_token").attr("value")
        $.ajax({
            url:'/tzfb/',
            type:'post',
            data:{
                'title':title.val(),
                'boarder_id':boarder_id,
                "csrf_token":csrf,
                'content':content
            },
            success:function (data) {
                if(data.code==200){
                xtalert.alertSuccess("发帖成功");
                window.location.href = '/'
                }else {
                    xtalert.alertError(data.msg)
                }
            }
        })
     })
})

