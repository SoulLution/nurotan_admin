<template>
  <transition name="fade-bottom-popup">
    <div
      v-if="popup"
      class="flex manager-popup flex-col rounded-t-30 bg-white fixed bottom-0 left-0 w-full"
    >
      <div class="flex flex-row justify-between py-4 px-8 border-b">
        <h2 class="text-cyan font-bold">{{ title }}</h2>
        <close @click="$emit('close', false)" />
      </div>
      <div class="flex flex-row flex-wrap w-full pt-4 pb-8 px-8">
        <div class="w-1/4 pr-7 mt-3">
          <span class="font-bold opacity-0">Выбрать мэнеджера</span>
          <multiselect
            v-model="manager"
            class="rounded-5 p-3 bg-opacity-25 py-2 cursor-pointer relative z-10"
            style="min-height:50px; width: 200px; display: inline-table"
            :options="list"
            :searchable="true"
            :close-on-select="false"
            select-label=""
            label="full_name"
            selected-label=""
            deselect-label=""
            placeholder="Выберите Мэнеджера"
            :taggable="true"
          />
        </div>
        <div class="w-1/4 mt-3 pr-7">
          <span class="font-bold opacity-0">Добавить</span>
          <v-button
            class="w-full mt-3 justify-center"
            style="height: 50px"
            :title="button"
            @click="$emit('close', manager)"
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
    }
  },
  data() {
    return {
      manager: "",
      list: []
    }
  },
  created() {
    let data = {
      find: ""
    }
    this.$axios
      .post(`/searchUser/123123123/`, this.changeData(data))
      .then(res => {
        console.log(res.data)
        this.list = res.data
      })
  },
  methods: {
    changeData(data) {
      let formData = new FormData()
      Object.keys(data).forEach(key => {
        formData.append(key, data[key])
      })
      return formData
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
<style lang="scss">
.manager-popup {
  & .multiselect__tags {
    background: transparent;
    padding-top: 0.75rem;
    padding-bottom: 0.5rem;
  }
}
</style>
