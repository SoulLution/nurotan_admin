<template>
  <div class="pt-4 rounded-t-30 mt-15">
    <div class="px-70px flex flex-col">
      <h1 class="page-title text-cyan text-2xl font-bold">
        Заявки
      </h1>
      <div class="flex flex-col py-10 mt-22 bg-white rounded-30">
        <div class="flex flex-row justify-between w-full px-4">
          <div class="flex flex-row">
            <multiselect
              v-model="status"
              class="rounded-5 p-3 bg-opacity-25 cursor-pointer relative z-10"
              style="min-height:50px; width: 200px; display: inline-table"
              :options="statuses"
              :searchable="false"
              :close-on-select="false"
              select-label=""
              label="title"
              selected-label=""
              deselect-label=""
              placeholder="Выберите статус"
              :taggable="true"
            />
            <div class="flex flex-row p-3 items-center" style="height: 60px">
              <span class="mr-4">Период</span>
              <template v-for="i in 2">
                <date-pick
                  :key="i"
                  v-model="date[i - 1]"
                  :format="'YYYY.MM.DD'"
                  next-month-caption="Следующий"
                  prev-month-caption="Предыдущий"
                  set-time-caption="Выбрать"
                  :weekdays="['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']"
                  :months="[
                    'Январь',
                    'Февраль',
                    'Март',
                    'Апрель',
                    'Мая',
                    'Июнь',
                    'Июль',
                    'Август',
                    'Сентябрь',
                    'Октябрь',
                    'Ноябрь',
                    'Декабрь'
                  ]"
                ></date-pick>
              </template>
              <div class="flex flex-row items-center p-3" style="height: 60px">
                <button
                  class="rounded-md bg-cyan hover:bg-white hover:text-cyan border-cyan border px-6 text-white py-2"
                  @click="getUsers()"
                >
                  Применить
                </button>
                <span
                  class="remove ml-4 pb-1 cursor-pointer text-gray-300 hover:text-red border-b border-gray-300 hover:border-red"
                  @click="removeToDefalut()"
                >
                  Сбросить
                </span>
              </div>
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
              class="bg-C4 bg-opacity-10 mr-12 rounded-full pl-15 pr-8 py-6 outline-none w-full"
              type="text"
              placeholder="Поиск ..."
            />
          </div>
        </div>
        <table class="mt-4">
          <thead>
            <tr>
              <td><div>Ответственный менеджер</div></td>
              <td><div>Клиент</div></td>
              <td><div>Статус обращения</div></td>
              <td><div class="text-cyan">Дата и время обращение</div></td>
              <td></td>
            </tr>
          </thead>
          <tbody>
            <template v-for="(user, i) in users">
              <tr :key="user.id">
                <td style="max-width: 75px">
                  <div>{{ user.manager.full_name }}</div>
                </td>
                <td style="max-width: 250px">
                  <div class="flex flex-row items-center">
                    <img :src="user.from + '.svg'" />
                    <span
                      class="truncate ml-2"
                      :title="user.name || user.phone"
                    >
                      {{ user.name || user.phone }}
                    </span>
                  </div>
                </td>
                <td style="max-width: 300px">
                  <div>
                    {{ getStatusName(user.checked) }}
                  </div>
                </td>
                <td>
                  <div>
                    {{ $moment(user.date).format("hh:mm / DD.MM.YYYY") }}
                  </div>
                </td>
                <td class="flex justify-end">
                  <v-button
                    class="whitespace-no-wrap mr-2"
                    title="Открыть чат"
                    @click="
                      $router.push({
                        path: '/chat',
                        query: { user_id: user.client_id }
                      })
                    "
                  />
                  <v-button
                    class="whitespace-no-wrap ml-2"
                    title="Подтвердить"
                    @click="changeUser(i)"
                  />
                </td>
              </tr>
            </template>
          </tbody>
          <tfoot>
            <tr>
              <td colspan="5">
                <pagination v-model="current_page" :max="all_pages" />
              </td>
            </tr>
          </tfoot>
        </table>
      </div>
    </div>
    <confirm-popup
      v-if="users.length && cur_user !== null"
      :popup="popup"
      :answers="users[cur_user].answers"
      @close="e => closeAndSendAnswer(e)"
    />
  </div>
