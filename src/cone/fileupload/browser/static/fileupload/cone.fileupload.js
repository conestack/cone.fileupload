var cone_fileupload = (function (exports, $) {
    'use strict';

    function show_file(evt, url) {
        evt.preventDefault();
        bdajax.path({
            path: bdajax.parsepath(url),
            target: url,
            event: 'contextchanged:#layout'
        });
        bdajax.trigger('contextchanged', '#layout', url);
    }
    class Fileupload {
        static initialize(context) {
            let fileupload = $('#fileupload', context);
            if (!fileupload.length) {
                return;
            }
            new Fileupload(fileupload);
        }
        constructor(elem) {
            this.elem = elem;
            elem.fileupload({
                sequentialUploads: true,
                messages: fileupload_i18n_messages
            });
            let accept_file_types = elem.data('accept_file_types');
            if (accept_file_types) {
                elem.fileupload('option', {
                    acceptFileTypes: eval(accept_file_types)
                });
            }
            this.add_files_handle = this.add_files_handle.bind(this);
            $('#toolbaraction-add-files', elem)
                .off()
                .on('click', this.add_files_handle);
            this.load_existing();
        }
        add_files_handle(evt) {
            evt.preventDefault();
            $('input:file', this.elem).click();
        }
        load_existing() {
            this.elem.addClass('fileupload-processing');
            $.ajax({
                url: this.elem.data('url'),
                dataType: 'json',
                context: this.elem[0]
            }).always(function () {
                $(this).removeClass('fileupload-processing');
            }).done(function (result) {
                $(this).fileupload('option', 'done').call(
                    this, $.Event('done'), {result: result});
            });
        }
    }

    $(function() {
        bdajax.register(Fileupload.initialize, true);
    });

    exports.Fileupload = Fileupload;
    exports.show_file = show_file;

    Object.defineProperty(exports, '__esModule', { value: true });

    return exports;

})({}, jQuery);
