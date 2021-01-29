<template>
  <div class="sm:pt-4 rounded-t-30 sm:mt-4">
    <div class="px-0 sm:px-70px flex flex-col">
      <h1 class="hidden sm:flex page-title text-cyan text-2xl font-bold">
        Активные диалоги
      </h1>
      <div class="flex flex-row sm:py-10">
        <div class="hidden sm:flex flex-col pr-3">
          <template v-for="(list, i) in chats">
            <router-link
              :key="list.id"
              :to="'/chat?user_id=' + list.id"
              class="chater bg-white pb-8 rounded-30 flex flex-row justify-between mb-7 pl-11 pr-7 py-6 mt-3 cursor-pointer"
            >
              <div class="flex flex-row justify-between">
                <div class="ava">
                  <img src="user.svg" />
                  <div class="absolute">
                    <svg
                      width="27"
                      height="27"
                      viewBox="0 0 27 27"
                      fill="none"
                      xmlns="http://www.w3.org/2000/svg"
                    >
                      <path
                        d="M19.0646 14.1059C20.6561 12.6164 21.6581 10.5042 21.6581 8.15729C21.6581 3.65954 17.9985 0 13.5008 0C9.00305 0 5.34351 3.65954 5.34351 8.15729C5.34351 10.5042 6.34544 12.616 7.93658 14.1059C5.48175 16.2178 2.14648 19.116 2.14648 25.8049V27H24.8539V25.8049C24.8543 19.1164 21.5194 16.2178 19.0646 14.1059ZM7.7338 8.15769C7.7338 4.97779 10.3209 2.3907 13.5008 2.3907C16.6803 2.3907 19.2678 4.97779 19.2678 8.15769C19.2678 11.3376 16.6807 13.9251 13.5008 13.9251C10.3209 13.9247 7.7338 11.3376 7.7338 8.15769ZM4.57941 24.6097C4.92799 19.8462 7.36211 17.7523 9.52892 15.8887C9.59186 15.8341 9.65441 15.7807 9.71695 15.727C10.9037 16.2357 12.1961 16.5074 13.51 16.5174C14.8083 16.5074 16.0975 16.2357 17.2842 15.727C17.346 15.7807 17.4089 15.8345 17.4723 15.8887C19.6387 17.7523 22.0732 19.8462 22.4218 24.6097H4.57941Z"
                        fill="black"
                      />
                    </svg>
                  </div>
                </div>
                <div class="flex flex-col justify-start items-start mt-2">
                  <h4 class="font-bold mb-1">{{ list.name }}</h4>
                  <span
                    class="text-sm text-opacity-50 text-black"
                    v-html="list.messages[list.messages.length - 1].content"
                  ></span>
                </div>
              </div>
              <div class="flex flex-col justify-between items-start">
                <span
                  class="status text-xs"
                  :class="{ active: i === current_chat }"
                >
                  {{
                    $moment(
                      list.messages[list.messages.length - 1].date
                    ).format("HH:mm")
                  }}
                </span>
                <img :src="list.from + '.svg'" />
              </div>
            </router-link>
          </template>
        </div>
        <div class="sm:ml-4 w-full sm:w-3/4">
          <div class="flex flex-col sm:bg-white sm:rounded-30">
            <div
              class="flex flex-row px-4 sm:px-12 bg-white sm:bg-transparent py-6 justify-between border-b border-black border-opacity-10"
            >
              <div v-if="chats.length" class="flex flex-col">
                <h4 class="font-bold mb-1">{{ chats[current_chat].name }}</h4>
                <div
                  class="flex flex-row text-black text-opacity-50 text-sm mt-3"
                >
                  <img
                    :src="chats[current_chat].from + '.svg'"
                    class="mr-3"
                    style="width: 22px"
                  />
                  <span>
                    {{ chats[current_chat].phone }}
                  </span>
                </div>
              </div>
              <div
                v-click-outside="() => (show_burger = false)"
                class="flex sm:hidden relative"
                @click="show_burger = !show_burger"
              >
                <div class="burger px-4 flex flex-col">
                  <div></div>
                  <div></div>
                  <div></div>
                </div>
                <div
                  v-if="show_burger"
                  class="burger-show bg-white absolute flex flex-col z-10"
                >
                  <button
                    class="py-4 px-3 text-left truncate text-xs border-C4 border-b"
                    @click="manager_popup = true"
                  >
                    Сменить ответственного
                  </button>
                  <button
                    class="py-4 px-3 text-left truncate text-xs border-C4 border-b"
                    @click="openChangeBranch()"
                  >
                    Переместить на этап
                  </button>
                </div>
              </div>
              <div class="hidden sm:flex flex-row mt-2">
                <button
                  class="py-3 ml-6 px-4 truncate text-cyan border-cyan border rounded-5"
                  @click="manager_popup = true"
                >
                  Сменить ответственного
                </button>
                <button
                  class="py-3 ml-6 px-4 truncate text-cyan border-cyan border rounded-5"
                  @click="openChangeBranch()"
                >
                  Переместить на этап
                </button>
                <!-- <button
                  class="py-3 ml-6 px-4 truncate text-red border-red border rounded-5"
                >
                  Отключить бота
                </button> -->
              </div>
            </div>
            <div
              ref="chat"
              class="chat overflow-x-hidden overflow-y-scroll px-4 sm:px-8 flex flex-col"
            >
              <template v-for="message in chat">
                <div
                  :key="message.id"
                  class="message-block w-full flex py-5"
                  :class="{
                    'left flex-row': message.from === 'client',
                    'right flex-row-reverse': message.from !== 'client'
                  }"
                >
                  <div class="ava hidden sm:flex">
                    <img v-if="message.from === 'client'" src="user.svg" />
                  </div>
                  <div
                    class="message flex flex-col relative"
                    :class="{ 'items-end': message.from !== 'client' }"
                  >
                    <span v-if="!isNaN(message.from)" class="text-cyan mb-4">{{
                      message.user.name
                    }}</span>
                    <span v-html="message.content"></span>
                    <div class="absolute">
                      {{ checkDate(message.date) }}
                    </div>
                  </div>
                </div>
              </template>
            </div>
            <form
              class="sender sm:px-8 flex justify-end items-center relative flex relative"
              @submit.prevent="sendMessage()"
            >
              <textarea
                v-model="form.message"
                type="text"
                placeholder="Введите сообщение ..."
                class="w-full sm:rounded-full border border-black
              border-opacity-10 outline-none mt-4 p-4"
              ></textarea>
              <div class="absolute hidden"><img src="add_file.svg" /></div>
              <div class="absolute" @click="sendMessage()">
                <img src="send.svg" />
              </div>
            </form>
          </div>
        </div>
      </div>
      <bottom-popup
        :popup="popup"
        :childs="popup_content"
        title="Изменить"
        button="Сохранить"
        @close="e => changeBranch(e)"
      />
    </div>
    <bottom-manager-popup
      :popup="manager_popup"
      title="Изменить"
      button="Сохранить"
      @close="e => changeManager(e)"
    />
  </div>
