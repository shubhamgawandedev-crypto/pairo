const BASE_URL = "/api";

function showToast(message, type = "info") {
    const toastEl = document.getElementById("toast");
    const toastBody = document.getElementById("toast-body");

    // Customize appearance based on type
    if (type === "success") {
        toastEl.classList.remove("bg-dark");
        toastEl.classList.add("bg-success");
    } else if (type === "error") {
        toastEl.classList.remove("bg-dark");
        toastEl.classList.add("bg-danger");
    } else {
        toastEl.classList.remove("bg-success", "bg-danger");
        toastEl.classList.add("bg-dark");
    }

    toastBody.innerText = message;

    const toast = new bootstrap.Toast(toastEl, {
        autohide: true,
        delay: 3500 // longer visibility for better UX
    });
    toast.show();
}