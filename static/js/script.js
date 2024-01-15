console.clear();
"use strict";


// modal section
let openAddWorkingOnTaskModal
let openAddDoneTaskModal
let openAddUnfinishedTaskModal
let modal
let overlay
let closeModalBtn
let createTaskForm
let workingOnTasksSection
let doneTasksSection
let unfinishedTasksSection
let display

document.addEventListener("DOMContentLoaded", () => {
    openAddWorkingOnTaskModal = document.getElementById("openAddWorkingOnTaskModal")
    openAddDoneTaskModal = document.getElementById("openAddDoneTaskModal")
    openAddUnfinishedTaskModal = document.getElementById("openAddUnfinishedTaskModal")

    workingOnTasksSection = document.getElementById("workingOnTasksSection")
    doneTasksSection = document.getElementById("doneTasksSection")
    unfinishedTasksSection = document.getElementById("unfinishedTasksSection")

    createTaskForm = document.getElementById("createTaskForm")
    modal = document.getElementById('modal')
    overlay = document.getElementById('overlay')
    closeModalBtn = document.getElementById('closeModalBtn')

    openAddWorkingOnTaskModal.addEventListener("click", () => openModal('w'))
    openAddDoneTaskModal.addEventListener("click", () => openModal('d'))
    openAddUnfinishedTaskModal.addEventListener("click", () => openModal('u'))
    closeModalBtn.addEventListener("click", closeModal)

    fetchAndRenderAllTasks();

    createTaskForm.addEventListener("submit", function(e) {
        e.preventDefault()
        const formData = extractFormData(createTaskForm)

        const taskTitleEl = document.getElementById("taskTitle")
        const taskDaysEl = document.getElementById("taskDays")
        const taskHoursEl = document.getElementById("taskHours")
        const taskMinutesEl = document.getElementById("taskMinutes")

        if (!formData.title) {
            taskTitleEl.nextElementSibling.textContent = "title is required!"
            return
        } else {
            taskTitleEl.nextElementSibling.textContent = ""
        }

        if (!formData.taskDurationDays && !formData.taskDurationHours && !formData.taskDurationMinutes) {
            taskDaysEl.nextElementSibling.textContent = "one or more of this fields are required"
            taskHoursEl.nextElementSibling.textContent = "one or more of this fields are required"
            taskMinutesEl.nextElementSibling.textContent = "one or more of this fields are required"
            return
        } else {
            taskDaysEl.nextElementSibling.textContent = ""
            taskHoursEl.nextElementSibling.textContent = ""
            taskMinutesEl.nextElementSibling.textContent = ""
        }

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

        fetch("http:\/\/localhost:8000/api/tasks", body)
            .then((response) => response.json())
            .then((data) => {
                if (data.error) {
                    notify("error while add task", "error")
                } else {
                    // close createTask model
                    closeModal()

                    // refresh tasks after create one
                    workingOnTasksSection.innerHTML = ""
                    doneTasksSection.innerHTML = ""
                    unfinishedTasksSection.innerHTML = ""
                    fetchAndRenderAllTasks();

                    // store timer in storage (because when refresh page, all timers reset)
                    let taskStartDate = new Date()
                    let daysDuration = taskStartDate.getDate() + Number(formData.taskDurationDays)
                    let hoursDuration = taskStartDate.getHours() + Number(formData.taskDurationHours)
                    let minutesDuration = taskStartDate.getMinutes() + Number(formData.taskDurationMinutes)

                    daysDuration = daysDuration == "" ? "0" + daysDuration : daysDuration;
                    daysDuration = daysDuration < 10 ? "0" + daysDuration : daysDuration;

                    hoursDuration = hoursDuration == "" ? "0" + hoursDuration : hoursDuration;
                    hoursDuration = hoursDuration < 10 ? "0" + hoursDuration : hoursDuration;

                    minutesDuration = minutesDuration == "" ? "0" + minutesDuration : minutesDuration;
                    minutesDuration = minutesDuration < 10 ? "0" + minutesDuration : minutesDuration;

                    currentMonth = taskStartDate.getMonth() + 1
                    currentMonth = currentMonth < 10 ? "0" + currentMonth : currentMonth
 
                    let taskEndDate = new Date(`${taskStartDate.getFullYear()}-${currentMonth}-${daysDuration}T${hoursDuration}:${minutesDuration}:${taskStartDate.getSeconds()}`)

                    let timerData = {
                        "taskStartDate": taskStartDate,
                        "taskEndDate": taskEndDate,
                    }

                    localStorage.setItem(`${data.data.id}_timer`, JSON.stringify(timerData, undefined, 4))

                    // start timer
                    const taskTimeEl = document.getElementById(`${data.data.id}_timer`)
                    startTimer(formData.taskDurationDays, formData.taskDurationHours, formData.taskDurationMinutes, 0, taskTimeEl)

                    notify("task was added successfully", "success");
                }
            })
            .catch((error) => {
                closeModal()
                console.log(error)
                notify("something went wrong, please try again later", "error")
            })
    })
})

async function fetchAndRenderTasks(status, targetSection) {
    taskTemplate = `
    <li class="list-group-item">
        <div class="widget-content p-0">
            <div class="widget-content-wrapper">
            <div class="widget-content-left">
                <div class="widget-heading">
                {TITLE_PLACEHOLDER}
                </div>
            </div>
            <div class="widget-content-right">
                <span class="btn btn-info" id="{TIME_ID_PLACEHOLDER}"></span>
                <button class="border-0 btn-transition btn btn-outline-success">
                <i class="fa fa-check"></i>
                </button>
                <button class="border-0 btn-transition btn btn-outline-danger">
                <i class="fa fa-trash"></i>
                </button>
            </div>
            </div>
        </div>
    </li>
    `

    try {
        const response = await fetch(`http:\/\/localhost:8000/api/tasks?status=${status}`);
        const tasks = await response.json();

        tasks.data.forEach((task) => {
            targetSection.insertAdjacentHTML("afterbegin", taskTemplate.replace('{TITLE_PLACEHOLDER}', task.title).replace('{TIME_ID_PLACEHOLDER}', `${task.id}_timer`));

            const timerStorage = localStorage.getItem(`${task.id}_timer`)
            if (timerStorage) {
                timerData = JSON.parse(timerStorage)
                // console.log(timerData)

                let now = new Date()
                let taskStartDate = new Date(timerData.taskStartDate)
                let taskEndDate = new Date(timerData.taskEndDate)
                let timeRemaining = taskEndDate - now;

                let taskDaysRemained = Math.floor(timeRemaining / (1000 * 60 * 60 * 24));
                let taskHoursRemained = Math.floor((timeRemaining % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                let taskMinutesRemained = Math.floor((timeRemaining % (1000 * 60 * 60)) / (1000 * 60));
                let taskSecondsRemained = Math.floor((timeRemaining % (1000 * 60)) / 1000);
                

                timerSection = document.getElementById(`${task.id}_timer`)
                startTimer(taskDaysRemained, taskHoursRemained, taskMinutesRemained, taskSecondsRemained, timerSection)
            } else {
                console.log("cannot get nothing from storage")
            }
        });

    } catch (error) {
        console.error(error);
        notify(`Error while getting ${status} tasks`, "error");
    }
}

async function fetchAndRenderAllTasks() {
    await Promise.all([
        fetchAndRenderTasks('w', workingOnTasksSection),
        fetchAndRenderTasks('d', doneTasksSection),
        fetchAndRenderTasks('u', unfinishedTasksSection),
    ]);
}

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
    createTaskForm.querySelectorAll("small.text-danger").forEach((t) => {
        t.innerHTML = ""
    })
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
