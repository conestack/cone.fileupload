import cleanup from 'rollup-plugin-cleanup';
import terser from '@rollup/plugin-terser';

const out_dir = 'src/cone/fileupload/browser/static/fileupload';

export default args => {
    let conf = {
        input: 'js/src/bundle.js',
        plugins: [
            cleanup()
        ],
        output: [{
            file: `${out_dir}/cone.fileupload.js`,
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
            file: `${out_dir}/cone.fileupload.min.js`,
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
