/*
 * cone.fileupload JS
 */

(function($) {

    $(document).ready(function() {
        // initial binding
        cone_fileupload.binder();

        // add binders to bdajax binding callbacks
        $.extend(bdajax.binders, {
            cone_fileupload_binder: cone_fileupload.binder
        });
    });

    cone_fileupload = {
        binder: function(context) {
            var fileupload = $('#fileupload', context);
            if (!fileupload.length) {
                return;
            }
            fileupload.fileupload();
            fileupload.addClass('fileupload-processing');
            $.ajax({
                url: fileupload.attr('action'),
                dataType: 'json',
                context: fileupload[0]
            }).always(function () {
                $(this).removeClass('fileupload-processing');
            }).done(function (result) {
                $(this).fileupload('option', 'done').call(
                    this, $.Event('done'), {result: result});
            });
        }
    };

})(jQuery);
