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
            // lookup fileupload form
            var fileupload = $('#fileupload', context);
            // return if not present
            if (!fileupload.length) {
                return;
            }
            // initialize fileupload plugin
            fileupload.fileupload({
                sequentialUploads: true,
                messages: fileupload_i18n_messages,
                disableImagePreview: fileupload.data('disable_image_preview'),
                disableVideoPreview: fileupload.data('disable_video_preview'),
                disableAudioPreview: fileupload.data('disable_audio_preview')
            });
            // check accept file types
            accept_file_types = fileupload.data('accept_file_types');
            if (accept_file_types) {
                fileupload.fileupload('option', {
                    acceptFileTypes: eval(accept_file_types)
                });
            }
            // load existing files
            fileupload.addClass('fileupload-processing');
            $.ajax({
                url: fileupload.data('url'),
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
