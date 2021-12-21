import $ from 'jquery';

export function show_file(evt, url) {
    evt.preventDefault();
    bdajax.path({
        path: bdajax.parsepath(url),
        target: url,
        event: 'contextchanged:#layout'
    });
    bdajax.trigger('contextchanged', '#layout', url);
}

export class Fileupload {

    static initialize(context) {
        let fileupload = $('#fileupload', context);
        if (!fileupload.length) {
            return;
        }
        new Fileupload(fileupload);
    }

    constructor(elem) {
        this.elem = elem;
        // initialize fileupload plugin
        elem.fileupload({
            sequentialUploads: true,
            messages: fileupload_i18n_messages
        });
        // check accept file types
        let accept_file_types = elem.data('accept_file_types');
        if (accept_file_types) {
            elem.fileupload('option', {
                acceptFileTypes: eval(accept_file_types)
            });
        }
        // bind add files action
        this.add_files_handle = this.add_files_handle.bind(this);
        $('#toolbaraction-add-files', elem)
            .off()
            .on('click', this.add_files_handle);
        // load existing files
        this.load_existing();
    }

    add_files_handle(evt) {
        evt.preventDefault();
        $('input:file', this.elem).click();
    }

    load_existing() {
        // load existing files
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
