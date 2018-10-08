$(function () {
    $('#pop').click(function (ev) {
        ev.preventDefault()
        $('#saveBanner').attr("from",'0')
    })
    $('#saveBanner').click(function (ev) {
        self=$(this)
        ev.preventDefault()
        bkname=$('#BKName').val()
        csrf = $('meta[name=csrf_token]').attr("value");
        url='/cms/nv/'
        if (self.attr('from')==1){
            url='/cms/updatebk/'
        }
        $.ajax({
            url:url,
            type:'post',
            data:{
                'bkname':bkname,
                'csrf_token':csrf
            },
            success:function (data) {
                if (data.code==200){
                    xtalert.alertSuccess('添加成功')
                    window.location.reload()
                }else {
                    xtalert.alertError(data.msg)
                }
            }

        })
    })

        $('#delebtn').click(function (ev) {
        ev.preventDefault()
        self=$(this)
        id=self.attr('data-id')
          csrf = $('meta[name=csrf_token]').attr("value");
        $.ajax({
            url:'/cms/delbk/',
            type:'post',
            data:{
                'csrf_token': csrf,
                'id':id
            },
            success:function (data) {
                if(data.code==200){
                    xtalert.alertSuccess('删除成功')
                       window.location.reload()
                }else {
                    xtalert.alertError('删除失败')
                }
            }


        })
    })
 $('.update-btn').click(function () {
        self = $(this);
        $('#myModal').modal('show');// 让模态框出来
        $('meta[name=csrf_token]').attr("value");
        $('#saveBanner').attr("from",'1')
        $('#id').val(self.attr('data-id'))
    })

})