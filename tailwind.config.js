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
        'primary':'#C44728',
        'secondary':'#e8aa8b',
        'accent':'#590BD6',
        'neutral':'#907123',
        'info':'#b5dff7',
        'success':'#39aa67',
        'warning':'#f1dd7c',
        'error':'#FF0000',
        'base-0':'#FFFFFF',
        'base-100':'#FBF7EE',
        'base-200':'#F7F0DE',
        'base-300':'#F3E8CE',
      }
    })
  ]
};
