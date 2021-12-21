import $ from 'jquery';

import {Fileupload} from './fileupload.js';

export * from './fileupload.js';

$(function() {
    bdajax.register(Fileupload.initialize, true);
});
