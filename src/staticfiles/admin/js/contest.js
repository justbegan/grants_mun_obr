django.jQuery(function($) {
    //contest documentss inline
    $('tr:not(.empty-form) .field-tags select').selectize({
        placeholder: 'Выберите тэги',
        plugins: ['remove_button']
    });
    $(document).on('formset:added', function(event, $row, formsetName) {
        $row.find('.field-tags select').selectize({
            placeholder: 'Выберите тэги',
            plugins: ['remove_button']
        });
    });

    //documents form
    if ($('#document_form').length) {
        $('#id_tags').selectize({
            placeholder: 'Выберите тэги',
            plugins: ['remove_button']
        });
    }
});