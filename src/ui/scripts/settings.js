// settings.js
function setActiveOption(selectId, valueToSelect) {
    var select = document.getElementById(selectId);
    for (var i = 0; i < select.options.length; i++) {
        if (select.options[i].value === valueToSelect) {
            select.selectedIndex = i;
            break;
        }
    }
}

function updateEncryptAlgorithm() {
    const selectElement = document.getElementById('selectlist-option-algorithm');
    const keysLocations = document.getElementById('keys-locations');

    if (selectElement.value === 'RSA') {
        keysLocations.style.display = 'block';
    } else {
        keysLocations.style.display = 'none';
    }

    eel.configuration_set('algorithm', selectElement.value)(function (success) { });
}

function updateAuthMethod() {
    const selectElement = document.getElementById('selectlist-option-authkey');
    eel.configuration_set('auth_method', selectElement.value)(function (success) { });
}

function updateLanguage() {
    const selectElement = document.getElementById('selectlist-option-language');
    eel.configuration_set('language', selectElement.value)(function (success) { });
    load_page_content(currentPage)
}
