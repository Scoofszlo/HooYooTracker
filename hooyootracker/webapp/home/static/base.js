setDateAndTimeNow();
showTimeAndDate();
timeAndDateInterval();
dynamicRewardStatusColor();
setInterval(timeAndDateInterval, 1000);


function dynamicRewardStatusColor() {
    var dynamicSpan = document.querySelectorAll(".bc_reward_code_status");

    dynamicSpan.forEach(function(span) {
        setColorBasedOnAvailability(span);
    });

    function setColorBasedOnAvailability(span) {
        var content = span.textContent.toLowerCase();

        switch (content) {
            case "available":
                span.style.backgroundColor = "rgb(43, 89, 63)";
                span.style.color = "white";
                span.style.padding = "5px 15px";
                span.style.borderRadius = "10px";
                break;
            case "expired":
                span.style.backgroundColor = "rgb(110, 54, 48)";
                span.style.color = "white";
                span.style.padding = "5px 15px";
                span.style.borderRadius = "10px";
                break;
            default:
                span.style.backgroundColor = "rgb(126, 126, 126)";
                span.style.color = "white";
                span.style.padding = "5px 15px";
                span.style.borderRadius = "10px";
        }
    }
}

function setDateAndTimeNow() {
    var targetDateElement = document.getElementById("bc_target_date");
    if (targetDateElement) {
        var currentDate = new Date();
        targetDateElement.dateTime = currentDate.toISOString();
    }
}

function timeAndDateInterval() {
    var currentLocalDate = new Date();
    var targetDate = new Date(document.getElementById('bc_target_date').dateTime);

    var timeDiff = Math.abs(targetDate - currentLocalDate);

    var seconds = Math.floor((timeDiff / 1000) % 60);
    var minutes = Math.floor((timeDiff / (1000 * 60)) % 60);
    var hours = Math.floor((timeDiff / (1000 * 60 * 60)) % 24);
    var days = Math.floor(timeDiff / (1000 * 60 * 60 * 24));

    var timeInterval = '';

    if (days > 0) {
        timeInterval += days + 'd ';
    }

    if (hours > 0) {
        timeInterval += hours + 'h ';
    }

    if (minutes > 0) {
        timeInterval += minutes + 'm ';
    }

    if (seconds > 0) {
        timeInterval += seconds + 's ';
    }

    document.getElementById('bc_time_interval').textContent = timeInterval.trim() + " ago";
}

function showTimeAndDate() {
    var targetDate = new Date(document.getElementById('bc_target_date').dateTime);
    var hours = targetDate.getHours();
    var minutes = targetDate.getMinutes();
    var day = targetDate.getDate();
    var month = targetDate.toLocaleString('default', {
        month: 'short'
    });
    var year = targetDate.getFullYear();

    // Add leading zeros if necessary
    hours = hours < 10 ? "0" + hours : hours;
    minutes = minutes < 10 ? "0" + minutes : minutes;

    var formattedTime = hours + ":" + minutes + ", " + month + " " + day + ", " + year;

    // Update the time display
    document.getElementById("bc_show_current_time_and_date").textContent = " | " + formattedTime + " (local time)";
}

document.getElementById("hc_genshin_impact_btn").onclick = function() {
    window.location.href = "/gi";
}

document.getElementById("hc_zenless_zone_zero_btn").onclick = function() {
    window.location.href = "/zzz";
}

