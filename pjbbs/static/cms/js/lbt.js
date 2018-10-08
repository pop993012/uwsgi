$(function () {
    $('#pop').click(function (ev) {
        ev.preventDefault()
        $('#saveBanner').attr("from",'0')
    })
    $('#saveBanner').click(function (ev) {
        self=$(this)
        ev.preventDefault();
        bannerName = $('#bannerName').val();
        imglink = $('#imglink').val();
        link = $('#link').val();
        priority = $('#priority').val();
        csrf = $('meta[name=csrf_token]').attr("value");
        id=$('#aa').attr('value')
        url1='/cms/nb/'
        if (self.attr('from')==1){
            url='/cms/lb/'
        }
         $.ajax({
            url: url1,
            type: 'post',
            data: {
                'bannerName': bannerName,
                'csrf_token': csrf,
                'imglink': imglink,
                'link': link,
                'priority': priority,
                'id':id
            },
            success: function (data) {
                if (data.code == 200) {
                    xtalert.alertSuccess('添加成功')
                       window.location.reload()
                } else {
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
            url:'/cms/iop/',
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
        $("#bannerName").val(self.attr('data-bannerName'));
        $('#imglink').val(self.attr('data-imglink'));
        $('#link').val(self.attr('data-link'));
        $('#priority').val(self.attr("data-priority"));
        $('#saveBanner').attr("from",'1')
        $('#id').val(self.attr('data-id'))
    })

        // 上传图片到七牛云
uploader = Qiniu.uploader({
            runtimes: 'html5,html4,flash',
            browse_button: 'QNbtn',//上传按钮的ID,
            max_file_size: '4mb',//最大文件限制
            dragdrop: false, //是否开启拖拽上传
            uptoken_url: '/cms/qiniu_token/',//设置请求qiniu-token的url
            domain: 'pfpjd7i5o.bkt.clouddn.com',//自己的七牛云存储空间域名
            get_new_uptoken: false, //是否每次上传文件都要从业务服务器获取token
            auto_start: true, //如果设置了true,只要选择了图片,就会自动上传
            unique_names: true,
            multi_selection: false,//是否允许同时选择多文件
            //文件类型过滤，这里限制为图片类型
            filters: {
              mime_types : [
                {title : "Image files", extensions: "jpg,jpeg,png"}
              ]
            },
            init: {
                'FileUploaded': function(up, file, info) {
                   var res = eval('(' + info + ')');
                    res.key;//获取上传文件的链接地址
                   // $('#imglink').attr('value',sourceLink)
                    sourceLink = 'http://pfpjd7i5o.bkt.clouddn.com/' + res.key;
                    console.log(sourceLink)  // 访问图片的网址
                    // 放到我们的input标签中
                    $("#imglink").val(sourceLink);
                },
                'Error': function(up, err, errTip) {
                    console.log(err);
                    xtalert.alertErrorToast("上传失败")
                }
            }
        })



})