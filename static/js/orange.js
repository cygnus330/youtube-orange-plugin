function getinfo(v, res, status) {
    var video = document.getElementById('video__info');

    if(status == "-1") {
        video.innerHTML = `
        <div class='video__dur'>동영상 처리 시작</div>
`
    } else if(status == "0") {
        video.innerHTML = `
        <div class='video__dur'>동영상 다운로드 중</div>
`
    } else if(status == "1") {
        video.innerHTML = `
        <div class='video__dur'>동영상 다운로드 완료</div>
        <button class="video__res__info" onclick="getvideo(v, res)">다운로드</button>
`
    }
}

function getvideo(v, res) {
    window.location.href = `/getvideo/${v}/${res}`;
    setTimeout(function() {
        window.location.href = '/';
    }, 1000);
}