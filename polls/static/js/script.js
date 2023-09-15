
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
    alert("Your Vote has been received.")
}


document.addEventListener('DOMContentLoaded', function () {
    disableLinks();
});
