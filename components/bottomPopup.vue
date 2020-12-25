<template>
  <transition name="fade-bottom-popup">
    <div
      v-if="popup"
      class="flex flex-col rounded-t-30 bg-white fixed bottom-0 left-0 w-full"
    >
      <div class="flex flex-row justify-between py-4 px-8 border-b">
        <h2 class="text-cyan font-bold">{{ title }}</h2>
        <close @click="$emit('close', false)" />
      </div>
      <div class="flex flex-row flex-wrap w-full pt-4 pb-8 px-8">
        <template v-for="(item, i) in childs">
          <div :key="i" class="w-1/4 pr-7" :class="{ 'mt-3': i > 3 }">
            <div v-if="item.component" class="flex flex-col">
              <span class="font-bold">{{ item.title }}</span>
              <component
                :is="item.component"
                v-model="item.value"
                :mask="item.type === 'phone' ? '+7 (###) ### - ####' : ''"
                :placeholder="item.placeholder"
                :childs="item.childs"
                :type="item.type"
              />
            </div>
          </div>
        </template>
        <div class="w-1/4 mt-3 pr-7">
          <span class="font-bold opacity-0">Добавить</span>
          <v-button
            class="w-full mt-3 justify-center"
            style="height: 50px"
            :title="button"
            @click="$emit('close', true)"
          />
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
    },
    childs: {
      type: Array,
      default: () => []
    }
  }
}
</script>

<style lang="scss" scoped>
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
