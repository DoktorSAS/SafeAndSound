/* passwords.js */
function toggleDetails(element) {
    const details = element.nextElementSibling;
    details.style.display = details.style.display === 'none' ? 'block' : 'none';
}

function openCredentialsModal() {
    document.getElementById('credentialsModal').style.display = "block";
}

function closeCredentialsModal() {
    document.getElementById('credentialsModal').style.display = "none";
}

async function submitCredential() {
    var service = document.getElementById('service').value;
    var emailOrUsername = document.getElementById('email_or_username').value;
    
    try {
        if (typeof(element) != 'undefined' && element != null) {
            var value = document.getElementById('long_text').value;
            await eel.add_credential(1, service, emailOrUsername, value)();
            document.getElementById('long_text').value = '';
        }
        else {
            var value = document.getElementById('password').value;
            await eel.add_credential(0, service, emailOrUsername, value)();
            document.getElementById('password').value = '';
        }
        
        // Clear the form fields
        document.getElementById('service').value = '';
        document.getElementById('email_or_username').value = '';
        closeCredentialsModal();
    } catch (error) {
        console.error('Error adding credential:', error);

    }
}

// Placeholder function for editing a credential
function editCredential() {
    console.log("Edit credential functionality");
}

// Placeholder function for deleting a credential
function deleteCredential() {
    console.log("Delete credential functionality");
}