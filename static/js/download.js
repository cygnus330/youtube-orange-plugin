function getinfo(v) {
    fetch(`/getinfo/${encodeURIComponent(v)}`)
        .then(response => response.json())
        .then(data => download(data, v))
        .catch(error => console.log(error));
}

function sec_to_time(sec) {
    var s = parseInt(sec, 10);
    const h = Math.floor(s / 3600);
    s -= h * 3600;
    const m = Math.floor(s / 60);
    s -= m * 60;

    const h_dis = h > 0 ? `${h}시간 ` : "";
    const m_dis = m > 0 ? `${m}분 ` : "";
    const s_dis = s > 0 ? `${s}초` : "";

    return h_dis + m_dis + s_dis || "0초";
}

function download(data, v) {
    var table = data;
    var res = table.res;
    var dur = table.dur;
    var auto = table.auto;
    var video = document.getElementById('video__info');

    video.innerHTML=`<div class='video__info__wrap'>
    <div class='video__dur'>${sec_to_time(dur)}</div>
    <div class='video__res'>
        <a class='video__res__info' href="/orange/${v}/${auto}">자동 ${Math.round(auto)}p</a>
    ${res.map((elem)=>{
        return (
            `<a class='video__res__info' href="/vote/${dur}/${elem}?v=${v}">${elem}p</a>`
        )
    }).join("")}
    </div>
</div>`
}