import cleanup from 'rollup-plugin-cleanup';
import {terser} from 'rollup-plugin-terser';

let out_path = 'src/cone/fileupload/browser/static/fileupload';

export default args => {
    let conf = {
        input: 'js/src/bundle.js',
        plugins: [
            cleanup()
        ],
        output: [{
            file: `${out_path}/cone.fileupload.js`,
            name: 'cone_fileupload',
            format: 'iife',
            globals: {
                jquery: 'jQuery'
            },
            interop: 'default',
            sourcemap: false
        }],
        external: [
            'jquery'
        ]
    };
    if (args.configDebug !== true) {
        conf.output.push({
            file: `${out_path}/cone.fileupload.min.js`,
            name: 'cone_fileupload',
            format: 'iife',
            plugins: [
                terser()
            ],
            globals: {
                jquery: 'jQuery'
            },
            interop: 'default',
            sourcemap: false
        });
    }
    return conf;
};
