$(document).ready(function() {
    // Initialize Select2 for menu_highlights and amenities
    $('#menu_highlights, #amenities').select2({
        tags: true, // Allow new tags
        tokenSeparators: [',', '\n'], // Split tags by commas and new lines
    });

    // Initialize Select2 for similar_cafes without tags, preventing arbitrary values
    $('#similar_cafes').select2();

    $('form').off('submit').on('submit', function (e) {
        e.preventDefault(); // Prevent the default form submission

        let formData = {
            name: $('#name').val(),
            image_url: $('#image_url').val(),
            neighbourhood: $('#neighbourhood').val(),
            address: $('#address').val(),
            summary: $('#summary').val(),
            price_range: $('#price_range').val(),
            stars: $('#stars').val(),
            menu_highlights: $('#menu_highlights').val(),
            amenities: $('#amenities').val(),
            similar_cafes: $('#similar_cafes').val()
        };

        const id = window.location.pathname.split('/').pop(); // Extract the item ID from the URL

        $.ajax({
            url: '/edit/' + id,
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(formData),
            success: function (response) {
                if (response.success) {
                    window.location.href = '/view/' + id;
                } else {
                    console.error(response.errors || response.message);
                }
            },
            error: function (xhr) {
                let response = JSON.parse(xhr.responseText);
                let errorMessages = '';

                if (response.errors) {
                    errorMessages = Object.keys(response.errors).map(key => response.errors[key]).join('<br>');
                } else {
                    errorMessages = 'An error occurred: ' + response.message;
                }

                // Set the error messages inside the modal body
                $('#errorModalBody').html(errorMessages);

                // Show the modal
                let errorModal = new bootstrap.Modal(document.getElementById('errorModal'), {
                  keyboard: true
                });
                errorModal.show();
            }
        });
    });
    $('#discardChangesButton').on('click', function(e) {
        e.preventDefault();
        let href = $(this).attr('href'); // Store the href to use on confirmation

        // Trigger the Bootstrap modal
        let confirmModal = new bootstrap.Modal(document.getElementById('confirmModal'), {
          keyboard: false
        });
        confirmModal.show();

        $('#confirmDiscard').on('click', function() {
            window.location.href = $('#discardChangesButton').attr('href'); // Redirect on confirmation
        });

        // Explicitly handle the modal close on "No"
        $('#closeModal').on('click', function() {
            confirmModal.hide();
        });
    });
    $('#errorModal').on('click', function() {
        $('#errorModal').modal('hide'); // Explicitly hide the error modal
    });
});