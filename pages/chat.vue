<template>
  <div class="pt-4 rounded-t-30 mt-4">
    <div class="px-70px flex flex-col">
      <h1 class="page-title text-cyan text-2xl font-bold">Активные диалоги</h1>
      <div class="flex flex-row py-10">
        <div class="flex flex-col pr-3">
          <template v-for="chat in chats">
            <div
              :key="chat.id"
              class="chater bg-white pb-8 rounded-30 flex flex-row justify-between mb-7 px-7 py-6 mt-3 cursor-pointer"
            >
              <div class="flex flex-row">
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
                  <h4 class="font-bold mb-1">{{ chat.fio }}</h4>
                  <span class="text-sm text-opacity-50 text-black">{{
                    chat.last.message
                  }}</span>
                </div>
              </div>
              <div class="flex flex-col justify-between items-start">
                <span class="status text-xs" :class="{ active: chat.active }">{{
                  $moment(chat.last.date).format("hh:mm")
                }}</span>
                <img :src="chat.messanger + '.svg'" />
              </div>
              <div class=""></div>
            </div>
          </template>
        </div>
        <div class="ml-4 w-3/4">
          <div class="flex flex-col bg-white rounded-30">
            <div
              class="flex flex-row px-12 py-6 justify-between border-b border-black border-opacity-10"
            >
              <div class="flex flex-col">
                <h4 class="font-bold mb-1">{{ chats[current_chat].fio }}</h4>
                <div
                  class="flex flex-row text-black text-opacity-50 text-sm mt-3"
                >
                  <img src="wp.svg" class="mr-3" style="width: 22px" />
                  <span>
                    {{ chats[current_chat].phone }},
                    {{ chats[current_chat].city }}
                  </span>
                </div>
              </div>
              <div class="flex flex-row mt-2">
                <button
                  class="py-3 ml-6 px-4 truncate text-cyan border-cyan border rounded-5"
                >
                  Сменить ответственного
                </button>
                <button
                  class="py-3 ml-6 px-4 truncate text-cyan border-cyan border rounded-5"
                >
                  Переместить на этап
                </button>
                <button
                  class="py-3 ml-6 px-4 truncate text-red border-red border rounded-5"
                >
                  Отключить бота
                </button>
              </div>
            </div>
            <div
              class="chat overflow-x-hidden overflow-y-scroll px-8 flex flex-col"
            >
              <template v-for="message in chats[current_chat].chat">
                <div
                  :key="message.id"
                  class="message-block w-full flex py-5"
                  :class="{
                    'left flex-row':
                      message.sender_id &&
                      !message.me &&
                      message.sender_id !== 51,
                    'right flex-row-reverse': message.me,
                    'system flex-row-reverse': !message.sender_id && !message.me
                  }"
                >
                  <div class="ava">
                    <img
                      v-if="message.sender_id && message.sender_id !== 51"
                      src="user.svg"
                    />
                  </div>
                  <div class="message relative">
                    <span>{{ message.message }}</span>
                    <div class="absolute">
                      {{ $moment(message.date).format("hh:mm") }}
                    </div>
                  </div>
                </div>
              </template>
            </div>
            <div
              class="sender px-8 flex justify-end items-center relative flex relative"
            >
              <input
                v-model="form.message"
                type="text"
                class="w-full rounded-full border border-black
              border-opacity-10 py-9 outline-none mt-4 p-70px"
              />
              <div class="absolute"><img src="add_file.svg" /></div>
              <div class="absolute">
                <img src="send.svg" @click="sendMessage()" />
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- <bottom-popup
      v-if="popup"
      :childs="popup_content"
      :title="
        popup_content[0].value ? 'Изменить' : 'Добавить нового сотрудника'
      "
      :button="popup_content[0].value ? 'Сохранить' : 'Добавить'"
      @close="popup = false"
    /> -->
    </div>
  </div>
</template>

<script>
export default {
  middleware: "index",
  data() {
    return {
      current_chat: 0,
      form: {
        message: "",
        files: []
      },
      chats: [
        {
          id: 1,
          fio: "Василий Комков",
          last: {
            date: new Date(),
            message: "Hello world!"
          },
          phone: "+7 770 343 34 34",
          city: "Almaty",
          active: true,
          messanger: "wp",
          chat: [
            {
              id: 1,
              message: "Новое обращение",
              type: "0",
              me: false,
              sender_id: 0,
              files: [],
              date: new Date(new Date().setHours(10, 12, 22))
            },
            {
              id: 2,
              message: "Чат назначен на VasiliyKomkov. Инициатор - VasyaKomkov",
              type: "0",
              me: false,
              sender_id: 0,
              files: [],
              date: new Date(new Date().setHours(10, 14, 10))
            },
            {
              id: 3,
              message: "Hello world!",
              type: "0",
              files: [],
              sender_id: 1,
              me: false,
              date: new Date()
            }
          ]
        },
        {
          id: 2,
          fio: "Не Василий Комков",
          last: {
            date: new Date(),
            message: "Hello world!"
          },
          phone: "+7 770 343 34 34",
          city: "Almaty",
          active: true,
          messanger: "tg",
          chat: [
            {
              id: 4,
              message: "Новое обращение",
              type: "0",
              me: false,
              sender_id: 0,
              files: [],
              date: new Date(new Date().setHours(10, 12, 22))
            },
            {
              id: 5,
              message: "Чат назначен на VasiliyKomkov. Инициатор - VasyaKomkov",
              type: "0",
              me: false,
              sender_id: 0,
              files: [],
              date: new Date(new Date().setHours(10, 14, 10))
            },
            {
              id: 6,
              message: "Hello world!",
              type: "0",
              files: [],
              sender_id: 1,
              me: false,
              date: new Date()
            }
          ]
        }
      ]
    }
  },
  methods: {
    sendMessage() {
      this.addMessage(this.current_chat, {
        ...this.form,
        me: true,
        date: new Date(),
        sender_id: 51,
        type: 0
      })
      this.form = { message: "", files: [] }
    },
    addMessage(index, data) {
      this.chats[index].chat.push(data)
    }
  }
}
</script>

<style lang="scss" scoped>
.chater {
  &:before {
    content: "";
    display: block;
    background-color: #d42d11;
    border-radius: 50px;
    height: 100%;
    width: 5px;
    margin-right: 1rem;
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
  & > input {
    padding-right: 9rem;
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
      margin-left: 58px;
      background: #f5f5f5;
      border-radius: 20px;
      padding: 18px 25px 27px 37px;
      color: #00000040;
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
    }
    & .message {
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
</style>
