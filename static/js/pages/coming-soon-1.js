// ===== COUNTDOWN =====
const targetDate = new Date("2026-12-31 00:00:00").getTime();

function updateCountdown(){
    const now = new Date().getTime();
    const gap = targetDate - now;

    const days = Math.floor(gap / (1000*60*60*24));
    const hours = Math.floor((gap % (1000*60*60*24)) / (1000*60*60));
    const minutes = Math.floor((gap % (1000*60*60)) / (1000*60));
    const seconds = Math.floor((gap % (1000*60)) / 1000);

    document.getElementById("days").innerText = days;
    document.getElementById("hours").innerText = hours;
    document.getElementById("minutes").innerText = minutes;
    document.getElementById("seconds").innerText = seconds;
}

setInterval(updateCountdown,1000);
