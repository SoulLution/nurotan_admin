<template>
  <svg
    class="cursor-pointer"
    width="32"
    height="32"
    viewBox="0 0 32 32"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    @click="$emit('click', true)"
  >
    <rect
      x="0.5"
      y="0.5"
      width="31"
      height="31"
      rx="3.5"
      fill="white"
      stroke="#D3DFF0"
    />
    <line
      v-if="bottom"
      stroke="#008FA0"
      stroke-width="2"
      y2="22.22066"
      x2="16.09667"
      y1="10.6365"
      x1="4.51251"
    />
    <line
      v-if="bottom"
      stroke="#008FA0"
      stroke-width="2"
      y2="22.30034"
      x2="15.43733"
      y1="10.71618"
      x1="26.52644"
    />
    <path
      v-if="!bottom"
      fill-rule="evenodd"
      clip-rule="evenodd"
      d="M20.862 10.1953L16 15.0573L11.138 10.1953L10.1953 11.138L15.0573 16L10.1953 20.862L11.138 21.8046L16 16.9426L20.862 21.8046L21.8046 20.862L16.9426 16L21.8046 11.138L20.862 10.1953Z"
      fill="#212121"
    />
  </svg>
</template>
<script>
export default {
  props: {
    bottom: {
      type: Boolean,
      default: false
    }
  }
}
</script>
