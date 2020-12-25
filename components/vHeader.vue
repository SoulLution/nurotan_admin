<template>
  <header class="head flex flex-row justify-between bg-white pl-22 pr-6">
    <router-link to="/" class="flex flex-row items-center">
      <img src="nur_otan.png" />
    </router-link>
    <nav class="flex flex-row items-center">
      <router-link v-if="checkOnAdmin" class="px-4 py-8" to="/">
        Конструктор диалогов
      </router-link>
      <router-link v-if="checkOnAdmin" class="px-4 py-8" to="/workers">
        Администрация
      </router-link>
      <router-link class="px-4 py-8" to="/confirm">
        Заявки
      </router-link>
      <router-link class="px-4 py-8" to="/dialogs">Чат</router-link>
    </nav>
    <div
      class="flex flex-row items-center relative"
      @mousemove="menu = true"
      @mouseleave="menu = false"
    >
      <div class="flex flex-col justify-center">
        <h4 class="text-h4 font-bold text-d_blue">{{ user.full_name }}</h4>
        <span class="txt-l_blue">{{
          checkOnAdmin ? "Администратор" : "Менеджер"
        }}</span>
      </div>
      <div
        class="ava rounded-full border-4 border-red mx-4 overflow-hidden"
        style="background-image: url(nur_otan_logo.png)"
      ></div>
      <img src="select_arrow.svg" />

      <transition name="fade-settings">
        <div v-show="menu" class="settings bg-white absolute flex flex-col">
          <div
            class="py-2 px-4 cursor-pointer hover:bg-cyan hover:text-white transition duration-150 "
            @click="signout()"
          >
            Выйти
          </div>
        </div>
      </transition>
    </div>
  </header>
</template>

<script>
export default {
  data() {
    return {
      menu: false,
      user: JSON.parse(localStorage.getItem("auth"))
    }
  },
  computed: {
    checkOnAdmin() {
      return this.user && this.user.is_admin == 1
    }
  },
  created() {
    if (!this.user) this.signout()
  },
  methods: {
    signout() {
      localStorage.setItem("auth", "")
      this.$router.push("/sign")
    }
  }
}
</script>

<style lang="scss" scoped>
.head {
  box-shadow: 0px 2px 2px 0px rgba(50, 50, 50, 0.32);
  & .ava {
    max-width: 50px;
    max-height: 50px;
    min-width: 50px;
    min-height: 50px;
    background-position: 50%;
    background-size: 100%;
    background-repeat: no-repeat;
    background-image: url("/nur_otan_logo.png");
  }
  & nav {
    & > a {
      position: relative;
      min-width: 200px;
      text-align: center;
      &:after {
        content: "";
        position: absolute;
        bottom: 0;
        left: 0;
        height: 100%;
        width: 100%;
        max-height: 0;
        background-color: #008fa0;
        transition: 0.3s;
      }
      &:hover {
        &:after {
          background-color: #52c0cc;
          max-height: 4px;
        }
      }
      &.nuxt-link-exact-active {
        &:after {
          background-color: #008fa0;
          max-height: 4px;
        }
      }
    }
  }
  & .settings {
    height: auto;
    max-height: 100%;
    width: 100%;
    bottom: 0;
    right: 0;
    transform: translateY(100%);
    overflow: hidden;
    box-shadow: 0px 1px 6px #000000;
    &.fade-settings-enter-active,
    &.fade-settings-leave-active {
      transition: 0.3s;
    }
    &.fade-settings-enter,
    &.fade-settings-leave-to {
      max-height: 0%;
    }
  }
}
</style>
