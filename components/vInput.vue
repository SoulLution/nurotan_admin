<template>
  <label class="flex w-full flex-col items-start">
    <span class="text-dark font-bold pb-6">{{ title }}</span>
    <div class="input w-full flex flex-row items-center justify-start relative">
      <div v-if="icon" class="icon absolute">
        <svg
          v-if="icon === 'user'"
          width="27"
          height="27"
          viewBox="0 0 27 27"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M19.0646 14.1059C20.6561 12.6164 21.6581 10.5042 21.6581 8.15729C21.6581 3.65954 17.9985 0 13.5008 0C9.00305 0 5.34351 3.65954 5.34351 8.15729C5.34351 10.5042 6.34544 12.616 7.93658 14.1059C5.48175 16.2178 2.14648 19.116 2.14648 25.8049V27H24.8539V25.8049C24.8543 19.1164 21.5194 16.2178 19.0646 14.1059ZM7.7338 8.15769C7.7338 4.97779 10.3209 2.3907 13.5008 2.3907C16.6803 2.3907 19.2678 4.97779 19.2678 8.15769C19.2678 11.3376 16.6807 13.9251 13.5008 13.9251C10.3209 13.9247 7.7338 11.3376 7.7338 8.15769ZM4.57941 24.6097C4.92799 19.8462 7.36211 17.7523 9.52892 15.8887C9.59186 15.8341 9.65441 15.7807 9.71695 15.727C10.9037 16.2357 12.1961 16.5074 13.51 16.5174C14.8083 16.5074 16.0975 16.2357 17.2842 15.727C17.346 15.7807 17.4089 15.8345 17.4723 15.8887C19.6387 17.7523 22.0732 19.8462 22.4218 24.6097H4.57941Z"
            fill="#CDCDCD"
          />
        </svg>
        <svg
          v-else-if="icon === 'password'"
          width="23"
          height="23"
          viewBox="0 0 23 23"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M17.7431 8.40653H17.5313V6.03096C17.5316 2.70545 14.8265 0 11.501 0C8.17549 0 5.47004 2.70545 5.47004 6.03096V8.40653H5.25785C3.36042 8.40653 1.81641 9.95054 1.81641 11.8483V19.5582C1.81641 21.456 3.36042 23 5.25785 23H17.7435C19.6409 23 21.1849 21.456 21.1849 19.5582V11.8483C21.1846 9.95054 19.6405 8.40653 17.7431 8.40653ZM7.57791 6.03096C7.57791 3.86794 9.33728 2.10787 11.501 2.10787C13.664 2.10787 15.4237 3.86759 15.4237 6.03096V8.40653H7.57791V6.03096ZM19.0767 19.5586C19.0767 20.2942 18.4784 20.8925 17.7431 20.8925H5.25785C4.52256 20.8925 3.92427 20.2942 3.92427 19.5586V11.8483C3.92427 11.1127 4.52256 10.5144 5.25785 10.5144H17.7435C18.4788 10.5144 19.077 11.1127 19.077 11.8483L19.0767 19.5586Z"
            fill="#CDCDCD"
          />
          <path
            d="M11.5005 13.0557C10.3338 13.0557 9.3877 14.0014 9.3877 15.1685C9.3877 15.9508 9.81419 16.6324 10.4465 16.9977V19.3466H12.5544V16.9977C13.1868 16.6324 13.6133 15.9508 13.6133 15.1685C13.6133 14.0014 12.6672 13.0557 11.5005 13.0557Z"
            fill="#CDCDCD"
          />
        </svg>
      </div>
      <input
        :id="id"
        v-model="data"
        v-mask="mask"
        class="text-dark w-full py-6 px-8 leading-6 rounded-md border border-black border-opacity-10"
        :class="{ 'pl-24': icon }"
        :type="type"
        :required="required"
        :placeholder="placeholder"
      />
    </div>
  </label>
</template>

<script>
export default {
  props: {
    title: {
      type: String,
      default: ""
    },
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
      type: [String, Number],
      default: ""
    },
    mask: {
      type: String,
      default: ""
    },
    type: {
      type: String,
      default: "text"
    },
    icon: {
      type: String,
      default: ""
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
