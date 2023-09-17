
// use for warn user when polls is closed in index.
const disableLinks= () => {

    const disabledLinks = document.querySelectorAll('.disabled');
    disabledLinks.forEach(link => {
        if (link.getAttribute('data-disabled') === 'true') {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                alert("Voting for this poll is closed.");
            });
        }
    });
    
}
const voteAlert = () =>{
    var form = document.getElementById('voteForm');
    var selectedChoice = form.querySelector('input[name="choice"]:checked');

    // if user didnt select any choice.
    if (!selectedChoice) {
        alert("Please select a choice before voting. 😅");
        event.preventDefault(); // Prevent form submission
    }
    else if (!is_login){
        alert("Please login.")
    }
    else{
        alert("Your vote has been submitted. Thank you! 🥰");
    }
}

const noQuestionAlert = () =>{
    alert("There're no polls right now. 🥹")
}

document.addEventListener('DOMContentLoaded', function () {
    disableLinks();
});
