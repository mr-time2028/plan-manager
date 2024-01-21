console.clear();
"use strict";


// modal section
let openAddWorkingOnTaskModal
let openAddDoneTaskModal
let openAddUnfinishedTaskModal
let createTaskModal
let updateTaskModal
let overlay
let closeCreateTaskModalBtn
let closeUpdateTaskModalBtn
let createTaskForm
let updateTaskForm
let workingOnTasksSection
let doneTasksSection
let unfinishedTasksSection
let display

document.addEventListener("DOMContentLoaded", async() => {
    openAddWorkingOnTaskModal = document.getElementById("openAddWorkingOnTaskModal")
    openAddDoneTaskModal = document.getElementById("openAddDoneTaskModal")
    openAddUnfinishedTaskModal = document.getElementById("openAddUnfinishedTaskModal")

    workingOnTasksSection = document.getElementById("workingOnTasksSection")
    doneTasksSection = document.getElementById("doneTasksSection")
    unfinishedTasksSection = document.getElementById("unfinishedTasksSection")

    createTaskForm = document.getElementById("createTaskForm")
    updateTaskForm = document.getElementById("updateTaskForm")
    createTaskModal = document.getElementById('createTaskModal')
    updateTaskModal = document.getElementById('updateTaskModal')
    overlay = document.getElementById('overlay')
    closeCreateTaskModalBtn = document.getElementById('closeCreateTaskModalBtn')
    closeUpdateTaskModalBtn = document.getElementById('closeUpdateTaskModalBtn')

    openAddWorkingOnTaskModal.addEventListener("click", () => openModal(createTaskModal, 'create', createTaskForm, 'w'))
    openAddDoneTaskModal.addEventListener("click", () => openModal(createTaskModal, 'create', createTaskForm, 'd'))
    openAddUnfinishedTaskModal.addEventListener("click", () => openModal(createTaskModal, 'create', createTaskForm, 'u'))
    closeCreateTaskModalBtn.addEventListener("click", () => closeModal(createTaskModal))
    closeUpdateTaskModalBtn.addEventListener("click", () => closeModal(updateTaskModal))

    await fetchAndRenderAllTasks();

    // update task
    document.querySelectorAll(".taskLi").forEach(element => {
        element.addEventListener("click", (e) => {
            e.preventDefault()

            openModal(updateTaskModal, '', updateTaskForm, "")
            const taskID = e.target.closest(".taskLi").querySelectorAll("input[type='hidden']")[0].value;
            const taskDescription = e.target.closest(".taskLi").querySelectorAll("input[type='hidden']")[1].value;
            const taskTitle = e.target.closest(".taskLi").querySelector(".widget-heading").textContent.trim()

            updateTaskForm.elements["updateTaskTitle"].value = taskTitle
            updateTaskForm.elements["updateTaskDescription"].value = taskDescription
            updateTaskForm.elements["taskID"].value = taskID
        })
    })

    updateTaskForm.addEventListener("submit", function(e) {
        e.preventDefault()
        const taskID = e.target.querySelectorAll("input[type='hidden']")[1].value;
        console.log(taskID)

        const headers = new Headers();
        headers.append("Content-Type", "application/json");

        const formData = extractFormData(updateTaskForm)

        const payload = {
            title: formData.title,
            description: formData.description,
        }
    
        const body = {
            method: "PUT",
            body: JSON.stringify(payload),
            headers: headers,
        }

        fetch(`http:\/\/localhost:8000/api/tasks/${taskID}`, body)
        .then((response) => response.json())
        .then((data) => {
            if (data.error) {
                notify("error while update task", "error")
            } else {
                location.href = location.href
            }
        })
        .catch((error) => {
            console.log(error)
            notify("something went wrong, please try again later", "error")
        })
    })

    // change status to "done"
    document.querySelectorAll(".taskLi").forEach(element => {
        const updateStatusBtn = element.querySelector(".btn-outline-success");

        if (updateStatusBtn) {
            updateStatusBtn.addEventListener("click", (e) => {
                e.stopPropagation()
                const taskID = e.target.closest(".taskLi").querySelector("input[type='hidden']").value;
                
                const payload = {
                    status: 'd'
                }

                const headers = new Headers();
                headers.append("Content-Type", "application/json");
            
                const body = {
                    method: "PUT",
                    body: JSON.stringify(payload),
                    headers: headers,
                }
    
                fetch(`http:\/\/localhost:8000/api/tasks/${taskID}`, body)
                .then((response) => response.json())
                .then((data) => {
                    if (data.error) {
                        notify("error while update task", "error")
                    } else {
                        // delete timer from local storage
                        localStorage.removeItem(`${taskID}_timer`)    
                        location.href = location.href
                    }
                })
                .catch((error) => {
                    console.log(error)
                    notify("something went wrong, please try again later", "error")
                })
            })
        }
    })

    // delete task
    document.querySelectorAll(".taskLi").forEach(element => {
        const deleteBtn = element.querySelector(".btn-outline-danger");

        if (deleteBtn) {
            deleteBtn.addEventListener("click", (e) => {
                e.stopPropagation()
                const taskID = e.target.closest(".taskLi").querySelector("input[type='hidden']").value;
                deleteTaskWithAlert(taskID, "Are you sure you want to delete this task?", "warning");
            });
        }
    });

    // create task
    createTaskForm.addEventListener("submit", function(e) {
        e.preventDefault()
        const formData = extractFormData(createTaskForm)

        const taskTitleEl = document.getElementById("createTaskTitle")
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
                    if (data.data.status === 'w') {
                        // store timer in storage (because when refresh page, all timers reset)
                        let taskStartDate = new Date()
                        let daysDuration = taskStartDate.getDate() + Number(formData.taskDurationDays)
                        let hoursDuration = taskStartDate.getHours() + Number(formData.taskDurationHours)
                        let minutesDuration = taskStartDate.getMinutes() + Number(formData.taskDurationMinutes)

                        daysDuration = daysDuration === "" ? "0" + daysDuration : daysDuration;
                        daysDuration = daysDuration < 10 ? "0" + daysDuration : daysDuration;

                        hoursDuration = hoursDuration === "" ? "0" + hoursDuration : hoursDuration;
                        hoursDuration = hoursDuration < 10 ? "0" + hoursDuration : hoursDuration;

                        minutesDuration = minutesDuration === "" ? "0" + minutesDuration : minutesDuration;
                        minutesDuration = minutesDuration < 10 ? "0" + minutesDuration : minutesDuration;

                        currentMonth = taskStartDate.getMonth() + 1
                        currentMonth = currentMonth < 10 ? "0" + currentMonth : currentMonth

                        let timeString = `${taskStartDate.getFullYear()}-${currentMonth}-${daysDuration}T${hoursDuration}:${minutesDuration}:${taskStartDate.getSeconds()}`
                        let taskEndDate = new Date(timeString)
                        localStorage.setItem(`${data.data.id}_timer`, taskEndDate, undefined, 4)

                        // start timer
                        const taskTimeEl = document.getElementById(`${data.data.id}_timer`)
                        startTimer(formData.taskDurationDays, formData.taskDurationHours, formData.taskDurationMinutes, taskStartDate.getSeconds(), taskTimeEl)
                    }

                    // close createTask model
                    closeModal(createTaskModal)

                    successAndRefreshAlert("task was added successfully!")
                }
            })
            .catch((error) => {
                closeModal(createTaskModal)
                console.log(error)
                notify("something went wrong, please try again later", "error")
            })
    })
})

