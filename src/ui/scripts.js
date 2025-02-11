function loadScript(src, id, onload) {
    return new Promise((resolve, reject) => {
        const script = document.createElement('script');
        script.src = src;
        script.async = true; // Load asynchronously
        script.id = id; // Useful for later reference or removal
        
        // Handle when the script is loaded
        script.onload = function() {
            console.log(`Script loaded: ${src}`);
            if (onload) onload();
            resolve(script);
        };
        
        // Handle errors
        script.onerror = function() {
            console.error(`Error loading script: ${src}`);
            reject(new Error(`Failed to load script: ${src}`));
        };
        
        // Append the script to the document
        document.body.appendChild(script);
    });
}

function unloadScript(scriptId) {
    const scriptElement = document.getElementById(scriptId);
    if (scriptElement) {
        scriptElement.remove();
        console.log(`Script with id '${scriptId}' has been removed from the DOM.`);
    } else {
        console.log(`Script with id '${scriptId}' was not found in the DOM.`);
    }
}

// scripts.js
var currentPage = "home.html"
var scriptLoaded = "null"
var language = "en"
async function load_page_content(page) {
    if (scriptLoaded != "null")
        unloadScript(scriptLoaded);
    
    try {
        eel.configuration_get("language")(function (value) {
            if (value) {
                language = value
            }
            else { language = "en" }
        })
        currentPage = page;
        eel.get_page_content(page)(async function (content_html) {
            scriptLoaded = page
            if (page == "passwords.html" || page == "plaintexts.html") {
                await loadScript('./scripts/credentials.js', scriptLoaded)
            }
            if (page == "home.html") {
                await loadScript('./scripts/home.js', scriptLoaded)
            }
            if (page == "settings.html") {
                await loadScript('./scripts/settings.js', scriptLoaded)
            }
            await updateSidebarLanguage(language);
            const translations = await loadLanguage(language);
            const updatedContent = updateContentWithTranslations(content_html, translations);
            const contentWithImages = await loadImagesFromDataAttributes(updatedContent);
            const content = document.getElementById("content");
            content.innerHTML = contentWithImages;

            
            switch (page) {
                case "settings.html":
                    async function populateLanguageOptions() {
                        try {
                            // Fetch the JSON file
                            const response = await fetch('./lang/languages.json');
                            const languages = await response.json();
                            
                            // Get the select element
                            const selectElement = document.getElementById('selectlist-option-language');
                            
                            // Clear existing options
                            selectElement.innerHTML = '';
                            
                            // Populate the select with options from JSON
                            languages.forEach(lang => {
                                const option = document.createElement('option');
                                option.value = lang.id;
                                option.textContent = lang.label;
                                selectElement.appendChild(option);
                            });
                            
                            // Add the onchange event listener if not already present
                            selectElement.onchange = updateLanguage;
                            
                            console.log('Language options populated successfully');
                        } catch (error) {
                            console.error('Failed to populate language options:', error);
                        }
                    }

                    await populateLanguageOptions();

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

                    eel.configuration_get('language')(async function (value) {
                        if (value) {
                            setActiveOption('selectlist-option-language', value);
                            await updateSidebarLanguage(language);
                        }
                    });
                    break;
                case "home.html":
                    eel.configuration_get('auth_method')(function (value) {
                        inputType = value;
                        showInput();
                    });
                    break;
                case "passwords.html":
                    update_credentials_data(0);
                    break
                case "plaintexts.html":
                    update_credentials_data(1);
                    break;
            }
        })
    } catch (error) {
        console.error('Failed to load content:', error);
    }
}

