// static/content/js/upload_progress.js

console.log("Upload Progress Skript geladen!");

document.addEventListener("DOMContentLoaded", function () {
    // Django Admin Formular suchen (Formular mit enctype multipart)
    var form = document.querySelector('form[enctype="multipart/form-data"]') || document.querySelector('#video_form') || document.querySelector('form');

    if (!form) {
        console.warn("Upload Progress: Kein Formular gefunden.");
        return;
    }

    form.addEventListener("submit", function (e) {
        var fileInputs = form.querySelectorAll('input[type="file"]');
        var hasFile = Array.from(fileInputs).some(function (input) {
            return input.files && input.files.length > 0;
        });

        // Nur eingreifen, wenn auch mindestens eine Datei ausgewählt ist
        if (hasFile) {
            e.preventDefault(); // Verhindert normalen Seiten-Reload

            console.log("Upload gestartet, erstelle Ladebalken...");

            var formData = new FormData(form);
            var xhr = new XMLHttpRequest();

            // Progress-Container & Balken bauen
            var progressBar = document.getElementById("upload-progress-bar");
            if (!progressBar) {
                var progressContainer = document.createElement("div");
                progressContainer.style.cssText = "width: 100%; background: #e0e0e0; margin: 20px 0; border-radius: 4px; overflow: hidden; box-shadow: inset 0 1px 3px rgba(0,0,0,0.2);";

                progressBar = document.createElement("div");
                progressBar.id = "upload-progress-bar";
                progressBar.style.cssText = "width: 0%; height: 25px; background: #417690; transition: width 0.2s; text-align: center; color: white; line-height: 25px; font-weight: bold; font-family: sans-serif;";

                progressContainer.appendChild(progressBar);

                // Direkt über den Speicher-Buttons im Admin einfügen
                var submitRow = form.querySelector(".submit-row") || form;
                submitRow.parentNode.insertBefore(progressContainer, submitRow);
            }

            // Fortschritt aktualisieren
            xhr.upload.addEventListener("progress", function (event) {
                if (event.lengthComputable) {
                    var percent = Math.round((event.loaded / event.total) * 100);
                    progressBar.style.width = percent + "%";
                    progressBar.innerText = percent + "%";
                }
            });

            // Nach Abschluss
            xhr.addEventListener("load", function () {
                if (xhr.status >= 200 && xhr.status < 400) {
                    // Erfolgreich -> Zurück zur Video-Liste leiten
                    window.location.href = "../";
                } else {
                    alert("Upload-Fehler! Status: " + xhr.status);
                }
            });

            xhr.open("POST", form.action || window.location.href, true);
            xhr.send(formData);
        }
    });
});