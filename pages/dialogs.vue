<template>
  <div class="pt-4 rounded-t-30 sm:mt-15">
    <div class="px-4 sm:px-70px flex flex-col">
      <h1 class="page-title text-cyan text-2xl font-bold">
        Все диалоги
      </h1>
      <div class="flex flex-col sm:py-10 sm:mt-22 sm:bg-white rounded-30">
        <div class="flex flex-col sm:flex-row justify-between w-full sm:px-4">
          <div class="flex flex-col sm:flex-row">
            <multiselect
              v-model="canal"
              class="rounded-5 sm:p-3 bg-opacity-25 cursor-pointer relative z-10 w200"
              style="min-height:50px; display: inline-table"
              :options="canals"
              :searchable="false"
              :close-on-select="false"
              select-label=""
              label="title"
              selected-label=""
              deselect-label=""
              placeholder="Выберите Канал"
              :taggable="true"
            />
            <div
              class="flex flex-col sm:p-3 sm:pb-5 sm:flex-row sm:items-center"
            >
              <button
                class="rounded-md bg-cyan hover:bg-white w-full sm:w-auto hover:text-cyan border-cyan border px-6 text-white py-2"
                @click="getClients()"
              >
                Применить
              </button>
              <span
                class="block sm:hidden rounded-md bg-transparent my-2 hover:bg-white w-full text-cyan hover:text-cyan border-cyan border px-6 text-center py-2"
                @click="removeToDefalut()"
              >
                Сбросить
              </span>
              <span
                class="hidden sm:block remove ml-4 pb-1 cursor-pointer text-gray-300 hover:text-red border-b border-gray-300 hover:border-red"
                style="height: 25px"
                @click="removeToDefalut()"
              >
                Сбросить
              </span>
            </div>
          </div>
          <div class="relative flex items-center input">
            <svg
              class="absolute"
              width="14"
              height="14"
              viewBox="0 0 14 14"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <g opacity="0.15">
                <path
                  d="M6.1653 0C2.76585 0 0 2.76585 0 6.1653C0 9.56495 2.76585 12.3306 6.1653 12.3306C9.56495 12.3306 12.3306 9.56495 12.3306 6.1653C12.3306 2.76585 9.56495 0 6.1653 0ZM6.1653 11.1924C3.39339 11.1924 1.13821 8.93725 1.13821 6.16533C1.13821 3.39341 3.39339 1.13821 6.1653 1.13821C8.93722 1.13821 11.1924 3.39339 11.1924 6.1653C11.1924 8.93722 8.93722 11.1924 6.1653 11.1924Z"
                  fill="black"
                />
                <path
                  d="M13.834 13.0283L10.5711 9.76538C10.3488 9.54305 9.98869 9.54305 9.76636 9.76538C9.54403 9.98752 9.54403 10.348 9.76636 10.5701L13.0292 13.833C13.1404 13.9441 13.2859 13.9997 13.4316 13.9997C13.5771 13.9997 13.7228 13.9441 13.834 13.833C14.0563 13.6108 14.0563 13.2504 13.834 13.0283Z"
                  fill="black"
                />
              </g>
            </svg>
            <input
              v-model="search"
              class="bg-white sm:bg-C4 sm:bg-opacity-10 sm:mr-24 rounded-full pl-15 pr-8 py-6 outline-none w-full"
              type="text"
              placeholder="Поиск ..."
            />
          </div>
        </div>
        <table class="hidden sm:table mt-4">
          <thead>
            <tr>
              <td><div>Последний оператор</div></td>
              <td><div>Клиент</div></td>
              <td><div>Мессенджер</div></td>
              <td><div>Последнее сообщение</div></td>
              <!-- <td><div>Теги клиента</div></td> -->
              <td>
                <div class="sort">Последнее сообщение</div>
              </td>
              <td><div class="sort">Первое сообщение</div></td>
              <!-- <td><div>Вложение</div></td> -->
              <td></td>
            </tr>
          </thead>
          <tbody>
            <template v-for="user in users">
              <tr :key="user.id">
                <td>
                  <div>{{ user.manager.full_name }}</div>
                </td>
                <td style="max-width: 125px">
                  <div class="flex flex-row">
                    <svg
                      width="27"
                      viewBox="0 0 27 27"
                      class="fill-current text-cyan"
                      xmlns="http://www.w3.org/2000/svg"
                    >
                      <path
                        d="M19.0646 14.1059C20.6561 12.6164 21.6581 10.5042 21.6581 8.15729C21.6581 3.65954 17.9985 0 13.5008 0C9.00305 0 5.34351 3.65954 5.34351 8.15729C5.34351 10.5042 6.34544 12.616 7.93658 14.1059C5.48175 16.2178 2.14648 19.116 2.14648 25.8049V27H24.8539V25.8049C24.8543 19.1164 21.5194 16.2178 19.0646 14.1059ZM7.7338 8.15769C7.7338 4.97779 10.3209 2.3907 13.5008 2.3907C16.6803 2.3907 19.2678 4.97779 19.2678 8.15769C19.2678 11.3376 16.6807 13.9251 13.5008 13.9251C10.3209 13.9247 7.7338 11.3376 7.7338 8.15769ZM4.57941 24.6097C4.92799 19.8462 7.36211 17.7523 9.52892 15.8887C9.59186 15.8341 9.65441 15.7807 9.71695 15.727C10.9037 16.2357 12.1961 16.5074 13.51 16.5174C14.8083 16.5074 16.0975 16.2357 17.2842 15.727C17.346 15.7807 17.4089 15.8345 17.4723 15.8887C19.6387 17.7523 22.0732 19.8462 22.4218 24.6097H4.57941Z"
                      />
                    </svg>

                    <span
                      class="truncate"
                      :title="user.name ? user.name : user.phone"
                    >
                      {{ user.name ? user.name : user.phone }}
                    </span>
                  </div>
                </td>
                <td>
                  <div class="flex justify-center">
                    <img :src="user.from + '.svg'" />
                  </div>
                </td>
                <td style="max-width: 250px">
                  <div
                    class="truncate pr-4"
                    :title="user.messages[user.messages.length - 1].content"
                    v-html="user.messages[user.messages.length - 1].content"
                  ></div>
                </td>
                <!-- <td>
                  <div>
                    <span v-for="(tag, i) in user.tags" :key="i">{{
                      tag + (i === user.tags.length - 1 ? "" : ", ")
                    }}</span>
                  </div>
                </td> -->
                <td>
                  <div>
                    {{
                      $moment(
                        user.messages[user.messages.length - 1].date
                      ).format(
                        checkFormat(
                          user.messages[user.messages.length - 1].date
                        )
                      )
                    }}
                  </div>
                </td>
                <td>
                  <div>
                    {{
                      $moment(user.messages[0].date).format(
                        checkFormat(user.messages[0].date)
                      )
                    }}
                  </div>
                </td>
                <!-- <td>
                  <div>{{ user.files }}</div>
                </td> -->
                <td class="flex justify-end">
                  <v-button
                    class="whitespace-no-wrap justify-center mr-2"
                    title="Открыть чат"
                    @click="
                      $router.push({
                        path: '/chat',
                        query: { user_id: user.id }
                      })
                    "
                  />
                  <v-button
                    class="whitespace-no-wrap justify-center ml-2"
                    title="Назначить на .."
                    @click="changeUser(user)"
                  />
                </td>
              </tr>
            </template>
          </tbody>
          <tfoot>
            <tr>
              <td colspan="9">
                <pagination v-model="current_page" :max="pages" />
              </td>
            </tr>
          </tfoot>
        </table>
        <div class="flex sm:hidden flex-col pr-3">
          <pagination
            v-if="pages > 1"
            v-model="current_page"
            class="mt-4"
            :max="pages"
          />
          <template v-for="list in users">
            <router-link
              :key="list.id"
              :to="'/chat?user_id=' + list.id"
              class="chater bg-white pb-8 rounded-30 flex flex-row justify-between pl-11 pr-7 py-6 mt-3 cursor-pointer"
            >
              <div class="flex flex-row justify-start w-full overflow-hidden">
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
              <div class="flex flex-col justify-start items-start">
                <span class="status text-xs mb-4">
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
          <pagination v-model="current_page" class="mt-4" :max="pages" />
        </div>
      </div>
    </div>
    <bottom-manager-popup
      :popup="popup"
      title="Изменить"
      button="Сохранить"
      @close="e => changeManager(e)"
    />
  </div>
