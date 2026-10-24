import $ from 'jquery';

import { Fileupload } from './fileupload.js';

export * from './fileupload.js';

$(() => {
    bdajax.register(Fileupload.initialize, true);
});
