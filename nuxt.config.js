export default {
  ssr: false,
  server: {
    port: 3000, // default: 3000
    host: "localhost" // default: localhost
    // host: "185.22.64.75" // default: localhost
  },
  // Global page headers (https://go.nuxtjs.dev/config-head)
  head: {
    title: "Admin",
    meta: [
      { charset: "utf-8" },
      { name: "viewport", content: "width=device-width, initial-scale=1" },
      { hid: "description", name: "description", content: "" }
    ],
    link: [{ rel: "icon", type: "image/x-icon", href: "/favicon.ico" }]
  },

  // Global CSS (https://go.nuxtjs.dev/config-css)
  css: [
    { src: "~assets/scss/main.scss", lang: "scss" },
    { src: "~assets/scss/colors.scss", lang: "scss" },
    { src: "vue-multiselect/dist/vue-multiselect.min.css" },
    { src: "vue-date-pick/dist/vueDatePick.css" }
  ],

  // Plugins to run before rendering page (https://go.nuxtjs.dev/config-plugins)
  plugins: ["~/plugins/emoji-picker.js"],

  // Auto import components (https://go.nuxtjs.dev/config-components)
  components: true,

  // Modules for dev and build (recommended) (https://go.nuxtjs.dev/config-modules)
  buildModules: [
    // https://go.nuxtjs.dev/eslint
    "@nuxtjs/eslint-module",
    // https://go.nuxtjs.dev/tailwindcss
    "@nuxtjs/tailwindcss"
  ],

  // Modules (https://go.nuxtjs.dev/config-modules)
  modules: [
    // https://go.nuxtjs.dev/axios
    "@nuxtjs/moment",
    "@nuxtjs/axios"
  ],

  // Axios module configuration (https://go.nuxtjs.dev/config-axios)
  axios: {
    baseURL: "http://185.22.64.75:3143/"
  },

  // Build Configuration (https://go.nuxtjs.dev/config-build)
  build: {
    port: 8779,
    /*
     ** You can extend webpack config here
     */
    extend(config, ctx) {
      // Run ESLint on save
      if (ctx.isDev && ctx.isClient) {
        config.module.rules.push({
          enforce: "pre",
          test: /\.(js|vue)$/,
          loader: "eslint-loader",
          exclude: /(node_modules)/
        })
      }
    }
  }
}
