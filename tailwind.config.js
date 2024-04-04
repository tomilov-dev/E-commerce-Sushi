/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./backend/**/*.{html,js}"],
  theme: {
    extend: {
      colors: {
        prim: "#fff7ed",
        sec: {
          DEFAULT: "#f8fafc",
          100: "#f1f5f9",
          200: "#e2e8f0",
        },
        accent: "#fda4af",
        icons: "#f87171",
      },
    },
  },
  plugins: [require("@tailwindcss/forms")],
};
