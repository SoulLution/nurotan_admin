<template>
  <div class="bg-white pt-4 rounded-t-30 mt-22">
    <div class="px-70px flex flex-col">
      <h1 class="page-title cyan text-cyan text-2xl font-bold">
        Сотрудники
      </h1>
      <div class="flex flex-row justify-end w-full">
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
            class="bg-C4 bg-opacity-10 mr-24 rounded-full pl-15 pr-8 py-6 outline-none w-full"
            type="text"
            placeholder="Поиск ..."
          />
        </div>
        <v-button
          title="Создать сотрудника"
          :plus="true"
          @click="changeUser({})"
        />
      </div>
      <table class="mt-24">
        <thead>
          <tr>
            <td
              class="cursor-pointer hover:bg-gray-100"
              :class="{
                active: sort_by.value === 'id' && sort_by.type === 'asc'
              }"
              @click="changeSort('id')"
            >
              <div>Код</div>
            </td>
            <td
              class="cursor-pointer hover:bg-gray-100"
              :class="{
                active: sort_by.value === 'full_name' && sort_by.type === 'asc'
              }"
              @click="changeSort('full_name')"
            >
              <div>Ф.И.О.</div>
            </td>
            <td
              class="cursor-pointer hover:bg-gray-100"
              :class="{
                active: sort_by.value === 'is_admin' && sort_by.type === 'asc'
              }"
              @click="changeSort('is_admin')"
            >
              <div>Должность</div>
            </td>
            <td
              class="cursor-pointer hover:bg-gray-100"
              :class="{
                active: sort_by.value === 'phone' && sort_by.type === 'asc'
              }"
              @click="changeSort('phone')"
            >
              <div>Телефон</div>
            </td>
            <td
              class="cursor-pointer hover:bg-gray-100"
              :class="{
                active: sort_by.value === 'email' && sort_by.type === 'asc'
              }"
              @click="changeSort('email')"
            >
              <div>E-mail</div>
            </td>
            <td></td>
          </tr>
        </thead>
        <tbody v-if="users.length">
          <template v-for="user in 7">
            <tr
              v-if="users[user + (current_page - 1) * 7 - 1]"
              :key="users[user + (current_page - 1) * 7 - 1].id"
            >
              <td>
                <div>#{{ users[user + (current_page - 1) * 7 - 1].code }}</div>
              </td>
              <td>
                <div>
                  {{ users[user + (current_page - 1) * 7 - 1].full_name }}
                </div>
              </td>
              <td>
                <div>{{ users[user + (current_page - 1) * 7 - 1].post }}</div>
              </td>
              <td>
                <div>{{ users[user + (current_page - 1) * 7 - 1].phone }}</div>
              </td>
              <td>
                <div>{{ users[user + (current_page - 1) * 7 - 1].email }}</div>
              </td>
              <td class="flex justify-end">
                <pencil
                  @click="changeUser(users[user + (current_page - 1) * 7 - 1])"
                />
                <delete
                  class="text-white border-red bg-red"
                  @click="blockUser(user + (current_page - 1) * 7 - 1)"
                />
              </td>
            </tr>
          </template>
        </tbody>
        <tfoot>
          <tr>
            <td colspan="6">
              <pagination
                v-model="current_page"
                :max="Math.ceil(users.length / 7)"
              />
            </td>
          </tr>
        </tfoot>
      </table>
    </div>
    <bottom-popup
      :popup="popup"
      :childs="popup_content"
      :title="popup_id ? 'Изменить' : 'Добавить нового сотрудника'"
      :button="popup_id ? 'Сохранить' : 'Добавить'"
      @close="e => (e ? sendUser() : (popup = false))"
    />
  </div>
</template>

