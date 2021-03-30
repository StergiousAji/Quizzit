let x = 0
  
for (var i = 1; i<2 ; i++) {​​​​​ 
    {{ questions|index:i}}
}


function countdown( elementName, minutes, seconds )
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



function highlightButton() {
    if(document.getElementById('btnAnswer').clicked == true)
    {
        document.getElementsById('btnAnswer1').style.borderColor = '#a83232';
    }
}

countdown( "ten-countdown", 10, 0);