</template>

<script>
export default {
  middleware: "index",
  data() {
    return {
      current_page: 1,
      // tag: [],
      // tags: ["12323132132321", 321, 412, 421, 32],
      canal: null,
      search: "",
      canals: [
        {
          id: "tg",
          title: "Телеграм"
        },
        {
          id: "wp",
          title: "WhatsApp"
        }
      ],
      users: [],
      current_user: null,
      popup: false,
      pages: 1
    }
  },
  watch: {
    search() {
      this.getClients()
    },
    // canal() {
    //   this.getClients()
    // },
    current_page() {
      this.getClients()
    }
  },
  created() {
    this.getClients()
  },
  methods: {
    removeToDefalut() {
      this.canal = null
      this.search = ""
      this.getClients()
    },
    changeManager(e) {
      if (e)
        this.$axios
          .get(
            `/update_changeManager/123123123/${this.current_user.id}/${e.id}/`
          )
          .then(() => [(this.current_user.manager = e)])
      this.popup = false
    },
    getClients() {
      let data = {
        find: this.search,
        from: this.canal && this.canal.id ? this.canal.id : "",
        page: (this.current_page - 1) * 7,
        user_id:
          JSON.parse(localStorage.getItem("auth")).is_admin == 1
            ? 0
            : JSON.parse(localStorage.getItem("auth")).id
      }
      this.$axios
        .post("/ClientsList/123123123/", this.changeData(data))
        .then(res => {
          this.pages = res.data.pages
          this.users = JSON.parse(res.data.data).map(x => {
            return {
              ...x,
              messages: JSON.parse(x.messages),
              manager: JSON.parse(x.manager)
            }
          })
          console.log(this.users[0])
        })
    },
    checkFormat(date) {
      return this.$moment(date).format("YY.MM.DD") !==
        this.$moment(new Date()).format("YY.MM.DD")
        ? "DD.MM.YY HH:mm"
        : "HH:mm"
    },
    changeUser(user) {
      this.popup = true
      this.current_user = user
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
.absolute {
  left: 36px;
}
.input {
  width: 100%;
  max-width: 550px;
}
table {
  border-collapse: separate;
  border-spacing: 0;
  & thead {
    border-bottom: 1px solid #00000015;
    color: #828282;
    & td {
      border-left: 1px solid #00000015;
      &:first-child {
        border-left: 0;
      }
      & > div {
        position: relative;
        display: flex;
        &.sort {
          color: #008fa0;
          &:after {
            // content: "";
            display: block;
            left: 20px;
            transform: translateY(8px);
            margin-left: 0.75rem;
            max-width: 12px;
            max-height: 7px;
            min-width: 12px;
            min-height: 7px;
            background-image: url("/down_cyan.png");
            background-repeat: no-repeat;
            background-position: 0 0;
          }
        }
      }
    }
  }
  & td {
    padding-top: 24px;
    padding-bottom: 30px;
    padding-left: 20px;
    padding-right: 20px;
    border-top: 1px solid #00000015;
  }
}
.w200 {
  width: 200px;
}
@media (max-width: 639px) {
  .w200 {
    width: 100%;
  }
}
</style>
<style lang="scss">
.multiselect__select {
  top: 11px;
  right: 4px;
}
.multiselect__tags,
.multiselect__input {
  background: #c4c4c410;
  border-radius: 5px;
}
.multiselect__input {
  background: transparent;
}

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
    min-width: 45px;
    max-width: 45px;
    min-height: 45px;
    max-height: 45px;
    background: #008fa0;
    border-radius: 50%;
    margin-right: 2rem;
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
    & > img {
      width: 40%;
    }
    & > .absolute {
      min-width: 27px;
      max-width: 27px;
      min-height: 27px;
      max-height: 27px;
      right: 0;
      bottom: 0;
      transform: translate(-5%, 25%);
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
</style>