<script>
import vInput from "@/components/vInputBottom"
import vSelect from "@/components/vSelect"
export default {
  middleware: "admin",
  data() {
    return {
      current_page: 1,
      users: [],
      popup: false,
      popup_id: 0,
      popup_content: [
        {
          title: "Ф.И.О.",
          component: vInput,
          value: "",
          placeholder: "Введите ФИО сотрудника"
        },
        {
          title: "Должность",
          component: vSelect,
          value: "Менеджер",
          childs: ["Менеджер", "Администратор"]
        },
        {
          title: "Пароль",
          component: vInput,
          type: "password",
          value: "",
          placeholder: "Введите пароль"
        },
        {},
        {
          title: "Номер телефона",
          component: vInput,
          value: "",
          type: "phone",
          placeholder: "Введите номер"
        },
        {
          title: "E-mail",
          component: vInput,
          type: "email",
          value: "",
          placeholder: "Введите email"
        }
      ],
      sort_by: {
        value: "id",
        type: "asc"
      }
    }
  },
  watch: {
    sort_by: {
      deep: true,
      handler() {
        this.getUsers()
      }
    }
  },
  created() {
    this.getUsers()
  },
  methods: {
    sendUser() {
      this.popup = false
      this.$axios
        .get(
          `/${this.popup_id ? "n_update" : "n_addUset"}/1111111111/${
            this.popup_id ? this.popup_id + "/" : ""
          }${this.popup_content[0].value}/${
            this.popup_content[1].value === "Менеджер" ? 0 : 1
          }/
        ${this.popup_content[2].value}/
        ${this.popup_content[4].value}/
        ${this.popup_content[5].value}/`
        )
        .then(res => {
          if (this.popup_id) {
            let user = this.users[
              this.users.findIndex(x => x.id === this.popup_id)
            ]
            user.full_name = this.popup_content[0].value
            user.post = this.popup_content[1].value
            user.phone = this.popup_content[4].value
            user.email = this.popup_content[5].value
          } else {
            let user = {
              id: res.data[0],
              code: res.data[0].padStart(13, 0),
              email: this.popup_content[5].value,
              fio: this.popup_content[0].value,
              post: this.popup_content[1].value,
              phone: this.popup_content[4].value
            }
            this.users.splice(0, 0, user)
          }
          this.popup_content[0].value = ""
          this.popup_content[1].value = "Менеджер"
          this.popup_content[4].value = ""
          this.popup_content[5].value = ""
        })
    },
    blockUser(index) {
      this.$axios
        .get(`/n_blockUser/1111111111/${this.users[index].id}/`)
        .then(() => {
          this.users.splice(index, 1)
        })
    },
    changeSort(type) {
      if (type === this.sort_by.value)
        this.sort_by.type = this.sort_by.type === "asc" ? "desc" : "asc"
      else {
        this.sort_by.value = type
        this.sort_by.type = "asc"
      }
    },
    getUsers() {
      this.$axios
        .get(
          `/n_userList/1111111111/${this.sort_by.value}/${this.sort_by.type}/`
        )
        .then(res => {
          this.users = res.data.map(x => {
            if (x.blocked !== "Заблокирован")
              return {
                ...x,
                code: (x.id + "").padStart(13, 0),
                post: x.is_admin ? "Администратор" : "Менеджер"
              }
          })
        })
    },
    changeUser(user) {
      this.popup = true
      this.popup_id = user.id
      this.popup_content[0].value = user.full_name
      this.popup_content[1].value = user.post
      this.popup_content[2].value = user.password
      this.popup_content[4].value = user.phone
      this.popup_content[5].value = user.email
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
    border-bottom: 1px solid #d3dff0;
    & td {
      border-left: 1px solid #d3dff0;
      &.active {
        & > div {
          &:after {
            transform: translateY(8px) scale(1, -1);
          }
        }
      }
      & > div {
        position: relative;
        display: flex;
        &:before {
          content: "";
          display: block;
          left: 20px;
          transform: translateY(2px);
          margin-right: 1rem;
          max-width: 12px;
          max-height: 15px;
          min-width: 12px;
          min-height: 15px;
          background-image: url("/anchor.png");
          background-repeat: no-repeat;
          background-position: 0 0;
        }
        &:after {
          content: "";
          display: block;
          left: 20px;
          transform: translateY(8px);
          margin-left: 0.75rem;
          max-width: 9px;
          max-height: 6px;
          min-width: 9px;
          min-height: 6px;
          transition: 0.3s;
          background-image: url("/down.png");
          background-repeat: no-repeat;
          background-position: 0 0;
        }
      }
      &:first-child {
        border-top-left-radius: 40px;
      }
      &:last-child {
        border-top-right-radius: 40px;
      }
    }
  }
  & td {
    padding-top: 35px;
    padding-bottom: 35px;
    padding-left: 20px;
    padding-right: 20px;
    border-top: 1px solid #d3dff0;
    &:first-child {
      border-left: 1px solid #d3dff0;
    }
    &:last-child {
      border-right: 1px solid #d3dff0;
    }
  }
}
</style>
