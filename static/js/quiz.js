function countdown(elementName, minutes, seconds)
{
    var element, endTime, hours, mins, msLeft, time;

    function twoDigits( n )
    {
        return (n <= 9 ? "0" + n : n);
    }

    function updateTimer()
    {
        msLeft = endTime - (+new Date);
        if ( msLeft < 1000 ) {
            window.location.replace("https://www.tutorialrepublic.com/%22");
        } else {
            time = new Date( msLeft );
            hours = time.getUTCHours();
            mins = time.getUTCMinutes();
            element.innerHTML = (hours ? hours + ':' + twoDigits( mins ) : mins) + ':' + twoDigits( time.getUTCSeconds() );
            setTimeout( updateTimer, time.getUTCMilliseconds() + 500 );
        }
    }

    element = document.getElementById( elementName );
    endTime = (+new Date) + 1000 * (60*minutes + seconds) + 500;
    updateTimer();
}

countdown("ten-countdown", 10, 0);

var chosenAnswer;
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

    document.getElementById('r').innerHTML = chosenAnswer;
}