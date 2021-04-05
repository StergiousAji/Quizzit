// Credit: Mateusz Rybczonec
// Source: https://css-tricks.com/how-to-create-an-animated-countdown-timer-with-html-css-and-javascript/


var timeLeft = null;

function startTimer(elementID, timeLimit, size='200px') {

    let timePassed = 0;
    const COLOR_CODES = {
        info: {
            color: "green"
        },
        warning: {
            color: "orange",
            threshold: timeLimit/2
        },
        alert: {
            color: "red",
            threshold: timeLimit/4
        }
    };

    const FULL_DASH_ARRAY = addElement(elementID, COLOR_CODES.info.color, timeLimit);

    changeSize(size);

    timerIntervalId = setInterval(() => {
        timePassed = timePassed += 1;
        timeLeft = timeLimit - timePassed;
        
        document.getElementById("base-timer-label").innerHTML = formatTime(timeLeft);
        setCircleDasharray(timeLimit, timeLeft, FULL_DASH_ARRAY);
        setRemainingPathColor(COLOR_CODES, timeLeft);
        
        if (timeLeft == 0) {
            stopTimer(timerIntervalId);
        }
    }, 1000);

    return timerIntervalId
}

// console.log(startTimer('timer1', 10, '200px'));



function stopTimer(timerIntervalId) {
    clearInterval(timerIntervalId);
    return timeLeft
}


function addElement(elementID, remainingPathColor, timeLimit) {
    // Length = 2πr, 45 come from below '...cy="50" r="45"></circle>...'
    const FULL_DASH_ARRAY = Math.round(2*Math.PI*45);

    document.getElementById(elementID).innerHTML = `
<div class="base-timer">
  <svg class="base-timer__svg" viewBox="0 0 100 100">
    <g class="base-timer__circle"> 
      <circle class="base-timer__path-elapsed" cx="50" cy="50" r="45"></circle>
      <path
        id="base-timer-path-remaining"
        stroke-dasharray="${FULL_DASH_ARRAY}"
        class="base-timer__path-remaining ${remainingPathColor}"
        d="
          M 50, 50
          m -45, 0
          a 45,45 0 1,0 90,0
          a 45,45 0 1,0 -90,0
        "
      ></path>
    </g>
  </svg>
  <span id="base-timer-label" class="base-timer__label">${formatTime(timeLimit)}</span>
</div>
`;
  
    return FULL_DASH_ARRAY
}


function changeSize(size) {
    document.getElementsByClassName("base-timer")[0].style.height = size;
    document.getElementsByClassName("base-timer")[0].style.width = size;

    document.getElementsByClassName("base-timer__label")[0].style.height = size;
    document.getElementsByClassName("base-timer__label")[0].style.width = size;
    newSize = (parseInt(size)/3).toFixed(0) + 'px'
    document.getElementsByClassName("base-timer__label")[0].style.fontSize = newSize;
}


function formatTime(time) {
    const minutes = Math.floor(time / 60);
    let seconds = time % 60;

    if (seconds < 10) {
        seconds = `0${seconds}`;
    }

    return `${minutes}:${seconds}`;
}


function setCircleDasharray(timeLimit, timeLeft, FULL_DASH_ARRAY) {
    let timeFraction = timeLeft / timeLimit;
    timeFraction = timeFraction - (1 - timeFraction) / timeLimit;
    const circleDasharray = `${ (timeFraction * FULL_DASH_ARRAY).toFixed(0) } ${ FULL_DASH_ARRAY }`;
    
    document.getElementById("base-timer-path-remaining").setAttribute("stroke-dasharray", circleDasharray);
}
    
   
function setRemainingPathColor(COLOR_CODES, timeLeft) {
    const { alert, warning, info } = COLOR_CODES;

    if (timeLeft <= alert.threshold) {
        document.getElementById("base-timer-path-remaining").classList.remove(warning.color);
        document.getElementById("base-timer-path-remaining").classList.add(alert.color);
        document.getElementById("base-timer-label").style.color = alert.color;

    } else if (timeLeft <= warning.threshold) {
        document.getElementById("base-timer-path-remaining").classList.remove(info.color);
        document.getElementById("base-timer-path-remaining").classList.add(warning.color);
    }
}
