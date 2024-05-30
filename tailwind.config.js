/** @type {import('tailwindcss').Config} */

const { createThemes } = require('tw-colors');

module.exports = {
  content: ["./backend/**/*.{html,js}"],
  theme: {},
  plugins: [
    require("@tailwindcss/forms"), 
    require('flowbite/plugin'),
    createThemes({
      "light": {
        'primary':'#e8aa8b',
        'secondary':'#cc5a3d',
        'accent':'#97BE5A',
        'neutral':'#907123',
        'info':'#b5dff7',
        'success':'#39aa67',
        'warning':'#f1dd7c',
        'error':'#FF0000',
        'base-100':'#f5eee6',
        'base-200':'#FFE8C5',
        'base-300':'#e9d9cb',
      }
    })
  ]
};
