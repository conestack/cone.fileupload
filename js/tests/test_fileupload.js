import $ from 'jquery';
import {show_file, Fileupload} from '../src/fileupload.js';

QUnit.module('cone.fileupload.show_file', hooks => {

    let bdajax_origin;

    hooks.beforeEach(() => {
        bdajax_origin = window.bdajax;
        window.bdajax = {
            parsepath: function(url) {
                return url.replace(/^https?:\/\/[^\/]+/, '');
            },
            path: function(opts) {},
            trigger: function(evt, selector, url) {}
        };
    });

    hooks.afterEach(() => {
        window.bdajax = bdajax_origin;
    });

    QUnit.test('show_file calls bdajax.path with correct options', assert => {
        let path_opts;
        window.bdajax.path = function(opts) {
            path_opts = opts;
        };

        let evt = $.Event('click');
        let url = 'http://example.com/path/to/file';

        show_file(evt, url);

        assert.true(evt.isDefaultPrevented());
        assert.strictEqual(path_opts.path, '/path/to/file');
        assert.strictEqual(path_opts.target, url);
        assert.strictEqual(path_opts.event, 'contextchanged:#layout');
    });

    QUnit.test('show_file triggers contextchanged event', assert => {
        let trigger_args;
        window.bdajax.trigger = function(evt, selector, url) {
            trigger_args = {evt, selector, url};
        };

        let evt = $.Event('click');
        let url = 'http://example.com/some/path';

        show_file(evt, url);

        assert.strictEqual(trigger_args.evt, 'contextchanged');
        assert.strictEqual(trigger_args.selector, '#layout');
        assert.strictEqual(trigger_args.url, url);
    });
});

QUnit.module('cone.fileupload.Fileupload.initialize', hooks => {

    let container;

    hooks.beforeEach(() => {
        container = $('<div />').appendTo('body');
        window.fileupload_i18n_messages = {};
        $.fn.fileupload = function() { return this; };
    });

    hooks.afterEach(() => {
        container.remove();
        delete window.fileupload_i18n_messages;
        delete $.fn.fileupload;
    });

    QUnit.test('initialize does nothing if no #fileupload element', assert => {
        let initialized = false;
        let orig_fileupload = $.fn.fileupload;
        $.fn.fileupload = function() {
            initialized = true;
            return this;
        };

        Fileupload.initialize(container);

        assert.false(initialized);
        $.fn.fileupload = orig_fileupload;
    });

    QUnit.test('initialize creates Fileupload instance when element exists', assert => {
        let fileupload_called = false;
        $.fn.fileupload = function() {
            fileupload_called = true;
            return this;
        };

        $('<div id="fileupload" data-url="/files" />').appendTo(container);

        Fileupload.initialize(container);

        assert.true(fileupload_called);
    });
});

QUnit.module('cone.fileupload.Fileupload.constructor', hooks => {

    let container,
        elem,
        ajax_origin;

    hooks.beforeEach(() => {
        ajax_origin = $.ajax;
        $.ajax = function() {
            return {
                always: function() { return this; },
                done: function() { return this; }
            };
        };

        container = $('<div />').appendTo('body');
        elem = $(`
            <div id="fileupload" data-url="/files">
                <div class="fileupload-empty"></div>
                <input type="file" />
                <button id="toolbaraction-add-files"></button>
            </div>
        `).appendTo(container);

        window.fileupload_i18n_messages = {error: 'Error'};

        $.fn.fileupload = function(action, opts) {
            if (typeof action === 'object') {
                this.data('fileupload-opts', action);
            } else if (action === 'option') {
                this.data('fileupload-option', opts);
            }
            return this;
        };
    });

    hooks.afterEach(() => {
        container.remove();
        $.ajax = ajax_origin;
        delete window.fileupload_i18n_messages;
        delete $.fn.fileupload;
    });

    QUnit.test('constructor initializes fileupload plugin', assert => {
        new Fileupload(elem);

        let opts = elem.data('fileupload-opts');
        assert.true(opts.sequentialUploads);
        assert.strictEqual(opts.messages, window.fileupload_i18n_messages);
    });

    QUnit.test('constructor sets acceptFileTypes if data attribute exists', assert => {
        elem.data('accept_file_types', '/\\.(gif|jpg)$/i');

        new Fileupload(elem);

        let option = elem.data('fileupload-option');
        assert.ok(option.acceptFileTypes);
    });

    QUnit.test('constructor binds add files button handler', assert => {
        new Fileupload(elem);

        let input_clicked = false;
        $('input:file', elem).on('click', () => {
            input_clicked = true;
        });

        $('#toolbaraction-add-files', elem).trigger('click');

        assert.true(input_clicked);
    });

    QUnit.test('delete click shows empty message when last item', assert => {
        $('<div class="template-download" />').appendTo(elem);
        $('<button class="delete" />').appendTo(elem);

        new Fileupload(elem);

        $('.fileupload-empty', elem).hide();
        $('.delete', elem).trigger('click');

        assert.strictEqual($('.fileupload-empty', elem).css('display'), 'block');
    });

    QUnit.test('delete click does not show empty when multiple items', assert => {
        $('<div class="template-download" />').appendTo(elem);
        $('<div class="template-download" />').appendTo(elem);
        $('<button class="delete" />').appendTo(elem);

        new Fileupload(elem);

        $('.fileupload-empty', elem).hide();
        $('.delete', elem).trigger('click');

        assert.strictEqual($('.fileupload-empty', elem).css('display'), 'none');
    });
});

