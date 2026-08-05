document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('#video_form') || document.querySelector('form');
    const fileInput = document.querySelector('input[type="file"]');

    if (!form || !fileInput) return;

    // Erstelle das Ladebalken-HTML dynamisch
    const progressContainer = document.createElement('div');
    progressContainer.style.cssText = 'display:none; margin: 15px 0; padding: 10px; background: #f8f9fa; border: 1px solid #ccc; border-radius: 4px;';
    progressContainer.innerHTML = `
        <div style="margin-bottom: 5px; font-weight: bold; color: #333;">
            Video wird hochgeladen: <span id="progress-text">0%</span>
        </div>
        <div style="width: 100%; background: #ddd; height: 20px; border-radius: 10px; overflow: hidden;">
            <div id="progress-bar" style="width: 0%; height: 100%; background: #417690; transition: width 0.2s;"></div>
        </div>
    `;

    // Füge den Ladebalken über den Speichern-Buttons ein
    const submitRow = document.querySelector('.submit-row');
    if (submitRow) {
        submitRow.parentNode.insertBefore(progressContainer, submitRow);
    }

    // Beim Absenden des Formulars per AJAX hochladen
    form.addEventListener('submit', function (e) {
        // Nur wenn tatsächlich eine neue Datei ausgewählt wurde
        if (fileInput.files.length > 0) {
            e.preventDefault(); // Verhindert das normale Seiten-Neuladen

            const formData = new FormData(form);
            const xhr = new XMLHttpRequest();

            // Fortschritts-Event
            xhr.upload.addEventListener('progress', function (e) {
                if (e.lengthComputable) {
                    const percent = Math.round((e.loaded / e.total) * 100);
                    progressContainer.style.display = 'block';
                    document.getElementById('progress-bar').style.width = percent + '%';
                    document.getElementById('progress-text').innerText = percent + '%';
                }
            });

            // Wenn der Upload fertig ist
            xhr.addEventListener('load', function () {
                if (xhr.status >= 200 && xhr.status < 400) {
                    // Nach erfolgreichem Upload zur Übersicht/Erfolgsseite weiterleiten
                    window.location.href = window.location.href;
                } else {
                    alert('Fehler beim Upload!');
                }
            });

            xhr.open('POST', form.action || window.location.href, true);
            xhr.send(formData);
        }
    });
});