module.exports = {
  content: ["./**/templates/**/*.html"],
  theme: {
    extend: {
      colors: {
        primary: "var(--primary-color)",
        "primary-light": "var(--primary-color-light)",
        background: "var(--background-color)",
        seconday: "var(--secondary-color)",
        third: "var(--third-color)",
      },
    },
  },
  plugins: [],
};
