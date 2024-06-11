$(document).ready(function() {
    $('#similar_cafes').select2();
});

function formatKey(key) {
    return key.split('_')
              .map(word => word.charAt(0).toUpperCase() + word.slice(1))
              .join(' ');
}

document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("addCafeForm");
    const formFeedback = document.getElementById("formFeedback");

    form.addEventListener("submit", function(event) {
        event.preventDefault(); // Prevent the form from submitting through the standard form action

        let formData = {
            name: document.getElementById("name").value.trim(),
            image_url: document.getElementById("image").value.trim(),
            neighbourhood: document.getElementById("neighbourhood").value.trim(),
            address: document.getElementById("address").value.trim(),
            summary: document.getElementById("summary").value.trim(),
            price_range: document.getElementById("price_range").value.trim(),
            stars: document.getElementById("stars").value.trim(),
            similar_cafes: $('#similar_cafes').val() || [],

            // Splitting comma-separated strings into arrays
            menu_highlights: document.getElementById("menu_highlights").value.split(',').map(item => item.trim()),
            amenities: document.getElementById("amenities").value.split(',').map(item => item.trim()),
        };

        $.ajax({
            url: '/add',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(formData),
            dataType: 'json',
            success: function(response) {
                console.log(response);
                form.reset(); // Reset the form on successful data submission
                formFeedback.innerHTML = `<div class="alert alert-success" role="alert">
                                            Café added successfully. <a href="/view/${response.id}">See it here</a>
                                          </div>`;
                document.getElementById("cafeName").focus(); // Focus on the first input field for the next entry
            },
            error: function(xhr) {
                let errorMessage = 'An unexpected error occurred';
                try {
                    const errors = JSON.parse(xhr.responseText).errors;
                    errorMessage = 'Please correct the following errors:<br>';
                    Object.keys(errors).forEach(function(key) {
                        errorMessage += `<strong>${formatKey(key)}:</strong> ${errors[key]}<br>`;
                    });
                } catch (e) {
                    console.error('Error parsing response:', e);
                }
                formFeedback.innerHTML = `<div class="alert alert-danger" role="alert">${errorMessage}</div>`;
            }
        });
    });
});