QUnit.module('cone.fileupload.Fileupload.add_files_handle', hooks => {

    let container,
        elem,
        ajax_origin;

    hooks.beforeEach(() => {
        ajax_origin = $.ajax;
        $.ajax = function() {
            return {
                always: function() { return this; },
                done: function() { return this; }
            };
        };

        container = $('<div />').appendTo('body');
        elem = $(`
            <div id="fileupload" data-url="/files">
                <div class="fileupload-empty" style="display: block;"></div>
                <input type="file" />
                <button id="toolbaraction-add-files"></button>
            </div>
        `).appendTo(container);

        window.fileupload_i18n_messages = {};
        $.fn.fileupload = function() { return this; };
    });

    hooks.afterEach(() => {
        container.remove();
        $.ajax = ajax_origin;
        delete window.fileupload_i18n_messages;
        delete $.fn.fileupload;
    });

    QUnit.test('add_files_handle prevents default and triggers file input', assert => {
        let fileupload = new Fileupload(elem);

        let input_clicked = false;
        $('input:file', elem).on('click', (e) => {
            e.preventDefault();
            input_clicked = true;
        });

        let evt = $.Event('click');
        fileupload.add_files_handle(evt);

        assert.true(evt.isDefaultPrevented());
        assert.true(input_clicked);
    });

    QUnit.test('add_files_handle hides empty message', assert => {
        let fileupload = new Fileupload(elem);

        let evt = $.Event('click');
        fileupload.add_files_handle(evt);

        assert.strictEqual($('.fileupload-empty', elem).css('display'), 'none');
    });
});

QUnit.module('cone.fileupload.Fileupload.load_existing', hooks => {

    let container,
        elem,
        ajax_origin;

    hooks.beforeEach(() => {
        ajax_origin = $.ajax;
        container = $('<div />').appendTo('body');
        elem = $(`
            <div id="fileupload" data-url="/api/files">
                <div class="fileupload-empty" style="display: block;"></div>
            </div>
        `).appendTo(container);

        window.fileupload_i18n_messages = {};

        $.fn.fileupload = function(action, opts) {
            if (action === 'option') {
                return function() {};
            }
            return this;
        };
    });

    hooks.afterEach(() => {
        container.remove();
        $.ajax = ajax_origin;
        delete window.fileupload_i18n_messages;
        delete $.fn.fileupload;
    });

    QUnit.test('load_existing makes AJAX request with correct params', assert => {
        let ajax_opts;
        $.ajax = function(opts) {
            ajax_opts = opts;
            return {
                always: function() { return this; },
                done: function() { return this; }
            };
        };

        new Fileupload(elem);

        assert.strictEqual(ajax_opts.url, '/api/files');
        assert.strictEqual(ajax_opts.dataType, 'json');
    });

    QUnit.test('load_existing adds processing class', assert => {
        $.ajax = function() {
            return {
                always: function() { return this; },
                done: function() { return this; }
            };
        };

        new Fileupload(elem);

        assert.true(elem.hasClass('fileupload-processing'));
    });

    QUnit.test('load_existing removes processing class on always', assert => {
        let always_callback;
        $.ajax = function(opts) {
            return {
                always: function(cb) {
                    always_callback = cb;
                    return this;
                },
                done: function() { return this; }
            };
        };

        new Fileupload(elem);
        always_callback.call(elem[0]);

        assert.false(elem.hasClass('fileupload-processing'));
    });

    QUnit.test('load_existing hides empty when files exist', assert => {
        let done_callback;
        $.ajax = function(opts) {
            return {
                always: function() { return this; },
                done: function(cb) {
                    done_callback = cb;
                    return this;
                }
            };
        };

        $.fn.fileupload = function(action, name) {
            if (action === 'option' && name === 'done') {
                return function() {};
            }
            return this;
        };

        new Fileupload(elem);
        done_callback.call(elem[0], {files: [{name: 'test.txt'}]});

        assert.strictEqual($('.fileupload-empty', elem).css('display'), 'none');
    });

    QUnit.test('load_existing keeps empty visible when no files', assert => {
        let done_callback;
        $.ajax = function(opts) {
            return {
                always: function() { return this; },
                done: function(cb) {
                    done_callback = cb;
                    return this;
                }
            };
        };

        $.fn.fileupload = function(action, name) {
            if (action === 'option' && name === 'done') {
                return function() {};
            }
            return this;
        };

        new Fileupload(elem);
        done_callback.call(elem[0], {files: []});

        assert.strictEqual($('.fileupload-empty', elem).css('display'), 'block');
    });
});
