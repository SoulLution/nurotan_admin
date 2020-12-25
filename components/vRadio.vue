<template>
  <label
    class="radio cursor-pointer flex flex-row items-start"
    :title="title.replace(/<\/?[^>]+(>|$)/g, '')"
  >
    <div
      style="min-height: 34px; min-width: 40px; max-height: 34px; max-width: 40px; overflow: visible"
    >
      <input type="radio" :checked="checked" @click="changeData" />
    </div>
    <span class="opacity-60 pt-2 truncate" v-html="title"></span>
  </label>
</template>

<script>
export default {
  props: {
    title: {
      type: String,
      default: ""
    },
    value: {
      type: Boolean,
      default: false
    },
    checked: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    changeData(e) {
      if (e) this.$emit("change", this.value)
    }
  }
}
</script>

<style lang="scss" scoped>
input {
  height: 0;
  width: 0;
  overflow: visible;
  position: relative;
  &:before,
  &::after {
    content: "";
    position: absolute;
    top: 0;
    max-width: 29px;
    max-height: 29px;
    min-width: 29px;
    min-height: 29px;
    border-radius: 50%;
    transform: translateY(-40%);
    cursor: pointer;
  }
  &:after {
    opacity: 0.2;
    border: 1px solid #0066ff;
    background-image: url("/radio.svg");
    background-repeat: no-repeat;
    background-position: 50%;
  }
  &::before {
    background-color: #ffffff;
    box-shadow: inset 0px 0px 0px 0px #f9db3d;
    transition: 0.3s;
  }
  &:hover {
    &:after {
      opacity: 0.5;
      border-color: #f9db3d;
    }
  }
  &:checked {
    &:after {
      opacity: 1;
      border-color: #f9db3d;
      box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.08);
    }
    &::before {
      box-shadow: inset 0px 0px 0px 15px #f9db3d;
    }
  }
}
</style>

<style lang="scss">
.radio {
  & * {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
}
</style>
