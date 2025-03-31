document.addEventListener("DOMContentLoaded", function () {
    // Get the dynamic toast element
    var toastElement = document.getElementById('dynamicToast');
    if (toastElement) {
        // Initialize and show the toast
        var toast = new bootstrap.Toast(toastElement);
        toast.show();
    }
});


function updateStatus(id, newStatus) {
    fetch('/update_status', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            type: "status_prof",
            professional_id: id,
            new_status: newStatus
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert(data.message);  // Optionally show a message to the user
        }
        // Reload the page after the update
        window.location.reload();  // This reloads the page
    })
    .catch(error => {
        console.error('Error:', error);
    });
}


function deleteService(id) {
    fetch('/update_status', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            type: "del_service",
            service_id: id,
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert(data.message);  // Optionally show a message to the user
        }
        if (data.error) {
            alert(data.error);  // Optionally show a message to the user
        }
        // Reload the page after the update
        window.location.reload();  // This reloads the page
    })
    .catch(error => {
        console.error('Error:', error);
    });
}


const alertPlaceholder = document.getElementById('liveAlertPlaceholder')
const appendAlert = (message, type) => {
  const wrapper = document.createElement('div')
  wrapper.innerHTML = [
    `<div class="alert alert-${type} alert-dismissible" role="alert">`,
    `   <div>${message}</div>`,
    '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
    '</div>'
  ].join('')

  alertPlaceholder.append(wrapper)
}

const alertTrigger = document.getElementById('liveAlertBtn')
if (alertTrigger) {
  alertTrigger.addEventListener('click', () => {
    appendAlert('Nice, you triggered this alert message!', 'success')
  })
}