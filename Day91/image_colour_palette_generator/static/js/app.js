const toast = document.querySelector("#toast");
const buttons = document.querySelectorAll(".hex-button");

function showToast(message) {
    if (!toast) {
        return;
    }

    toast.textContent = message;
    toast.classList.add("visible");

    setTimeout(() => {
        toast.classList.remove("visible");
    }, 1200);
}

buttons.forEach((button) => {
    button.addEventListener("click", async () => {
        const hexCode = button.dataset.hex;

        try {
            await navigator.clipboard.writeText(hexCode);
            showToast(`${hexCode} copied`);
        } catch (error) {
            showToast("Copy failed");
        }
    });
});
