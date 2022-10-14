let timerShow = document.getElementById("timer");

const data = document.currentScript.dataset;
let end_time = Date.parse(data.end_time);

timer = setInterval(function () {
    let remaining_time = end_time-new Date();

    if (remaining_time <= 0) {
        clearInterval(timer);
        alert("Время закончилось!");
        window.location.reload();
    } else {
        let total_seconds = remaining_time/1000;
        let seconds = String(Math.trunc(total_seconds%60)).padStart(2, '0');
        let minutes = String(Math.trunc(total_seconds/60%60)).padStart(2, '0');
        let hours = Math.trunc(total_seconds/3600);
        timerShow.innerText = `${hours}:${minutes}:${seconds}`;
    }
}, 1000)