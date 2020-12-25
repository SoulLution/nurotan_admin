<template>
  <svg
    class="border border-black border-opacity-10 rounded-5 ml-3 bg-transparent cursor-pointer fill-current hover:bg-red hover:text-white"
    width="32"
    height="32"
    viewBox="0 0 32 32"
    xmlns="http://www.w3.org/2000/svg"
    @click="$emit('click', true)"
  >
    <path
      fill-rule="evenodd"
      clip-rule="evenodd"
      d="M12.6686 22.6663C11.9333 22.6663 11.3353 22.0683 11.3353 21.333V13.333H10.002V11.9997H12.002H12.6686V10.6663C12.6686 9.93101 13.2666 9.33301 14.002 9.33301H18.002C18.7373 9.33301 19.3353 9.93101 19.3353 10.6663V11.9997H20.002H22.002V13.333H20.6686V21.333C20.6686 22.0683 20.0706 22.6663 19.3353 22.6663H12.6686ZM18.002 10.6663H14.002V11.9997H18.002V10.6663ZM13.3353 13.333H18.6686H19.3353L19.336 21.333H12.6686V13.333H13.3353ZM14.002 14.6663H15.3353V19.9997H14.002V14.6663ZM16.6686 14.6663H18.002V19.9997H16.6686V14.6663Z"
    />
  </svg>
</template>

<style lang="scss" scoped>
svg {
  max-width: 32px;
  max-height: 32px;
  min-width: 32px;
  min-height: 32px;
  transition: 0.1s;
}
</style>