</template>

<script>
export default {
  middleware: "index",
  data() {
    return {
      current_page: 1,
      all_pages: 1,
      tag: [],
      search: "",
      tags: ["12323132132321", 321, 412, 421, 32],
      status: null,
      date: [
        this.$moment(new Date().setDate(1)).format("YYYY.MM.DD"),
        this.$moment(
          new Date(new Date().setMonth(new Date().getMonth() + 1)).setDate(0)
        ).format("YYYY.MM.DD")
      ],
      statuses: [
        {
          id: 3,
          title: "Подтверждён"
        },
        {
          id: 0,
          title: "Не просмотрено"
        },
        {
          id: 1,
          title: "Просмотрено"
        },
        {
          id: 2,
          title: "Отклонён"
        }
      ],
      users: [],
      cur_user: null,
      popup: false
    }
  },
  watch: {
    current_page() {
      this.getUsers()
    }
  },
  created() {
    this.getUsers()
  },
  methods: {
    closeAndSendAnswer(type) {
      if (type !== false) {
        if (type === true)
          this.$axios
            .get(
              `n_update_requestChecked/123123123/${
                this.users[this.cur_user].id
              }/${3}/`
            )
            .then(() => {
              this.users[this.cur_user].checked = 3
            })
        else
          this.$axios
            .get(
              `n_update_requestChecked/123123123/${
                this.users[this.cur_user].id
              }/${2}/`
            )
            .then(() => {
              this.users[this.cur_user].checked = 2
            })
      } else this.popup = false
    },
    removeToDefalut() {
      this.status = null
      this.date = [
        this.$moment(new Date().setDate(1)).format("YYYY.MM.DD"),
        this.$moment(
          new Date(new Date().setMonth(new Date().getMonth() + 1)).setDate(0)
        ).format("YYYY.MM.DD")
      ]
      this.search = ""
    },
    changeUser(index) {
      this.popup = true
      this.cur_user = index
      console.log(this.users[index].checked)
      if (this.users[index].checked === 0)
        this.$axios
          .get(
            `n_update_requestChecked/123123123/${this.users[index].id}/${1}/`
          )
          .then(() => {
            this.users[index].checked = 1
          })
    },
    getStatusName(status) {
      switch (status) {
        case 0:
          return "Не просмотрено"
        case 1:
          return "Просмотрен"
        case 2:
          return "Отклонён"
        case 3:
          return "Одобрен"
      }
    },
    getUsers() {
      let data = {
        checked: this.status ? this.status.id.toString() : "",
        find: this.search,
        "date-start": this.$moment(
          this.date[0] ? this.date[0] : new Date().setDate(1)
        ).format("YYYY-MM-DD"),
        "date-end": this.$moment(
          this.date[1]
            ? this.date[1]
            : new Date(new Date().setMonth(new Date().getMonth() + 1)).setDate(
                0
              )
        ).format("YYYY-MM-DD"),
        page: this.current_page - 1
      }
      data = this.changeData(data)
      this.$axios.post(`/n_requests/1111111111/`, data).then(res => {
        this.users = JSON.parse(res.data.data).map(x => {
          return {
            ...x,
            date: new Date(x.date),
            checked: parseInt(x.checked),
            manager: JSON.parse(x.manager),
            answers: JSON.parse(x.answers)
          }
        })
        this.all_pages = res.data.pages || 1
        this.cur_user = null
      })
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
            content: "";
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
.multiselect__input,
.multiselect__single {
  background: transparent;
  white-space: nowrap;
}
.vdpComponent input {
  font-size: 1rem;
  background: #c4c4c416;
  width: 150px;
  margin-right: 0.5rem;
  padding: 0.5rem 2rem;
}
.vdpClearInput {
  top: 0;
  right: 1rem;
  border-radius: 5px;
  width: auto;
}
</style>
