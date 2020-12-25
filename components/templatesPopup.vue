<template>
  <div
    class="popup fixed w-full h-full top-0 left-0 flex justify-center items-center z-50"
  >
    <div
      class="popup-bg bg-black bg-opacity-10 w-full h-full absolute left-0 top-0 z-0"
      @click="$emit('close', false)"
    ></div>
    <div
      class="popup-content px-24 py-15 pt-24 relative z-10 bg-white rounded-20 flex flex-col justify-start items-start"
    >
      <h5 class="font-normal mt-12 text-d_blue">Выбрать шаблон</h5>

      <div class="flex flex-col w-full mt-9 overflow-auto">
        <template v-for="item in list">
          <div
            :key="item.id"
            class="bsadow w-full px-4 py-6 rounded-5 mb-4 cursor-pointer text-lg font-semibold"
            @click="sendMessage(item)"
          >
            <span v-html="item.title"></span>
          </div>
        </template>
      </div>
      <div class="flex flex-row justify-start items-center mt-10">
        <button
          class="flex flex-row items-center py-3 px-4 rounded-5 text-white bg-gray-500 hover:text-dark border border-gray-500 transition duration-150 hover:border-d_blue hover:bg-white"
          @click="sendMessage()"
        >
          Отменить
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    list: {
      type: Array,
      default: () => []
    }
  },
  methods: {
    sendMessage(item) {
      this.$emit("close", item ? item.to_branch : "")
    }
  }
}
</script>

<style lang="scss" scoped>
.popup-content {
  width: 100%;
  height: 100%;
  max-width: 90%;
  max-height: 95%;
}
.bsadow {
  box-shadow: 0 0 5px 0 #00000015;
}
</style>
