document.addEventListener("DOMContentLoaded", () => {
  const infoAlert = document.getElementById("info-alert");
  const errorAlert = document.getElementById("error-alert");

  const currentUrl = new URL(window.location.href);
  const params = new URLSearchParams(currentUrl.search);

  const infoMessage = params.get("info");
  const errorMessage = params.get("error");

  if (infoMessage && infoAlert) {
    infoAlert.innerText = infoMessage;
    infoAlert.style.display = "block";
  }
  if (errorMessage && errorAlert) {
    errorAlert.innerText = errorMessage;
    errorAlert.style.display = "block";
  }
});
