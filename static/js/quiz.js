
var chosenAnswer = null;


window.onbeforeunload = function() {
    console.log('reload page?');
    return "Do you really want to leave the page?"
};


// override
function stopTimer(timerIntervalId) {
    clearInterval(timerIntervalId);
    if (timeLeft == 0) {
        document.getElementById('finish-btn').click();
    }
    return timeLeft
}


function reset_mc_btn() {
    let choiceButtons = document.getElementsByClassName('mc-buttons');
    for (i = 0; i < choiceButtons.length; i++) {
        choiceButtons[i].style.borderColor = '#000000';
        choiceButtons[i].style.color = '#000000';
    }
    chosenAnswer = null;
}


document.querySelectorAll('.mc-buttons').forEach(item => {
    item.addEventListener('click', function() {
        reset_mc_btn();

        item.style.borderColor = '#ffffff';
        item.style.color = '#ffffff';

        //Save Chosen Answer
        chosenAnswer = item.getAttribute("data-choice");
    })
})


$(document).ready(function(){
    const url = window.location.href;
    const csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;

    let startTime = document.getElementById('timer').getAttribute("data-start-time"); 
    // startTimer in 'circular timer,js'
    let timerIntervalId = startTimer('timer', startTime, '200px')


    $('#next-btn').click(function() {   
        $.post(
            `${url}`,                            // url
            {                                    // data to be submit
                'csrfmiddlewaretoken': csrf_token,
                'isNextClicked': true,
                'chosenAnswer': chosenAnswer,
            },    
            function(question, status, xhr) {    // success callback function
                console.log('Next question succeeded.');

                // change the question's text and choices
                $('#txtQuestion').text('Q' + question['index'].toString() + ': ' + question['question_text']);
                $('#btnChoiceA').text(question['choiceA']);
                $('#btnChoiceB').text(question['choiceB']);
                $('#btnChoiceC').text(question['choiceC']);
                $('#btnChoiceD').text(question['choiceD']);
                
                $('#index-indicator').text(question['index']);
                
                // change the button to finish button at the last question
                if (question['isLast']) {
                    document.getElementById('finish-btn').style.display = "block";
                    document.getElementById('next-btn').style.display = "none";
                };
            },
            'json',    // response data format
        ).fail(function(jqxhr, settings, ex) { console.log('Next question failed, ' + ex); }); 

        reset_mc_btn();
    });



    $(document).on("click", "#finish-btn", function(e){
        let timeRemain = stopTimer(timerIntervalId)
        $.post(
            `${url}`,    // url
            {            // data to be submit
                'csrfmiddlewaretoken': csrf_token,
                'isFinishClicked': true,
                'chosenAnswer': chosenAnswer,
                'timeRemain': timeRemain
            },
            function(data) {
                console.log('Finish succeeded.');
                $("body").html(data);
                window.onbeforeunload = null;
            }, 
        ).fail(function(jqxhr, settings, ex) { console.log('Finish failed, ' + ex); });      
    });
});

