// passwords.js
function toggleDetails(element) {
    const details = element.nextElementSibling;
    details.style.display = details.style.display === 'none' ? 'block' : 'none';
}

// home.js
let inputType = "c"; // Change for different display modes

async function showInput() {
    const inputs = {
        "passwordInput": "none",
        "passcodeInput": "none",
        "dropzoneInput": "none"
    };

    if (inputType === "p" || inputType === "t") inputs["passwordInput"] = "block";
    if (inputType === "c" || inputType === "t") inputs["passcodeInput"] = "block";
    if (inputType === "d" || inputType === "t") inputs["dropzoneInput"] = "block";

    for (let [id, display] of Object.entries(inputs)) {
        document.getElementById(id).style.display = display;
    }
}

function togglePassword() {
    const password = document.getElementById("password");
    const passwordIcon = document.getElementById("passwordIcon");
    const isPasswordVisible = password.type === "text";

    password.type = isPasswordVisible ? "password" : "text";
    passwordIcon.innerHTML = isPasswordVisible ?
        '<path d="M29.946,15.675C27.954,9.888,22.35,6,16,6S4.046,9.888,2.054,15.675c-0.072,0.21-0.072,0.44,0,0.65 C4.046,22.112,9.65,26,16,26s11.954-3.888,13.946-9.675C30.018,16.115,30.018,15.885,29.946,15.675z M16,22c-3.309,0-6-2.691-6-6 s2.691-6,6-6s6,2.691,6,6S19.309,22,16,22z"/>' :
        '<path d="M20.722,24.964c0.096,0.096,0.057,0.264-0.073,0.306c-7.7,2.466-16.032-1.503-18.594-8.942 c-0.072-0.21-0.072-0.444,0-0.655c0.743-2.157,1.99-4.047,3.588-5.573c0.061-0.058,0.158-0.056,0.217,0.003l4.302,4.302 c0.03,0.03,0.041,0.072,0.031,0.113c-1.116,4.345,2.948,8.395,7.276,7.294c0.049-0.013,0.095-0.004,0.131,0.032 C17.958,22.201,20.045,24.287,20.722,24.964z"/><path d="M24.68,23.266c2.406-1.692,4.281-4.079,5.266-6.941c0.072-0.21,0.072-0.44,0-0.65 C27.954,9.888,22.35,6,16,6c-2.479,0-4.841,0.597-6.921,1.665L3.707,2.293c-0.391-0.391-1.023-0.391-1.414,0s-0.391,1.023,0,1.414 l26,26c0.391,0.391,1.023,0.391,1.414,0c0.391-0.391,0.391-1.023,0-1.414L24.68,23.266z"/>';
}

function moveToNext(field) {
    if (field.value.length >= 1) {
        const next = field.nextElementSibling;
        if (next && next.tagName === "INPUT") {
            next.focus();
        }
    }
}

function allowDrop(event) {
    event.preventDefault();
}

function handleDrop(event) {
    event.preventDefault();
    let files = event.dataTransfer.files;
    if (files.length > 0) alert("File dropped: " + files[0].name);
}

function handleFileSelect(event) {
    let files = event.target.files;
    if (files.length > 0) alert("File selected: " + files[0].name);
}

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
    load_page_content(current_page)
}

