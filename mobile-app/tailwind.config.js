/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./App.{js,jsx,ts,tsx}", "./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: "#10b981", // Emerald 500
        secondary: "#047857", // Emerald 700
        dark: "#1f2937",
        light: "#f3f4f6"
      }
    },
  },
  plugins: [],
}
