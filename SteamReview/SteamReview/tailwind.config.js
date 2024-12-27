/** @type {import('tailwindcss').Config} */
module.exports = {
    purge: [
        './templates/*.html',
    ],
    theme: {
        extend: {
            lineClamp: {
                12: '12',
            }
        },
    },
    plugins: [
        require('@tailwindcss/line-clamp'),
    ],
}
