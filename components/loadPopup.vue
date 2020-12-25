<template>
  <transition name="confirm-popup">
    <div
      v-if="popup"
      class="popup fixed w-full h-full top-0 left-0 flex justify-center items-center z-50"
    >
      <div
        class="popup-bg bg-black bg-opacity-10 w-full h-full absolute left-0 top-0 z-0"
      ></div>
      <transition name="confirm-popup">
        <div
          v-if="popup"
          class="popup-content px-24 py-15 pt-24 relative z-10 flex flex-col justify-start items-start"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            xmlns:xlink="http://www.w3.org/1999/xlink"
            style="margin: auto; background: rgba(255, 255, 255, 0); display: block;"
            width="200px"
            height="200px"
            viewBox="0 0 100 100"
            preserveAspectRatio="xMidYMid"
          >
            <circle
              cx="50"
              cy="50"
              r="36"
              stroke-width="7"
              stroke="#008fa0"
              stroke-dasharray="56.548667764616276 56.548667764616276"
              fill="none"
              stroke-linecap="round"
            >
              <animateTransform
                attributeName="transform"
                type="rotate"
                repeatCount="indefinite"
                dur="1.3513513513513513s"
                keyTimes="0;1"
                values="0 50 50;360 50 50"
              />
            </circle>
          </svg>
        </div>
      </transition>
    </div>
  </transition>
</template>

<script>
export default {
  props: {
    popup: {
      type: Boolean,
      default: false
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
</style>
