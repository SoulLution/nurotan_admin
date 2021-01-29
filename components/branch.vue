<template>
  <div
    class="inline-flex w-1/2 h-full mb-10"
    :class="i % 2 === 0 ? 'pr-5' : 'pl-5'"
    @click="$emit('click', true)"
  >
    <div
      class="flex flex-col bg-white rounded-30 px-10 py-8 w-full"
      :class="{ 'branch-static': withOut, active }"
    >
      <div class="flex flex-row justify-between">
        <h3
          class="flex flex-row items-start text-d_blue text-lg font-bold pr-2"
          :class="withOut ? 'w-full' : 'w-3/5'"
        >
          <span class="branch-title truncate" v-html="branch.title"></span>
          <pencil
            v-if="!withOut"
            class=" text-svg_default hover:text-d_blue hover:border-d_blue"
            style="margin-top: 0.375rem"
            @click="$emit('open-title', true)"
          />
        </h3>
        <v-button
          v-if="!withOut"
          title="Добавить"
          :plus="true"
          @click="$emit('add-answer', true)"
        />
      </div>
      <div v-if="!withOut" class="flex flex-row mt-2">
        <v-radio
          v-if="is_request === undefined"
          class="w-1/2"
          title="Вопрос для заявки"
          style="min-height: 2.125rem; max-height: 2.125rem;"
          :checked="is_request !== undefined"
          @change="is_request = ''"
        />
        <input
          v-if="is_request !== undefined"
          v-model="is_request"
          placeholder="Название поля в заявке"
          class="mr-2 rounded-5 border border-black border-opacity-10 w-3/5 py-2 px-4"
          type="text"
        />
        <close
          v-if="is_request !== undefined"
          @click="is_request = undefined"
        />
      </div>
      <div class="flex flex-row w-full mt-8 text-sm justify-between">
        <div
          v-for="(type, j) in types"
          :key="j"
          class="type rounded-full py-3 px-2 text-center w-full whitespace-no-wrap cursor-pointer"
          :class="branch.answers_type == j ? 'active text-d_blue' : 'text-C4'"
          @click="$emit('change-type', j)"
        >
          {{ type }}
        </div>
      </div>
      <div
        v-if="branch.answers_type < 2"
        class="flex flex-col mt-2 branch-content"
      >
        <v-radio
          v-if="!withOut"
          class="w-1/2"
          title="Единый ответ"
          style="min-height: 2.125rem; max-height: 2.125rem;"
          :checked="branch.for_all_active"
          @change="$emit('change-for-all', !branch.for_all_active)"
        />
        <template v-for="(answer, j) in branch.answers">
          <div
            v-if="answer.content"
            :key="answer.id"
            class="flex flex-row justify-between items-center overflow-hidden"
            style="min-height: 2.125rem; max-height: 2.125rem;"
          >
            <div class="flex flex-row w-1-2 items-center truncate">
              <div
                v-if="branch.answers.length - 1"
                class="arrows flex flex-col h-full pr-2"
              >
                <img
                  v-if="j"
                  class="first mb-1 cursor-pointer"
                  src="/down.png"
                  @click="$emit('change-position', { index: j, value: -1 })"
                />
                <img
                  v-if="j !== branch.answers.length - 2"
                  class="mt-1 cursor-pointer"
                  src="/down.png"
                  @click="$emit('change-position', { index: j, value: 1 })"
                />
              </div>
              <v-radio
                v-if="!withOut"
                class="w-full"
                :title="answer.content"
                :checked="branch.current === answer.id"
                @change="$emit('change-current', answer.id)"
              />
              <span v-else v-html="answer.content"></span>
            </div>
            <div v-if="!withOut" class="flex flex-row">
              <pencil style="margin-left: 0" @click="$emit('open-answer', j)" />
              <delete
                class="text-red border-red"
                style="margin: 0 1rem"
                @click="$emit('remove-answer', j)"
              />
            </div>
          </div>
        </template>
      </div>
      <div v-else>
        <div class="w-full mt-4 h-6 px-2 border border-C4 text-C4">
          Произвольный ввод
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    branch: {
      type: Object,
      default: () => {}
    },
    i: {
      type: Number,
      default: 0
    },
    withOut: {
      type: Boolean,
      default: false
    },
    active: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      types: ["Кнопки под сообщением", "Меню", "Текстовый ввод"],
      is_request: JSON.stringify(this.branch.is_request)
    }
  },
  watch: {
    is_request(newString) {
      this.$emit("change-is-request", newString)
    }
  }
}
</script>

<style lang="scss" scoped>
.branch-title {
  & * {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
}
.branch-content {
  height: 250px;
  overflow: hidden scroll;
}
.branch-static {
  transition: 0.3s;
  box-shadow: 0 0 15px 0 #00000015;
  &.active {
    transition: 0s;
    box-shadow: inset 0 0 15px 0 #f9db3d15, 0 0 15px 0 #008fa0 !important;
  }
  &:hover {
    box-shadow: inset 0 0 15px 0 #00000015, 0 0 15px 0 #00000015;
  }
}
.arrows {
  max-width: 19px;
  min-width: 19px;
  & > img:last-child {
    transition: 0.3s;
  }
  & > .first {
    transform: scale(-1, -1);
  }
}
</style>
