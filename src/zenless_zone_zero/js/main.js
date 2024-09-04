dynamicRewardStatusColor();
showTimeAndDate();
timeAndDateInterval();
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
            case "unavailable":
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

function timeAndDateInterval() {
    var currentLocalDate = new Date();
    var currentUtcDate = new Date(currentLocalDate.getTime() + currentLocalDate.getTimezoneOffset() * 60000);
    var targetDate = new Date(document.getElementById('bc_target_date').dateTime);

    var timeDiff = Math.abs(targetDate - currentUtcDate);

    var seconds = Math.floor((timeDiff / 1000) % 60);
    var minutes = Math.floor((timeDiff / (1000 * 60)) % 60);
    var hours = Math.floor((timeDiff / (1000 * 60 * 60)) % 24);
    var days = Math.floor(timeDiff / (1000 * 60 * 60 * 24));

    hours = hours + (days * 24);

    var timeInterval = '';

    if (days > 0) {
        timeInterval += days + 'd ';
    }

    var remainingHours = Math.floor(timeDiff / (1000 * 60 * 60)) - (days * 24);
    if (remainingHours > 0) {
        timeInterval += remainingHours + 'h ';
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
    document.getElementById("bc_show_current_time_and_date").textContent = " | " + formattedTime + " (UTC+0)";
}

document.getElementById("bc_available_btn").onclick = function() {
    window.location.href = "index.html";
}

document.getElementById("bc_archives_btn").onclick = function() {
    window.location.href = "archives.html";
}

document.getElementById("hc_genshin_impact_btn").onclick = function() {
    window.location.href = "../genshin_impact/index.html";
}

document.getElementById("hc_zenless_zone_zero_btn").onclick = function() {
    window.location.href = "index.html";
}
