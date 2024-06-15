const fileInput = document.getElementById('file-upload');
const form = document.getElementById('form');
const errorMessage = document.getElementById('error-message');
const serverResponse = document.getElementById('server-response');
const spinner = document.getElementById('spinner');
const uploadIcon = document.getElementById('upload-icon');
const uploadLabel = document.querySelector('label[for="file-upload"] p');

fileInput.addEventListener('change', function () {
    if (this.files && this.files.length > 0) {
        uploadLabel.textContent = this.files[0].name;
        uploadIcon.outerHTML = `
    <svg id="upload-icon" class="w-8 h-8 mb-4 text-gray-500 dark:text-gray-400"
        aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24"
        viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"
        strokeLinecap="round" strokeLinejoin="round">
        <path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z" />
        <path d="M14 2v4a2 2 0 0 0 2 2h4" />
    </svg>`;
        errorMessage.classList.add('hidden');
    }
});

document.body.addEventListener('htmx:beforeRequest', function (event) {
    if (!fileInput.files || fileInput.files.length === 0) {
        event.preventDefault();
        errorMessage.textContent = 'Please select a file before uploading.';
        errorMessage.classList.remove('hidden');
    } else {
        spinner.classList.remove('hidden');
        serverResponse.classList.add('hidden');
        errorMessage.classList.add('hidden');
    }
});

document.body.addEventListener('htmx:afterSwap', function (event) {
    spinner.classList.add('hidden');
    if (errorMessage) {
        serverResponse.classList.remove('hidden');
    } else {
        serverResponse.classList.add('hidden');
    }

    const response = JSON.parse(event.detail.xhr.response);
    if (response.status === 'success') {
        serverResponse.textContent = 'File uploaded successfully!';
        serverResponse.classList.remove('text-red-500');
        serverResponse.classList.remove('hidden');
        setTimeout(function () {
            window.location.href = '/';
        }, 2000); // wait for 2 seconds before redirecting
    }
});