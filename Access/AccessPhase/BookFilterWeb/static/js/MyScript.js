$(document).ready(function() {
    // Hide all inputs initially except radio buttons
    $('.input-group, .form-select, .form-check-input:not([type="radio"]), .form-range, #span_Stars, #span_Avail').hide();

    // Show the corresponding input when a radio button is clicked
    $('input[type="radio"]').click(function() {
        // Hide all inputs
        $('.input-group, .form-select, .form-check-input:not([type="radio"]), .form-range, #span_Stars, #span_Avail').hide();

        $('input[type="text"], input[type="number"], input[type="checkbox"], input[type="range"], select').val('').prop('checked', false);

        // Show the input corresponding to the selected radio button
        if (this.id === 'r_searchTitle') {
            $('#i_Title').closest('.input-group').show();
        } else if (this.id === 'r_searchDesc') {
            $('#i_Desc').closest('.input-group').show();
        } else if (this.id === 'r_searchGenre') {
            $('.form-select').show();
        } else if (this.id === 'r_filterPrice') {
            $('#i_minPrice').closest('.input-group').show();
            $('#i_maxPrice').closest('.input-group').show();
        } else if (this.id === 'r_inStock') {
            $('#i_inStock').closest('.form-check').show();
            $('#i_inStock').show();
        } else if (this.id === 'r_filterStars') {
            $('#i_starsRange').show();
            $('#span_Stars').show();
        } else if (this.id === 'r_filterAvail') {
            $('#i_availRange').show();
            $('#span_Avail').show();
        }
    });

    // Trigger click on the checked radio button to show the corresponding input on page load
    $('input[type="radio"]:checked').click();


    $('.toggle-link').click(function() {
        var $textContainer = $(this).prev('.text-container');
        $textContainer.toggleClass('expanded');
        $(this).text($textContainer.hasClass('expanded') ? 'See less' : 'See more');
    });
});