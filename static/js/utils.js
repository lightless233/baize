/**
 * Created by lightless on 2017/2/19.
 */

function makeNoty (type, message, layout="topRight") {
    noty({
        text: message,
        theme: 'metroui',
        type: type,
        layout: layout,
        animation: {
            open: {height: 'toggle'},
            close: {height: 'toggle'},
            easing: 'swing',
            speed: '500',
        },
        timeout: 3000,
    });
}