// fetch task in paralell way
async function fetchAndRenderTasks(status, targetSection) {
    let checkBtnTemplate = `
    <button class="border-0 btn-transition btn btn-outline-success">
        <i class="fa fa-check"></i>
    </button>
    `

    let timerTemplate = `
    <span class="btn btn-info" id="{TIME_ID_TIMER}"></span>
    `

    let taskTemplate = `
    <li class="taskLi list-group-item">
        <input type="hidden" value="{TASK_ID}"/>
        <input type="hidden" value="{TASK_DESCRIPTION}"/>

        <div class="widget-content p-0">
            <div class="widget-content-wrapper">
                <div class="widget-content-left">
                    <div class="widget-heading">
                    {TASK_TITLE}
                    </div>
                </div>
                <div class="widget-content-right">
                    ${status == 'w' ? timerTemplate: ''}
                    ${status == 'w' ? checkBtnTemplate : ''}
                    <button class="border-0 btn-transition btn btn-outline-danger">
                        <i class="fa fa-trash"></i>
                    </button>
                </div>
            </div>
        </div>
    </li>
    `

    try {
        let response

        if (status) {
            response = await fetch(`http:\/\/localhost:8000/api/tasks?status=${status}`);
        } else {
            response = await fetch(`http:\/\/localhost:8000/api/tasks`);
        }
        const tasks = await response.json();

        tasks.data.forEach((task) => {
            targetSection.insertAdjacentHTML("afterbegin",
                taskTemplate
                .replace('{TASK_TITLE}', task.title)
                .replace('{TIME_ID_TIMER}', `${task.id}_timer`)
                .replace('{TASK_ID}', task.id)
                .replace('{TASK_DESCRIPTION}', task.description)
            )

            const timerStorage = localStorage.getItem(`${task.id}_timer`)
            if (timerStorage) {
                let now = new Date()
                let taskEndDate = new Date(timerStorage)
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
        console.log(error);
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
            performActionAfterTimer(display);
        }
    }, 1000);
}

// change task status to "unfinished"
function performActionAfterTimer(display) {
    const taskID = display.closest(".taskLi").querySelector("input[type='hidden']").value;
    console.log(taskID)

    const payload = {
        status: 'u'
    }

    const headers = new Headers();
    headers.append("Content-Type", "application/json");

    const body = {
        method: "PUT",
        body: JSON.stringify(payload),
        headers: headers,
    }

    fetch(`http:\/\/localhost:8000/api/tasks/${taskID}`, body)
    .then((response) => response.json())
    .then((data) => {
        if (data.error) {
            notify("error while update task", "error")
        } else {
            // delete timer from local storage
            localStorage.removeItem(`${taskID}_timer`)    
            location.href = location.href
        }
    })
    .catch((error) => {
        console.log(error)
        notify("something went wrong, please try again later", "error")
    })
}

// utils
const extractFormData = function(formElement) {
    return [...formElement.querySelectorAll('input'), ...formElement.querySelectorAll('textarea')]
    .map(input => ({[input.name]: input.value}))
    .reduce((prev, curr) => ({...prev, ...curr}), {})
}

const openModal = function (modalEl, action, form, status) {
    if (action === 'create') {
        [...form.querySelectorAll('input'), ...form.querySelectorAll('textarea')].forEach(input => {
            input.value = ""
        })
    }

    modalEl.showModal()
    modalEl.classList.add('block')
    if (status) {
        form.querySelector("input[type=hidden]").value = status
    }
    form.querySelectorAll("small.text-danger").forEach((t) => {
        t.innerHTML = ""
    })
}

const closeModal = function (modalEl) {
    modalEl.classList.remove('block')
    modalEl.close()
}

function notify(msg, msgType) {
    notie.alert({
        type: msgType,
        text: msg,
    })
}

function successAndRefreshAlert(title) {
    Swal.fire({
        title: title,
        showDenyButton: false,
        showCancelButton: false,
        confirmButtonText: "OK",
        denyButtonText: `dsf`
      }).then((result) => {
        location.href = location.href;
      });
}


function deleteTaskWithAlert(taskID, title) {
    Swal.fire({
        title: title,
        text: "You won't be able to revert this!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#d33",
        cancelButtonColor: "#3085d6",
        confirmButtonText: "Yes, delete it!"
      }).then((result) => {
        if (result.isConfirmed) {
            const headers = new Headers();
            headers.append("Content-Type", "application/json");
        
            const body = {
                method: "DELETE",
                headers: headers,
            }

            fetch(`http:\/\/localhost:8000/api/tasks/${taskID}`, body)
            .then((response) => response.json())
            .then((data) => {
                if (data.error) {
                    notify("error while delete task", "error")
                } else {      
                    // delete timer from local storage
                    localStorage.removeItem(`${taskID}_timer`)
                    location.href = location.href
                }
            })
            .catch((error) => {
                console.log(error)
                notify("something went wrong, please try again later", "error")
            })
        }
    });
}