</template>

<script>
import vSelect from "@/components/vSelect"
export default {
  beforeRouteLeave(to, from, next) {
    if (this.inter) clearInterval(this.inter)
    next()
  },
  middleware: "index",
  data() {
    return {
      load: true,
      show_burger: false,
      current_chat: 0,
      current_page: 0,
      form: {
        message: "",
        files: []
      },
      chat: [],
      chats: [],
      inter: null,
      popup: false,
      manager_popup: false,
      popup_content: [
        {
          title: "",
          component: vSelect,
          value: "",
          childs: []
        }
      ],
      save_content: []
    }
  },
  watch: {
    $route: {
      deep: true,
      handler() {
        this.current_page = 0
        this.manager_popup = false
        this.popup = false
        this.chat = []
        this.getChatList()
        this.getClients()
        if (this.inter) clearInterval(this.inter)
      }
    }
  },
  beforeDestroy() {
    if (this.inter) clearInterval(this.inter)
  },
  created() {
    this.getChatList()
    this.getClients()
  },
  methods: {
    changeManager(e) {
      if (e)
        this.$axios.get(
          `/update_changeManager/123123123/${this.$route.query.user_id}/${e.id}/`
        )
      this.manager_popup = false
    },
    changeBranch(e) {
      if (e && this.popup_content[0].value) {
        let data = {
          client_id: this.$route.query.user_id,
          to_branch: this.save_content.find(
            x => x.title === this.popup_content[0].value
          ).branch_id
        }
        this.$axios
          .post("/changeBranch/123123123/", this.changeData(data))
          .then(res => console.log(res))
      }
      this.popup = false
    },
    openChangeBranch() {
      let data = {
        client_id: this.$route.query.user_id
      }
      this.$axios
        .post("/lastBranches/123123123/", this.changeData(data))
        .then(res => {
          this.popup = true
          this.popup_content[0].title = "Выбрать этап"
          this.popup_content[0].value = ""
          this.popup_content[0].childs = JSON.parse(res.data[0].content).map(
            x => x.title
          )
          this.save_content = JSON.parse(res.data[0].content)
        })
    },
    getClients() {
      let data = localStorage.getItem("chats")
        ? JSON.parse(localStorage.getItem("chats"))
        : []

      for (let i = 0; i < data.length - 1; i++)
        if (
          data[i].last.valueOf() <
          new Date().valueOf() + 1000 * 60 * 60 * 6
        ) {
          data.splice(i, 1)
          i--
        }
      this.$axios
        .get(`/Client/12313123/${this.$route.query.user_id}`)
        .then(res => {
          let new_data = res.data.map(x => {
            return {
              ...x,
              messages: JSON.parse(x.messages)
            }
          })
          if (data.findIndex(x => x.id == this.$route.query.user_id) === -1) {
            data.splice(0, 0, new_data[0])
            data[0].last = new Date()
            this.current_chat = 0
          } else {
            this.current_chat = data.findIndex(
              x => x.id == this.$route.query.user_id
            )
            data[data.findIndex(x => x.id == this.$route.query.user_id)] =
              new_data[0]
            data[
              data.findIndex(x => x.id == this.$route.query.user_id)
            ].last = new Date()
          }
          localStorage.setItem("chats", JSON.stringify(data))
          this.chats = data
        })
    },
    checkDate(date) {
      if (
        this.$moment(new Date()).format("DD MM YYYY") !==
        this.$moment(date).format("DD MM YYYY")
      )
        return this.$moment(date).format("DD.MM.YYYY HH:mm")
      else return this.$moment(date).format("HH:mm")
    },
    getChatList() {
      let data = {
        page: this.current_page * 20,
        user_id: this.$route.query.user_id,
        last: 0
      }
      this.load = false
      this.$axios
        .post("/n_messagesList/123123123/", this.changeData(data))
        .then(res => {
          res.data.forEach(x => {
            this.chat.splice(0, 0, x)
          })
          if (!this.current_page)
            this.$nextTick(() => {
              this.$refs["chat"].scrollTo({
                top:
                  this.$refs["chat"].clientHeight +
                  this.$refs["chat"].scrollHeight
              })
              this.$refs["chat"].onscroll = () => {
                if (this.$refs["chat"].scrollTop <= 250 && this.load)
                  this.getChatList()
              }
            })
          if (!this.inter)
            this.inter = setInterval(() => {
              let data = {
                page: 0,
                user_id: this.$route.query.user_id,
                last: this.chat[this.chat.length - 1].id
              }
              this.$axios
                .post("/n_messagesList/123123123/", this.changeData(data))
                .then(res => {
                  res.data.forEach(x => {
                    this.chat.push(x)
                  })
                })
            }, 5000)
          this.current_page++
        })
        .finally(() => (this.load = true))
    },
    sendMessage() {
      let data = {
        message: this.form.message,
        user_id: this.$route.query.user_id,
        from: JSON.parse(localStorage.getItem("auth")).id
      }
      this.$axios
        .post("/sendMessage/123123123/", this.changeData(data))
        .then(() => {
          let data = {
            page: 0,
            user_id: this.$route.query.user_id,
            last: this.chat[this.chat.length - 1].id
          }
          this.$axios
            .post("/n_messagesList/123123123/", this.changeData(data))
            .then(res => {
              res.data.forEach(x => {
                this.chat.push(x)
              })
            })
        })
      this.form = { message: "", files: [] }
    },
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
.chater {
  position: relative;
  &:before {
    content: "";
    display: block;
    position: absolute;
    background-color: #d42d11;
    border-radius: 50px;
    height: calc(100% - 3rem);
    width: 5px;
    margin-left: -1rem;
  }
  & .ava {
    min-width: 66px;
    max-width: 66px;
    min-height: 66px;
    max-height: 66px;
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
    margin-right: 1.15rem;
    & > img {
      width: 40%;
    }
    & > .absolute {
      min-width: 40px;
      max-width: 40px;
      min-height: 40px;
      max-height: 40px;
      right: 0;
      bottom: 0;
      transform: translate(25%, 25%);
      background: #f9db3d;
      border-radius: 50%;
      display: flex;
      justify-content: center;
      align-items: center;
      & > svg {
        width: 40%;
      }
    }
  }
  & .status {
    position: relative;
    display: flex;
    align-items: center;
    &:after {
      content: "";
      position: absolute;
      right: -12px;
      background: #3ae141;
      max-width: 6px;
      max-height: 6px;
      min-width: 6px;
      min-height: 6px;
      transition: 0.3s;
      border-radius: 50%;
      transform: scale(0);
    }
    &.active:after {
      transform: scale(1);
      box-shadow: 0 0 0 3px #3ae14140;
    }
  }
}
.chat {
  height: 60vh;
}
.sender {
  & > textarea {
    resize: none;
    padding-right: 9rem;
    max-height: 5rem;
  }
  & > .absolute {
    cursor: pointer;
    margin-top: 1rem;
    right: 110px;
    &:last-child {
      padding: 1rem;
      right: 45px;
      background: #008fa0;
      border-radius: 50%;
    }
  }
}

.ava {
  min-width: 66px;
  max-width: 66px;
  min-height: 66px;
  max-height: 66px;
  background: #008fa0;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  & > img {
    width: 40%;
  }
}
.message-block {
  &.left {
    & .message {
      max-width: 75%;
      margin-left: 58px;
      background: #f5f5f5;
      border-radius: 20px;
      padding: 18px 25px 27px 37px;
      color: #000000e0;
      font-size: 14px;
      line-height: 19px;
      &:before {
        content: "";
        position: absolute;
        background-image: url("/for_message.svg");
        background-repeat: no-repeat;
        left: 0;
        top: 1.5rem;
        width: 60px;
        height: 39px;
        transform: translateX(-50px);
      }
    }
  }
  &.right {
    & .ava {
      opacity: 0;
      max-width: 0;
      min-width: 0;
    }
    & .message {
      max-width: 75%;
      background: #f5f5f5;
      border-radius: 20px;
      padding: 18px 25px 27px 37px;
    }
  }
  &.system {
    & .ava {
      opacity: 0;
    }
    & .message {
      background: #008fa0;
      border-radius: 20px;
      padding: 23px 47px 31px;
      font-size: 18px;
      line-height: 25px;
      text-align: center;
      color: #ffffff;
      max-width: 370px;
      & > .absolute {
        color: #ffffff;
      }
    }
  }
}
.message {
  min-width: 270px;
  & > span {
    word-break: break-word;
  }
  & > .absolute {
    font-size: 12px;
    line-height: 16px;
    color: #000000;
    opacity: 0.4;
    right: 25px;
    bottom: 11px;
  }
}
@media (max-width: 639px) {
  .hidden {
    display: none;
  }
  .sender {
    & > textarea {
      padding-right: 3.75rem;
    }
    & > .absolute {
      cursor: pointer;
      margin-top: 1rem;
      display: none;
      right: 110px;
      justify-content: center;
      align-items: center;
      & > img {
        width: 60%;
      }
      &:last-child {
        display: flex;
        padding: 0;
        max-width: 27px;
        max-height: 27px;
        min-width: 27px;
        min-height: 27px;
        right: 25px;
        background: #008fa0;
        border-radius: 50%;
      }
    }
  }
  .message-block {
    &.left {
      & .message {
        margin-left: 0;
        &:before {
          display: none;
        }
      }
    }
  }
}
.burger {
  & > div {
    max-width: 6px;
    max-height: 6px;
    min-width: 6px;
    min-height: 6px;
    margin-top: 4px;
    border-radius: 50%;
    background-color: #c4c4c4;
    & > :first-child {
      margin-top: 0;
    }
  }
}
.burger-show {
  bottom: 0;
  right: 0;
  transform: translateY(80%);
  box-shadow: 0px 10px 25px rgba(0, 0, 0, 0.1);
  border-radius: 10px 0px 10px 10px;
}
</style>
