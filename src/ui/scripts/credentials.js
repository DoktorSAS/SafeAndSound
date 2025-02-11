/* passwords.js */
async function update_credentials_data(type) {
    try {
        document.getElementById('credentials').innerHTML = '';
        const data = await eel.get_credentials_data(type)();
        var credentials = data; 
        var itemTemplate = await fetch('./components/password.html').then(response => response.text());
        if (type == 1) {
            itemTemplate = await fetch('./components/plaintext.html').then(response => response.text());
        }

        for (let credential of credentials) {
            var parser = new DOMParser();
            var doc = parser.parseFromString(itemTemplate, 'text/html');
            var item = doc.body.firstElementChild; 

            item.querySelector('.item-number').textContent = (credentials.indexOf(credential) + 1).toString();
            item.querySelector('.item-title').textContent = credential.service;
            item.querySelector('.email').textContent = credential.email_or_username;

            var valueClass = ".password";
            if(type == 1) {
                valueClass = ".plaintext";
            }
            var valueElement = item.querySelector(valueClass);
            valueElement.textContent = credential.value;

            var emailCopyButton = item.querySelector('.email-container .copy-button');
            emailCopyButton.setAttribute('onclick', `copyToClipboard('${credential.email_or_username}')`);
            
            if(type == 0)  {
                var passwordCopyButton = item.querySelector('.password-container .copy-button');
                passwordCopyButton.setAttribute('onclick', `copyToClipboard('${credential.value}')`);
            }

            var itemHTML = item.outerHTML;
            const itemWithImages = await loadImagesFromDataAttributes(itemHTML);
            var tempDiv = document.createElement('div');
            tempDiv.innerHTML = itemWithImages;

            document.getElementById('credentials').appendChild(tempDiv.firstElementChild);
        }

        const translations = await loadLanguage(language);
        const updatedContent = updateContentWithTranslations(document.getElementById('credentials').innerHTML, translations);
        document.getElementById('credentials').innerHTML = updatedContent;
    } catch (error) {
        console.error('Error fetching or processing credentials data:', error);
    }
}

function openCredentialsModal() {
    document.getElementById('credentialsModal').style.display = "block";
}

function closeCredentialsModal() {
    document.getElementById('credentialsModal').style.display = "none";
}

async function submitCredential(type) {
    var service = document.getElementById('service').value;
    var emailOrUsername = document.getElementById('email_or_username').value;
    var encryption = document.getElementById('selectlist-option-algorithm').value;
    try {
        if (type == 1) {
            var value = document.getElementById('long_text').value;
            await eel.add_credential(1, encryption, service, emailOrUsername, value)();
            document.getElementById('long_text').value = '';
        }
        else {
            var value = document.getElementById('password').value;
            await eel.add_credential(0, encryption, service, emailOrUsername, value)();
            document.getElementById('password').value = '';
        }

        // Clear the form fields
        document.getElementById('service').value = '';
        document.getElementById('email_or_username').value = '';
        update_credentials_data(type);
        closeCredentialsModal();
    } catch (error) {
        console.error('Error adding credential:', error);

    }
}

function toggleDetails(element) {
    const details = element.nextElementSibling;
    details.style.display = details.style.display === 'none' ? 'block' : 'none';
}

function editCredential(event) {
    event.preventDefault();
    event.stopPropagation();
    console.log('Editing credential:', event.target);
    // Your edit functionality here
}

async function removeCredential(event, type) {
    event.preventDefault();
    event.stopPropagation();
    const listItem = event.target.closest('.list-item');
    
    if (listItem) {
        const itemNumberElement = listItem.querySelector('.item-number');
        if (itemNumberElement) {
            const itemNumber = parseInt(itemNumberElement.textContent, 10) - 1;
            try {
                await eel.remove_credential(type, itemNumber)();
                listItem.querySelector('.item-title').textContent = '';
                document.getElementById('credentials').innerHTML = '';
                
                await update_credentials_data(type);
                console.log(`Credential with ID ${itemNumber} removed.`);
                
            } catch (error) {
                console.error('Error removing credential:', error);
            }
        } else {
            console.error('Item number not found within the list item.');
        }
    } else {
        console.error('List item not found.');
    }
}