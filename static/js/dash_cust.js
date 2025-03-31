function completeRequest(req_id, cust_id) {
    fetch('/update_request', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            type: "complete_request",
            customer_id: cust_id,
            request_id: req_id
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

function cancelRequest(req_id, cust_id) {
    fetch('/update_request', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            type: "cancel_request",
            customer_id: cust_id,
            request_id: req_id
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

