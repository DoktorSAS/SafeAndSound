# Safe&Sound Password Manager

In my quest to experiment with [Eel](https://github.com/python-eel/Eel), I embarked on creating a password manager. As a solo developer, I never anticipated encountering so many challenges due to the library being in such an early stage of development. 

Reflecting on my experience, I've found that Eel, while intriguing, isn't quite robust or feature-rich for comprehensive development tasks. Its limitations became apparent as I progressed.

During the development phase, I deliberately chose to work with plain HTML, CSS, and JavaScript (avoiding TypeScript) to challenge myself further. This decision made the project more demanding but also more rewarding in terms of learning and overcoming obstacles.

## 1° Challenge: Browser resources

Given that EEL (Electron Embedded Library) is still under development, optimizing it to reduce memory and CPU usage presents challenges. While relying on Chrome for execution might seem straightforward, it's actually quite problematic for this type of application due to Chrome's numerous default features that are often unnecessary for specialized software like mine.

To achieve the desired performance and functionality, I had to specify numerous flags when launching the browser. These flags were necessary to disable Chrome's default features, preventing conflicts with existing Chrome profiles and ensuring a streamlined experience tailored to our application's needs.

- `--user-data-dir=c:\\temp\\Safe&Sound`
- `--disable-gpu`
- `--disable-extensions`
- `--disable-plugins`
- `--disable-translate`
- `--disable-features=TranslateUI`
- `--disable-features=Translate`
- `--disable-features=TranslateLanguageDetection`
- `--disable-features=NetworkService`
- `--disable-features=CrossSiteDocumentBlockingIfIsolating`
- `--disable-features=CrossSiteDocumentBlockingAlways`
- `--disable-features=ImprovedCookieControls`
- `--disable-features=GlobalMediaControls`
- `--disable-features=IdleDetection`
- `--disable-password-manager`
- `--disable-autofill-keyboard-accessory`
- `--disable-autofill-fallback-to-insecure-mode`
- `--disable-save-password-bubble`
- `--disable-password-generation`
- `--disable-forms-re Strict-mode-for-autofill`
- `--disable-password-leak-detection`
- `--disable-sync`
- `--disable-password-manager-internal`
- `--disable-password-manager-reauthentication`
- `--disable-password-manager-warning`
- `--password-manager-internal-disabled`

## 2° Challenge: Loading files

The page is structured with a sidebar that remains constant and a main section that changes based on the selection made in the sidebar. Content for the main section is loaded only when requested. 

Specifically, at startup, only the sidebar is loaded. Once the `index.html` has loaded, I call the `load_page_content` function from the associated script to load the home page content. This approach means that initially, the files to be loaded are significantly reduced, as they do not include the content, stylesheet, or JavaScript for each page.

Common stylesheets are referenced in `index.html`, whereas page-specific styles for content loaded into the `main section` are included with the HTML code of each page. This means that `<style>` tags can be dynamically added or removed at any time, with an immediate impact on the application. However, this is not the case for `<script> `tags. For these, I had to develop JavaScript functions to manage script loading and unloading. I created `loadScript` and `unloadScript` functions to append or remove script elements by assigning and using a unique `ID` to identify them.

## 3° Challenge: Encryption and Decryption

There are various algorithms for encrypting and decrypting strings, but not all are suitable for every use case. For instance, SHA, being a one-way function, cannot be used for password encryption. However, it can be utilized to generate a unique hash from a string, which is useful for authentication purposes.

In this project, we aim to provide two encryption options: the first relates to the file that actually contains the data, and the second concerns the method used for decrypting passwords.

The algorithms chosen for encrypting and decrypting individual credentials must be bidirectional, meaning they should work in both directions, while the algorithm for encrypting the file can be one-way.