/* locaization */
async function updateSidebarLanguage(lang) {

    function adjustFontSizeToFit(element, maxWidth = '8.5rem', maxFontSize = '1.25rem') {
        // Convert maxWidth and maxFontSize to pixels
        const maxWidthInPx = convertRemToPixels(maxWidth);
        const maxFontSizeInPx = convertRemToPixels(maxFontSize);

        // Function to convert rem to pixels
        function convertRemToPixels(rem) {
            return rem.replace('rem', '') * parseFloat(getComputedStyle(document.documentElement).fontSize);
        }

        // Initial font size
        let currentFontSize = maxFontSizeInPx;

        // Check the width of the text
        function checkTextWidth() {
            element.style.fontSize = currentFontSize + 'px';
            const textWidth = element.scrollWidth;

            // If the text width is greater than the max width, reduce font size
            if (textWidth > maxWidthInPx) {
                currentFontSize -= 1; // Decrease by 1px
                if (currentFontSize > 0) {
                    checkTextWidth(); // Recursively check again with reduced font size
                } else {
                    console.warn('Font size cannot be reduced further to fit the text');
                }
            }
        }

        // Start the process
        checkTextWidth();
    }
    try {
        const translations = await loadLanguage(lang);
        const sidebar = document.getElementById('sidebar');
        if (sidebar) {
            const elementsToTranslate = sidebar.querySelectorAll('[data-lang-id]');
            elementsToTranslate.forEach(element => {
                const langId = element.getAttribute('data-lang-id');
                if (translations[langId]) {
                    element.textContent = translations[langId];
                    adjustFontSizeToFit(element);
                }
            });
            console.log('Sidebar language updated to:', lang);
        } else {
            console.error('Sidebar element not found');
        }
    } catch (error) {
        console.error('Failed to update sidebar language:', error);
    }
}

function updateContentWithTranslations(content_html, translations) {
    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = content_html;
    
    // Query for elements with data-lang-id for content text translation
    const textElements = tempDiv.querySelectorAll('[data-lang-id]');
    textElements.forEach(element => {
        const langId = element.getAttribute('data-lang-id');
        if (translations[langId]) {
            element.textContent = translations[langId];
        }
    });
    
    // Query for elements with data-lang-placeholder-id for placeholder translation
    const placeholderElements = tempDiv.querySelectorAll('[data-lang-placeholder-id]');
    placeholderElements.forEach(element => {
        const placeholderLangId = element.getAttribute('data-lang-placeholder-id');
        if (translations[placeholderLangId]) {
            element.placeholder = translations[placeholderLangId] + "...";
        }
    });
    
    return tempDiv.innerHTML;
}

function loadLanguage(lang) {
    return fetch(`lang/${lang}.ini`)
        .then(response => response.text())
        .then(data => {
            return parseINI(data);
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
async function loadImagesFromDataAttributes(content) {
    imagesLoaded = false;
    // Create a temporary container to parse and load images
    const tempContainer = document.createElement('div');
    tempContainer.innerHTML = content;

    const elements = tempContainer.querySelectorAll('*[data-image-path]');

    const loadPromises = Array.from(elements).map(async element => {
        const imagePath = element.getAttribute('data-image-path');
        const imageWidth = element.getAttribute('data-image-width');
        const imageHeight = element.getAttribute('data-image-height');

        if (imagePath) {
            if (imagePath.endsWith('.svg')) {
                try {
                    const response = await fetch(imagePath);
                    const svgContent = await response.text();
                    const parser = new DOMParser();
                    const svgDoc = parser.parseFromString(svgContent, "image/svg+xml");
                    const svgElement = svgDoc.documentElement;

                    if (imageWidth) {
                        svgElement.setAttribute('width', imageWidth);
                    }
                    if (imageHeight) {
                        svgElement.setAttribute('height', imageHeight);
                    }
                    element.innerHTML = svgElement.outerHTML;
                } catch (error) {
                    console.error(`Error loading SVG image: ${error}`);
                }
            } else {
                await new Promise((resolve) => {
                    const img = new Image();
                    img.onload = () => {
                        if (imageWidth) {
                            img.width = parseInt(imageWidth, 10);
                        }
                        if (imageHeight) {
                            img.height = parseInt(imageHeight, 10);
                        }
                        element.appendChild(img);
                        resolve();
                    };
                    img.onerror = () => {
                        console.error(`Error loading image: ${imagePath}`);
                        resolve();
                    };
                    img.src = imagePath;
                });
            }
        }
    });

    await Promise.all(loadPromises);
    imagesLoaded = true;

    // Return the content with images loaded
    return tempContainer.innerHTML;
}

document.addEventListener('DOMContentLoaded', function () {
    //const translations = await loadLanguage(language);
    //updateContentWithTranslations(document.body.innerHTML, translations);
    load_page_content("home.html")
});

document.addEventListener("wheel", function touchHandler(e) {
    if (e.ctrlKey) {
        e.preventDefault();
    }
}, { passive: false });