<template>
  <label class="flex w-full flex-col items-start mt-3">
    <div class="input w-full flex flex-row items-center justify-start relative">
      <select
        v-model="data"
        class="text-dark w-full py-3 px-6 leading-6 rounded-md border border-black border-opacity-10"
      >
        <option v-for="(child, i) in childs" :key="i" :value="child">{{
          child
        }}</option>
      </select>
    </div>
  </label>
</template>

<script>
export default {
  props: {
    placeholder: {
      type: String,
      default: ""
    },
    id: {
      type: String,
      default: ""
    },
    required: {
      type: Boolean,
      default: false
    },
    value: {
      type: [String, Number, Object],
      default: ""
    },
    childs: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      data: this.value
    }
  },
  watch: {
    data(newData) {
      this.$emit("input", newData)
    },
    value(newData) {
      if (this.data !== newData) this.data = newData
    }
  }
}
</script>

<style lang="scss" scoped>
.icon {
  left: 32px;
}
</style>
