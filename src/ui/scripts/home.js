/* home.js */

function updatePassword() {
    const password = document.getElementById("password").value;
    if (password.length > 0) {
        eel.set_key(password)();
    }
}

function updatePasscode() {
    const passcode = Array.from(document.getElementsByClassName("passcode")).map(input => input.value).join("");
    if (passcode.length === 6) {
        eel.set_key(passcode)();
    }
}

function updateKey(){
    if (inputType === "p") updatePassword();
    if (inputType === "c") updatePasscode();
}

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

    if (inputType === "d") {
        document.getElementById("DECRYPT").style.display = "none";
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

function selectFile() {
    eel.open_file_dialog('{"multiple": false}')((returnedPath) => {
        if (returnedPath) {
            console.log("File path from dialog: ", returnedPath);
        } else {
            console.log("No file was selected from the dialog.");
        }
    });
}

function allowDrop(event) {
    event.preventDefault();
}

function handleDrop(event) {
    event.preventDefault();
    let files = event.dataTransfer.files;
    if (files.length > 0) {
        processFile(files[0]);
    }
}

function handleFileSelect(event) {
    let files = event.target.files;
    if (files.length > 0) {
        processFile(files[0]);
    }
}

function processFile(file) {
    let reader = new FileReader();
    
    reader.onload = function(event) {
        let binaryString = String.fromCharCode.apply(null, new Uint8Array(event.target.result));
        let base64String = btoa(binaryString);
        alert(base64String)
        eel.set_key_base64(base64String)((result) => {
            if (result) {
                console.log("Key updated successfully");
                alert("File processed and key updated.");
            } else {
                console.log("Failed to update key");
                alert("Failed to update key.");
            }
        });
    };
    
    // Read the file as an ArrayBuffer
    reader.readAsArrayBuffer(file);
}