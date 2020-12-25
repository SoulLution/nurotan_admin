<template>
  <transition name="fade-bottom-popup">
    <div
      v-if="popup"
      :class="{ active: show }"
      class="special-bottom flex flex-col rounded-t-30 bg-white fixed bottom-0 left-0 w-full"
    >
      <div class="flex flex-row justify-between py-4 px-8 border-b">
        <h2 class="text-cyan font-bold">{{ title }}</h2>
        <close class="special-close" :bottom="!show" @click="show = !show" />
      </div>
      <div class="flex flex-row flex-wrap w-full pt-4 pb-8 px-8">
        <div class="w-1/4 mt-3 pr-7">
          <v-button
            class="w-full mt-3 justify-center"
            style="height: 50px"
            :title="button"
            @click="$emit('close', true)"
          />
        </div>
        <div class="w-1/4 mt-3 pr-7">
          <button
            class="flex flex-row w-full mt-3 justify-center items-center py-3 px-4 rounded-5 text-cyan fill-current bg-gray-200 hover:text-dark border border-gray-200 transition duration-150 hover:border-d_blue hover:bg-white"
            @click="$emit('close', false)"
          >
            Сбросить
          </button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
export default {
  props: {
    popup: {
      type: Boolean,
      default: false
    },
    title: {
      type: String,
      default: ""
    },
    button: {
      type: String,
      default: ""
    }
  },
  data() {
    return {
      show: true
    }
  }
}
</script>

<style lang="scss" scoped>
.special-bottom {
  transition: 0.3s;
  transform: translateY(100%);
  &.active {
    transform: translateY(0);
    & .special-close {
      transform: translateY(0);
    }
  }
  & .special-close {
    transform: translateY(-47px) scale(1, -1);
  }
}
.special-close {
  transition: 0.3s;
}
.border-b {
  border-color: #d7e2f1;
}
.left-0 {
  max-width: 95%;
  left: 2.5%;
  box-shadow: 0px -4px 16px rgba(0, 0, 0, 0.0973558);
}
.w1\/4 {
  padding-right: 30px;
  &:nth-child(2n) {
    margin-top: 42px;
  }
}
</style>
