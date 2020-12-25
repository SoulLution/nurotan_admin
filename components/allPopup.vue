<template>
  <div
    class="popup fixed w-full h-full top-0 left-0 flex justify-center items-center z-50"
  >
    <div
      class="popup-bg bg-black bg-opacity-10 w-full h-full absolute left-0 top-0 z-0"
      @click="$emit('close', false)"
    ></div>
    <div
      class="popup-content pt-24 relative z-10 bg-white rounded-20 flex flex-col justify-start items-start overflow-y-scroll"
    >
      <h5 class="font-normal px-24 text-xl mb-12 text-d_blue">
        Выбрать Сообщение
      </h5>

      <div class="flex flex-row px-24 flex-wrap w-full">
        <template v-for="(branch, i) in list">
          <branch
            v-if="branch.answers_type == 2 || branch.answers.length - 1"
            :key="branch.id"
            :branch="branch"
            :i="i"
            :with-out="true"
            :active="branch.id === cur_branch"
            class="branch bsadow cursor-pointer"
            @click="e => changeBranch(branch.id)"
          />
        </template>
      </div>
      <div
        class="sticky bottom-0 border-t border-black border-opacity-10 py-4 px-24 flex flex-row justify-between items-center mt-10 w-full bg-white"
      >
        <div class="flex flex-row">
          <button
            class="flex flex-row items-center py-3 px-4 mr-4 rounded-5 text-white bg-gray-500 hover:text-dark border border-gray-500 transition duration-150 hover:border-d_blue hover:bg-white"
            @click="$emit('close', false)"
          >
            Отменить
          </button>
          <v-button
            v-if="cur_branch"
            title="Выбрать"
            @click="sendMessage(list.find(x => x.id === cur_branch))"
          />
        </div>
        <v-radio
          title="Сохранить структуры ответов"
          :checked="save_structure"
          @change="save_structure = !save_structure"
        />
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
  data() {
    return {
      save_structure: false,
      cur_branch: 0
    }
  },
  methods: {
    changeBranch(id) {
      this.cur_branch = id
    },
    sendMessage(item) {
      this.$emit("close", {
        branch: item ? item : "",
        save_structure: this.save_structure
      })
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
.branch {
  height: auto;
}
</style>
