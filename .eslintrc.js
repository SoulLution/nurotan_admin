module.exports = {
  root: true,
  env: {
    browser: true,
    node: true,
    es6: true
  },
  parserOptions: {
    ecmaVersion: 6,
    sourceType: "module",
    parser: "babel-eslint"
  },
  // parser: "vue",
  extends: [
    "eslint:recommended",
    "plugin:vue/recommended",
    "plugin:prettier/recommended"
  ],
  plugins: ["vue", "prettier"],
  rules: {
    semi: ["error", "never"],
    "no-console": "off",
    "vue/max-attributes-per-line": "off",
    "vue/singleline-html-element-content-newline": "off",
    "vue/multiline-html-element-content-newline": "off",
    "vue/html-self-closing": [
      "error",
      {
        html: {
          void: "always",
          normal: "never",
          component: "any"
        }
      }
    ],
    "prettier/prettier": ["error", { endOfLine: "auto", semi: false }]
  }
}
