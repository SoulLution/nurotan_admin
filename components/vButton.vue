<template>
  <button
    class="flex flex-row items-center py-3 px-4 rounded-5 text-white fill-current bg-cyan hover:text-dark border border-cyan transition duration-150 hover:border-d_blue hover:bg-white"
    :disabled="disabled"
    @click="$emit('click', true)"
  >
    <svg
      v-if="plus"
      width="16"
      height="16"
      viewBox="0 0 16 16"
      class="mr-2"
      xmlns="http://www.w3.org/2000/svg"
    >
      <g clip-path="url(#clip0)">
        <path
          d="M8.46532 8.46696H14.5827C14.9626 8.46712 15.2706 8.15905 15.2705 7.77915C15.2705 7.39909 14.9627 7.09134 14.5827 7.09134L8.46532 7.09134L8.46516 0.973836C8.46516 0.593772 8.15741 0.286024 7.77734 0.286024C7.39744 0.285862 7.08937 0.593935 7.08953 0.973836L7.08969 7.09134L0.972191 7.09118C0.592289 7.09102 0.284217 7.39909 0.28438 7.77899C0.284541 7.96886 0.361559 8.14089 0.485923 8.26526C0.610287 8.38962 0.782321 8.46664 0.972353 8.46664L7.08986 8.4668L7.08986 14.5841C7.08986 14.7742 7.16687 14.9462 7.29124 15.0706C7.4156 15.1949 7.58764 15.272 7.77767 15.272C8.15757 15.2721 8.46564 14.964 8.46548 14.5841L8.46532 8.46696Z"
        />
      </g>
      <defs>
        <clipPath id="clip0">
          <rect
            width="11"
            height="11"
            transform="translate(7.77832) rotate(45)"
          />
        </clipPath>
      </defs>
    </svg>
    {{ title }}
  </button>
</template>

<script>
export default {
  props: {
    title: {
      type: String,
      default: ""
    },
    plus: {
      type: Boolean,
      default: false
    },
    disabled: {
      type: Boolean,
      default: false
    }
  }
}
</script>

<style lang="scss" scoped>
button {
  height: max-content;
  &:disabled {
    background-color: rgba(226, 232, 240, 1);
    border-color: rgba(226, 232, 240, 1);
    color: #8e8e8e;
  }
}
</style>
