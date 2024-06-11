$(document).ready(function() {
    $('#searchForm').on('submit', function(e) {
        let searchQuery = $('#searchQuery').val().trim();

        if (!searchQuery) {
            e.preventDefault(); // Prevent form submission
            $('#searchQuery').val(''); // Clear the search box
            $('#searchQuery').focus(); // Focus on the search box
        }
    });
});

