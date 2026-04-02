/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./**/templates/**/*.html",
    "./**/*.py",
    "./static/**/*.js",
  ],

  theme: {
    extend: {},
  },

  safelist: [
    "md:rounded-[20px]",
    "md:hover:scale-[1.2]",
    "md:hover:[text-shadow:0_10px_4px_rgba(0,0,0,0.4)]",
    "btn",
    "tag",
    "recipe",
    "active-slider",
    "scrollbar-hide",
    "step",
    "items-baseline"
  ],

  plugins: [],
}