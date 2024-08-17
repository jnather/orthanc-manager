document.addEventListener("DOMContentLoaded", function() {
    const deleteForms = document.querySelectorAll(".delete-form");

    deleteForms.forEach(form => {
        form.addEventListener("submit", function(event) {
            event.preventDefault();
            const modal = document.createElement('div');
            modal.className = 'modal';
            modal.innerHTML = `
                <div class="modal-content">
                    <h2>Confirm Deletion</h2>
                    <p>Are you sure you want to delete this modality?</p>
                    <button id="confirm" class="btn btn-danger">Delete</button>
                    <button id="cancel" class="btn btn-secondary">Cancel</button>
                </div>
            `;
            document.body.appendChild(modal);

            document.getElementById('confirm').addEventListener('click', function() {
                form.submit();
            });

            document.getElementById('cancel').addEventListener('click', function() {
                document.body.removeChild(modal);
            });
        });
    });
});