// scripts.js
let current_page = "home.html"
async function load_page_content(page) {
    let language = "en"
    try {
        eel.configuration_get("language")(function (value) {
            if (value) {
                language = value
            }
            else { language = "en" }
        })
        current_page = page;
        eel.get_page_content(page)(async function (content_html) {

            const translations = await loadLanguage(language);
            // Update the content with the translated HTML
            const updatedContent = updateContentWithTranslations(content_html, translations);
            const content = document.getElementById("content");
            content.innerHTML = updatedContent;
            await loadImagesFromDataAttributes()
            /*while(!imagesLoaded){}*/
            switch (page) {
                case "settings.html":
                    eel.configuration_get('pubkey_fpath')(function (value) {
                        if (value) {
                            const pubkey_fpath = document.getElementById("manualInput-pubkey_fpath");
                            pubkey_fpath.value = value
                        }
                    });

                    eel.configuration_get('privkey_fpath')(function (value) {
                        if (value) {
                            const pubkey_fpath = document.getElementById("manualInput-privkey_fpath");
                            pubkey_fpath.value = value
                        }
                    });

                    /* Handle files inputs*/
                    const fileButtons = document.querySelectorAll('.clickFileButton');

                    fileButtons.forEach(button => {
                        button.addEventListener('click', function () {
                            const id = this.getAttribute('data-id');
                            const title = this.getAttribute('data-dialog-title') || "Select a file";
                            const multiple = this.getAttribute('data-dialog-multiple') === 'false';

                            // Call the Python function through Eel
                            eel.open_file_dialog_eel(JSON.stringify({
                                multiple: multiple,
                                title: title
                            }))(function (paths) {
                                const fileInput = document.getElementById(`manualInput-${id}`);

                                if (Array.isArray(paths)) {
                                    fileInput.value = paths.join(', ');
                                } else if (paths) {
                                    fileInput.value = paths;  // for single file selection
                                }

                                eel.configuration_set(id, fileInput.value)(function (success) {
                                    if (success) {
                                        console.log(`Operation successfull for ${id}`);
                                    }
                                });
                            });
                        });
                    });

                    eel.configuration_get('algorithm')(function (value) {
                        if (value) {
                            setActiveOption('selectlist-option-algorithm', value);
                            updateEncryptAlgorithm();
                        }
                    });

                    eel.configuration_get('auth_method')(function (value) {
                        if (value) {
                            setActiveOption('selectlist-option-authkey', value);
                            updateAuthMethod();
                        }
                    });

                    eel.configuration_get('language')(function (value) {
                        if (value) {
                            setActiveOption('selectlist-option-language', value);
                        }
                    });

                    break;
                case "home.html":
                    eel.configuration_get('auth_method')(function (value) {
                        inputType = value;
                        showInput();
                    });
                    break;
            }
        })
    } catch (error) {
        console.error('Failed to load content:', error);
    }
}

/* locaization */

function updateContentWithTranslations(content_html, translations) {
    // Create a temporary DOM element to parse the content_html
    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = content_html;
    // Update text based on translations
    const elements = tempDiv.querySelectorAll('[data-lang-id]');
    elements.forEach(element => {
        const langId = element.getAttribute('data-lang-id');
        if (translations[langId]) {
            element.textContent = translations[langId];
        }
    });
    // Return the updated HTML
    return tempDiv.innerHTML;
}


function loadLanguage(lang) {
    return fetch(`lang/${lang}.ini`)
        .then(response => response.text())
        .then(data => {
            return parseINI(data); // Return translations as an object
        })
        .catch(error => console.error('Error loading language file:', error));
}


function parseINI(data) {
    const lines = data.split('\n');
    const result = {};
    for (let line of lines) {
        line = line.trim();
        if (line.includes('=')) {
            const [key, value] = line.split('=').map(part => part.trim());
            result[key] = value.replace(/"/g, ''); // Remove quotes
        }
    }
    return result;
}

/* images/svg/icon loader */
let imagesLoaded = false
async function loadImagesFromDataAttributes() {
    imagesLoaded = false
    // Select all elements with the data-image-path attribute
    const elements = document.querySelectorAll('*[data-image-path]');

    for (const element of elements) {
        const imagePath = element.getAttribute('data-image-path');
        const imageWidth = element.getAttribute('data-image-width');
        const imageHeight = element.getAttribute('data-image-height');

        // Check if the image path has a value
        if (imagePath) {
            // Check if the image is an SVG
            if (imagePath.endsWith('.svg')) {
                try {
                    const response = await fetch(imagePath);
                    const svgContent = await response.text();
                    // Set the innerHTML of the element to the SVG content
                    element.innerHTML = svgContent;

                    // Optionally, set the width and height if they are provided
                    if (imageWidth) {
                        element.querySelector('svg').setAttribute('width', imageWidth);
                    }
                    if (imageHeight) {
                        element.querySelector('svg').setAttribute('height', imageHeight);
                    }
                } catch (error) {
                    console.error(`Error loading SVG image: ${error}`);
                }
            } else {
                // Create an img element for non-SVG images
                const img = document.createElement('img');
                img.src = imagePath;

                // Set the width and height if they are provided
                if (imageWidth) {
                    img.width = parseInt(imageWidth, 10); // Set width
                }
                if (imageHeight) {
                    img.height = parseInt(imageHeight, 10); // Set height
                }

                // Append the img element to the element
                element.appendChild(img);
            }
        }
    }
    imagesLoaded = true
}

document.addEventListener('DOMContentLoaded', function () {
    load_page_content("home.html")
});

document.addEventListener("wheel", function touchHandler(e) {
    if (e.ctrlKey) {
        e.preventDefault();
    }
}, { passive: false });