function countdown(elementName, minutes, seconds, criticalTimeMins)
{
    let element, endTime, hours, mins, msLeft, time;

    element = document.getElementById(elementName);
    endTime = (+new Date) + 1000 * (60*minutes + seconds) + 500;
    criticalTime = (new Date(1000*(60*(criticalTimeMins-1) + 59) + 500))
    updateTimer();

    function twoDigits(n) {
        return (n <= 9 ? "0" + n : n);
    }

    function updateTimer() {
        msLeft = endTime - (+new Date);
        if (msLeft < 1000) {
            window.location.replace("https://www.tutorialrepublic.com/%22");
        } else {
            time = new Date(msLeft);
            hours = time.getUTCHours();
            mins = time.getUTCMinutes();
            element.innerHTML = (hours ? hours + ':' + twoDigits(mins) : mins) + ':' + twoDigits(time.getUTCSeconds());
            setTimeout(updateTimer, time.getUTCMilliseconds() + 500);
        }

        if (msLeft < criticalTime) {
            element.style.color = '#b00505';
            element.style.borderColor = '#b00505';
        }
    }
}

countdown("ten-countdown", 10, 0, 1);

const url = window.location.href;
let chosenAnswer = null;
function chooseButton(button) {
    // Reset All Choice Buttons
    choiceButtons = document.getElementsByClassName('mc-buttons');
    for (i = 0; i < choiceButtons.length; i++) {
        choiceButtons[i].style.borderColor = '#000000';
        choiceButtons[i].style.color = '#000000';
    }

    button.style.borderColor = '#ffffff';
    button.style.color = '#ffffff';

    //Save Chosen Answer
    chosenAnswer = button.innerHTML;
}

let question = document.getElementById('txtQuestion').innerHTML;
let index = parseInt(document.getElementById('index').innerHTML);
const csrf = document.getElementsByName('csrfmiddlewaretoken');
console.log(question);
console.log(index);
function next() {
    const data = {};
    data['csrfmiddlewaretoken'] = csrf[0].value;
    data[question] = chosenAnswer;
    data['index'] = index;
    console.log(data)

    $.ajax({
        type: 'POST',
        url: `${url}`,
        data: data,
        success: function(response) {
            console.log(response);
        },
        error: function(error) {
            console.log(error);
        }
    })

    location.reload();
}