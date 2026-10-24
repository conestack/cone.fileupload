import $ from 'jquery';

QUnit.module('cone.fileupload.bundle', (hooks) => {
    hooks.afterEach(() => {
        delete window.bdajax;
    });

    QUnit.test('bundle exports Fileupload and registers it on DOM ready', async (assert) => {
        const registered = [];
        window.bdajax = {
            register: (func, instant) => {
                registered.push({ func, instant });
            },
        };

        const bundle = await import('../src/bundle.js');
        // ready callbacks run in registration order, this one after the bundle's
        await new Promise((resolve) => $(resolve));

        assert.deepEqual(Object.keys(bundle).sort(), ['Fileupload', 'show_file'], 'exported names');
        assert.strictEqual(registered.length, 1, 'one registration');
        assert.strictEqual(
            registered[0].func,
            bundle.Fileupload.initialize,
            'initialize registered',
        );
        assert.true(registered[0].instant, 'registered for instant execution');
    });
});
