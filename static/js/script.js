console.clear();
"use strict";


// modal section
let openAddWorkingOnTaskModal, openAddDoneTaskModal, openAddUnfinishedTaskModal, modal, overlay, closeModalBtn, createTaskForm

document.addEventListener("DOMContentLoaded", () => {
    openAddWorkingOnTaskModal = document.getElementById("openAddWorkingOnTaskModal")
    openAddDoneTaskModal = document.getElementById("openAddDoneTaskModal")
    openAddUnfinishedTaskModal = document.getElementById("openAddUnfinishedTaskModal")

    createTaskForm = document.getElementById("createTaskForm")
    modal = document.getElementById('modal')
    overlay = document.getElementById('overlay')
    closeModalBtn = document.getElementById('closeModalBtn')

    openAddWorkingOnTaskModal.addEventListener("click", () => openModal('w'))
    openAddDoneTaskModal.addEventListener("click", () => openModal('d'))
    openAddUnfinishedTaskModal.addEventListener("click", () => openModal('u'))
    closeModalBtn.addEventListener("click", closeModal)
    
    // TODO: load tasks
    async function fetchTasks() {
        e.preventDefault()

        const headers = new Headers();
        headers.append("Content-Type", "application/json");

        const body = {
            method: "GET",
            headers: headers,
        }

        // get workingOn tasks
        await fetch("http:\/\/localhost:8000/api/tasks/", body)
        .then((response) => response.json())
        .then((data) => {
            if (data.error) {
                notify("error while add task", "error")
            } else {
                closeModal()
                
                notify("task was added successfully", "success")
            }
        })
        .catch((error) => {
            closeModal()
            notify("something went wrong, please try again later", "error")
        })


    }

    createTaskForm.addEventListener("submit", function(e) {
        e.preventDefault()
        const formData = extractFormData(createTaskForm)

        const payload = {
            title: formData.title,
            description: formData.description,
            status: formData.status,
        }

        const headers = new Headers();
        headers.append("Content-Type", "application/json");

        const body = {
            method: "POST",
            body: JSON.stringify(payload),
            headers: headers,
        }

        fetch("http:\/\/localhost:8000/api/tasks/", body)
            .then((response) => response.json())
            .then((data) => {
                if (data.error) {
                    notify("error while add task", "error")
                } else {
                    closeModal()
                    notify("task was added successfully", "success")
                }
            })
            .catch((error) => {
                closeModal()
                notify("something went wrong, please try again later", "error")
            })

        
        /*

        [{
            id: <backend>
            startDate: now(),
            duration: form.duration
        },
        {

        }]

        */
    })
})

const extractFormData = function(formElement) {
    return [...formElement.querySelectorAll('input'), ...formElement.querySelectorAll('textarea')]
    .map(input => ({[input.name]: input.value}))
    .reduce((prev, curr) => ({...prev, ...curr}), {})
}

const openModal = function (status) {
    [...createTaskForm.querySelectorAll('input'), ...createTaskForm.querySelectorAll('textarea')].forEach(input => {
        input.value = ""
    })

    modal.showModal()
    modal.classList.add('block')
    createTaskForm.querySelector("input[type=hidden]").value = status
}

const closeModal = function () {
    modal.classList.remove('block')
    modal.close()
}

function notify(msg, msgType) {
    notie.alert({
        type: msgType,
        text: msg,
    })
}

function notifyModal(title, icon, html, footer) {
    Swal.fire({
        icon: icon,
        title: title,
        html: html,
        footer: footer
    })
}


// document.addEventListener('keydown', function(e) {
//     if (e.key == 'Escape' && !modal.classList.contains('hidden')) closeModal() 
// })


// timer
function startTimer(days=0, hours=0, minutes=0, seconds=0, display) {
    var timer = (days*24*60*60) + (hours*60*60) + (minutes*60) + seconds
    var intervalId = setInterval(function () {
        var daysFormatted = Math.floor(timer / (24 * 60 * 60));
        var hoursFormatted = Math.floor((timer % (24 * 60 * 60)) / (60 * 60));
        var minutesFormatted = Math.floor((timer % (60 * 60)) / 60);
        var secondsFormatted = Math.floor(timer % 60);

        daysDisplay = daysFormatted < 10 ? "0" + daysFormatted : daysFormatted;
        hoursDisplay = hoursFormatted < 10 ? "0" + hoursFormatted : hoursFormatted;
        minutesDisplay = minutesFormatted < 10 ? "0" + minutesFormatted : minutesFormatted;
        secondsDisplay = secondsFormatted < 10 ? "0" + secondsFormatted : secondsFormatted;

        display.textContent = daysDisplay + ":" + hoursDisplay + ":" + minutesDisplay + ":" + secondsDisplay;

        if (--timer < 0) {
            clearInterval(intervalId);
            display.textContent = "Timer Stopped";
            performActionAfterTimer();
        }
    }, 1000);
}

function performActionAfterTimer() {
    // Perform your desired action here
    console.log("Timer has stopped. Performing action...");
}

var display = document.getElementById('time');
startTimer(2, 5, 6, 0, display);
