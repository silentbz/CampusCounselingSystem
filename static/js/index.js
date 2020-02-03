
var recorder;
var btn = document.getElementById('voice_btn');
// 用于判断下一步是开始录音还是结束录音
var btn_flag = 0;


function startRecording() {
    HZRecorder.get(function (rec) {
        recorder = rec;
        recorder.start();
        btn.setAttribute("value","结束录音");
        btn.style.background = "#ed4014";

        btn_flag = 1
    });
}
function stopRecording() {
    recorder.stop();
    btn.setAttribute("value","开始录音");
    btn.style.background = "#215798";

    btn_flag = 0;
    uploadAudio();
}
function uploadAudio() {
    layer.open({
        type: 3
    });
    recorder.upload("https://api.sillywa.com/api/recognition/", function (state, e) {
        switch (state) {
            case 'uploading':
                var percentComplete = Math.round(e.loaded * 100 / e.total) + '%';
                console.log(percentComplete)
                break;
            case 'ok':                   
                console.log(JSON.parse(e.target.responseText));
                layer.closeAll()
                if (e.target.status != 200) {
                    var result = JSON.parse(e.target.responseText).result;
                    layer.msg(result)
                } else {

                    var result = JSON.parse(e.target.responseText).result[0];

                    layer.msg("识别成功：" + result,{icon: 1})
                }
                break;
            case 'error':
                layer.msg("上传失败");
                break;
            case 'cancel':
                layer.msg("上传被取消");
                break;
        }
     });
}
// 添加点击事件
btn.onclick = function() {
    if(btn_flag == 1) {
        stopRecording()
    } else {
        startRecording()
    }
};


