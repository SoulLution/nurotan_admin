<template>
  <transition-group name="confirm-popup">
    <div
      v-if="popup"
      key="bg"
      class="bg z-40"
      @click="$emit('close', false)"
    ></div>
    <div
      v-if="popup"
      key="content"
      class="flex flex-col rounded-t-30 bg-white fixed  w-full z-50 overflow-y-auto"
    >
      <div class="flex flex-row justify-center py-4 px-8">
        <h2 class="text-lg sm:text-4xl sm:mb-22">Проверка обращения</h2>
      </div>
      <div class="flex flex-row flex-wrap w-full pt-4 pb-8 px-8">
        <template v-for="answer in answers">
          <div :key="answer.id" class="w-full sm:w-1/3 sm:pr-7">
            <div class="flex flex-col">
              <span class="sm:font-bold text-sm sm:text-base">{{
                answer.title
              }}</span>
              <span
                class="rounded-5 border border-black border-opacity-25 mt-2 mb-4 sm:mt-6 sm:mb-7 p-4"
                v-html="answer.value"
              >
              </span>
            </div>
          </div>
        </template>
        <div class="w-full sm:w-1/3 sm:pr-7">
          <div class="flex flex-col">
            <span class="sm:font-bold text-sm sm:text-base">
              Получатель
            </span>
            <multiselect
              v-model="cur_fild"
              class="rounded-5 bg-opacity-25 cursor-pointer relative z-10 w-full mt-2 mb-4 sm:mt-6 sm:mb-7"
              style="min-height:50px; display: block"
              :options="fields"
              :searchable="true"
              :close-on-select="true"
              select-label=""
              label="korrespondent"
              selected-label=""
              deselect-label=""
              placeholder="Выберите Получателя"
              :taggable="true"
            />
          </div>
        </div>
      </div>
      <div class="flex flex-row py-1 pb-4 w-full justify-center items-center">
        <v-button
          class="justify-center mr-1 sm:mr-6 px-6"
          style="height: 50px"
          title="Одобрить"
          :disabled="!cur_fild.id"
          @click="$emit('close', cur_fild)"
        />
        <span
          class="flex justify-center items-center rounded-5 sm:hidden cursor-pointer text-lg text-red ml-1 px-6 hover:text-gray-700 border border-red hover:border-gray-700"
          style="height: 50px"
          @click="$emit('close', -1)"
        >
          Отклонить
        </span>
        <span
          class="hidden sm:flex justify-center items-center cursor-pointer text-lg text-red ml-6 hover:text-gray-700 border-b border-transparent border-dashed hover:border-gray-700"
          @click="$emit('close', -1)"
        >
          Отклонить
        </span>
      </div>
    </div>
  </transition-group>
</template>

<script>
export default {
  props: {
    popup: {
      type: Boolean,
      default: false
    },
    answers: {
      type: Object,
      default: () => {}
    },
    field: {
      type: Object,
      default: () => {}
    },
    fields: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      cur_fild: this.field
    }
  },
  watch: {
    field(newData) {
      this.cur_fild = newData
    }
  },
  mounted() {
    console.log(this.answers)
  }
}
</script>

<style lang="scss" scoped>
.bg {
  width: 100vw;
  height: 100vh;
  position: fixed;
  left: 0;
  top: 0;
  background: #00000016;
}
.fixed {
  width: 90%;
  height: 80%;
  left: 5%;
  top: 10%;
}
@media (max-width: 639px) {
  .bg {
    background: #ffffffe0;
  }
  .fixed {
    height: 50%;
    width: 100%;
    left: 0;
    top: unset;
    bottom: 0;
    box-shadow: 0px -25px 55px rgba(0, 0, 0, 0.05);
  }
}
</style>
