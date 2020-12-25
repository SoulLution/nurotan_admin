const colors = {
  yellow: "#F9DB3D",
  cyan: "#008FA0",
  grey: "#F9F9F9",
  dark: "#242424",
  red: "#D42D11",
  d_blue: "#003360",
  l_blue: "#8AA1C1",
  blue: "#2C5DE5",
  svg_default: "#7E98AE",
  C4: "#C4C4C4"
}

module.exports = {
  theme: {
    extend: {
      opacity: {
        "10": "0.1",
        "60": "0.6"
      }
    },
    backgroundColor: theme => ({
      ...theme("colors"),
      ...colors
    }),
    textColor: theme => ({
      ...theme("colors"),
      ...colors
    }),
    borderColor: theme => ({
      ...theme("colors"),
      ...colors
    }),
    fontSize: {
      xs: ".75rem",
      sm: ".875rem",
      base: "1rem",
      lg: "1.125rem",
      xl: "1.25rem",
      h4: "1.375rem",
      "2xl": "1.5rem",
      "3xl": "1.875rem",
      "4xl": "2.25rem",
      "5xl": "3rem",
      "6xl": "4rem",
      "7xl": "5rem"
    },
    spacing: {
      1: "0.25rem",
      2: "0.5rem",
      3: "0.75rem",
      4: "1rem",
      5: "1.25rem",
      6: "1.5rem",
      7: "1.75rem",
      8: "2rem",
      9: "2.25rem",
      10: "2.5rem",
      11: "2.75rem",
      12: "3rem",
      14: "3.5rem",
      15: "3.75rem",
      13: "3.25rem",
      21: "5.25rem",
      22: "5.5rem",
      24: "6rem",
      "70px": "70px"
    },
    borderRadius: {
      none: "0",
      sm: "0.125rem",
      md: "0.3125rem",
      lg: "0.5rem",
      5: "5px",
      10: "10px",
      20: "20px",
      27: "27px",
      30: "30px",
      full: "9999px",
      large: "12px"
    }
  },
  variants: {
    backgroundColor: ["responsive", "hover", "focus", "active"],
    textColor: ["responsive", "hover", "focus", "active"]
  },
  plugins: [],
  purge: {
    // Learn more on https://tailwindcss.com/docs/controlling-file-size/#removing-unused-css
    enabled: process.env.NODE_ENV === "production",
    content: [
      "components/**/*.vue",
      "layouts/**/*.vue",
      "pages/**/*.vue",
      "plugins/**/*.js",
      "nuxt.config.js"
    ]
  }
}
