<template>
  <div class="sign flex justify-center items-center h-full">
    <div class="content bg-white rounded-27">
      <div class="flex flex-row pb-6 items-center">
        <img src="nur_otan_logo.png" />
        <h2 class="text-2xl font-bold text-yellow ml-16">
          ВХОД В УЧЕТНУЮ ЗАПИСЬ
        </h2>
      </div>
      <div class="flex flex-col pt-13">
        <v-input
          id="email"
          v-model="login"
          class="mb-6"
          title="Ваш логин"
          placeholder="E-mail"
          icon="user"
          type="email"
          :required="true"
        />
        <v-input
          id="password"
          v-model="password"
          class="mb-12"
          title="Ваш пароль"
          placeholder="Введите пароль"
          icon="password"
          type="password"
          :required="true"
        />
        <div class="flex flex-row items-center justify-start">
          <button class="rounded-md bg-cyan text-white font-bold py-7">
            Войти
          </button>
          <span
            class="remove ml-14 pb-2 cursor-pointer font-bold text-gray-300 hover:text-red border-b border-gray-300 hover:border-red"
          >
            Сбросить пароль
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  layout: "sign",
  data() {
    return {
      login: "",
      password: ""
    }
  }
}
</script>

<style lang="scss">
.sign {
  & > .content {
    max-width: 822px;
    padding: 42px 0 71px;
    & > div {
      padding-left: 70px;
      padding-right: 93px;
      &:first-child {
        border-bottom: 1px solid #00000010;
      }
    }
  }
}
button {
  min-width: 210px;
}
.remove {
  border-bottom: 1px dashed #9a9a9a50;
  &:hover {
    border-color: #d42d11;
  }
}
</style>
