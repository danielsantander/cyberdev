let currentPollIndex = 0; // Track the current poll index

function displayPoll(poll) {
    let polldom = {
        question: document.querySelector(".poll .question"),
        answers: document.querySelector(".poll .answers")
    };

    // Update the DOM with the current poll's question and answers
    polldom.question.innerText = poll.question;
    polldom.answers.innerHTML = poll.answers.map(function (answer, i) {
        return `
            <div class="answer" onclick="markanswer('${i}')">
                ${answer}
                <span class="percentage_bar"></span>
                <span class="percentage_value"></span>
            </div>
        `;
    }).join("");
}

function markanswer(i) {
    let poll = pollData[currentPollIndex]; // Get the current poll
    poll.selectanswer = +i;

    try {
        document.querySelector(".poll .answers .answer.selected")
            .classList.remove("selected");
    } catch (msg) {}

    document.querySelectorAll(".poll .answers .answer")[+i].classList.add("selected");

    showresults();
}

function showresults() {
    let poll = pollData[currentPollIndex]; // Get the current poll
    let answers = document.querySelectorAll(".poll .answers .answer");
    poll.selectedAnswer = -1;
    for (let i = 0; i < answers.length; i++) {
        let percentage = 0;

        if (i == poll.selectanswer) {
            // percentage = Math.round(
            //     (poll.answerweight[i] + 1) * 100 / (poll.pollcount + 1)
            // );
        } else {
            // percentage = Math.round(
            //     (poll.answerweight[i]) * 100 / (poll.pollcount + 1)
            // );
        }

        answers[i].querySelector(".percentage_bar").style.width = percentage + "%";
        answers[i].querySelector(".percentage_value").innerText = percentage + "%";
    }

    // Move to the next poll after a short delay
    setTimeout(() => {
        currentPollIndex++;
        if (currentPollIndex < pollData.length) {
            displayPoll(pollData[currentPollIndex]);
        } else {
            alert("All polls completed!");
            currentPollIndex = pollData.length - 1; // Prevent further out-of-bounds access
        }
    }, 2000); // 2-second delay before showing the next poll
}

// Initialize the first poll
displayPoll(pollData[currentPollIndex]);