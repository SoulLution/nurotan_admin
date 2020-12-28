<template>
  <div class="px-70px" style="min-height: 120vh; padding-bottom: 225px">
    <div class="flex flex-row justify-between items-center mt-15">
      <h1 class="page-title text-cyan text-2xl font-bold">
        Конструктор диалогов
      </h1>
      <div class="flex flex-col items-start">
        <div class="flex flex-row">
          <!-- <v-button class="mr-10" title="Приаязать шаблон" />
          <v-button
            title="Создать сообщение"
            :plus="true"
            @click="addBranch()"
          /> -->
        </div>
      </div>
    </div>
    <load-popup :popup="load" />
    <bottom-special-popup
      class="z-20"
      :popup="true"
      title="Внести изменения в чат бота"
      button="Сохранить"
      @close="e => saveAllBranches(e)"
    />
    <input-popup
      v-if="popup"
      :type="popup_type"
      :value="checkValue"
      @close="e => addAnswer('', e)"
    />
    <all-popup
      v-if="popup_all"
      :list="getForAll"
      @close="e => addCopyBranch(e)"
    />
    <templates-popup
      v-if="popup_templates"
      :list="templates"
      @close="e => changeOnTemplate(e)"
    />
    <div>
      <div class="flex flex-row mt-24 w-full">
        <div class="w-1/3 pr-11">
          <div
            class="sticky overflow-hidden pb-10 pt-5 flex flex-col items-center top-0 bg-white rounded-30"
          >
            <template v-for="(item, i) in templates">
              <div
                :key="item.id"
                class="template relative border-b border-black border-opacity-10 flex justify-between items-center py-12 pl-15 pr-8 w-full cursor-pointer"
                :class="{ active: item.id === current_template }"
                @click="changeTree(i)"
              >
                <span v-html="item.title"></span>
                <div v-if="item.id !== 1" class="flex flex-row">
                  <pencil style="margin-left: 0" @click="redactTemplate(i)" />
                  <delete
                    class="text-red border-red"
                    style="margin-left: 1rem"
                    @click="removeTemplate(i)"
                  />
                </div>
              </div>
            </template>
            <v-button
              class=" mt-15"
              :plus="true"
              title="Добавить"
              @click="addTree()"
            />
          </div>
        </div>
        <div class="w-2/3">
          <div class="flex flex-row flex-wrap">
            <template v-for="(branch, i) in tree">
              <branch
                :key="branch.id"
                :branch="branch"
                :i="i"
                @change-is-request="e => (branch.is_request = e)"
                @change-for-all="e => changeForAll(branch, e)"
                @open-title="e => changeTitle(i)"
                @open-answer="e => changeAnswer(i, e)"
                @change-type="e => changeType(e, i)"
                @change-current="e => changeCurrent(e, i)"
                @add-answer="addAnswer(branch)"
                @remove-answer="e => removeAnswer(e, branch)"
              />
            </template>
            <div
              v-if="
                !tree.length ||
                  tree[tree.length - 1].current !== undefined ||
                  tree[tree.length - 1].for_all_active
              "
              key="new"
              class="w-1/2 mb-10"
              :class="tree.length % 2 === 0 ? 'pr-5' : 'pl-5'"
            >
              <div
                class="flex flex-col bg-transparent border items-center justify-center border-dashed border-C4 h-full rounded-30 px-10 py-8 w-full"
              >
                <v-button
                  class="w-full justify-center mb-4"
                  title="Выбрать существующий"
                  @click="openAllBranches()"
                />
                <v-button
                  class="w-full justify-center mb-4"
                  title="Привязать шаблон"
                  @click="openTemplates()"
                />
                <v-button
                  class="w-full justify-center"
                  title="Создать сообщение"
                  @click="addBranch()"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
let new_in_all_branches = {}

const getRand16bit = () => {
  return Math.round(Math.random() * 100000000)
    .toString(16)
    .toUpperCase()
}
export default {
  middleware: "admin",
  data() {
    return {
      load: false,
      error: false,
      popup: false,
      popup_all: false,
      popup_templates: false,
      current_template: 1,
      redact_template: false,
      current_branch: null,
      current_answer: null,
      current_in_tree: null,
      popup_type: 0,
      templates: [
        {
          id: 1,
          title: "Основное меню",
          branch: 1
        }
      ],
      all_branches: [],
      tree: [],
      branch_template: {
        title: "Сообщение",
        answers_type: 0,
        is_request: undefined,
        current: undefined,
        to_branch: null,
        for_all: false,
        for_all_active: false,
        answers: [
          {
            id: -1,
            content: "Вариант ответа",
            to_branch: null
          },
          {
            id: "text",
            content: "",
            to_branch: null
          }
        ]
      }
    }
  },
  head() {
    return {
      title: "Конструктор диалогов"
    }
  },
  computed: {
    getForAll() {
      return this.all_branches.filter(x => {
        let res = true
        this.tree.forEach(k => {
          if (k.id === x.id) res = false
        })
        return res
      })
    },
    checkValue() {
      return this.redact_template
        ? this.redact_template.title
        : this.current_answer
        ? this.current_answer.content
        : this.current_in_tree
        ? this.current_in_tree.title
        : ""
    }
  },
  watch: {
    templates: {
      deep: true,
      handler(newData) {
        localStorage.setItem("templates", JSON.stringify(newData))
      }
    },
    all_branches: {
      deep: true,
      handler(newData) {
        localStorage.setItem(
          "bot",
          JSON.stringify(
            newData.map(x => {
              return {
                ...x,
                current: undefined
              }
            })
          )
        )
      }
    }
  },
  created() {
    this.getAllBranches()
    this.getAllTemplates()
  },
  methods: {
    async saveAllBranches(type) {
      try {
        let show = false
        localStorage.setItem("back_up", JSON.stringify(this.all_branches))
        if (!type) {
          localStorage.setItem("bot", "")
          this.getAllBranches()
          localStorage.setItem("templates", "")
          this.getAllTemplates()
        } else {
          this.load = true
          for await (const branch of this.all_branches.map(e =>
            (e.id + "").indexOf("-") > -1 ? this.uploadBranch(e) : ""
          ))
            if (show) console.log(branch)
          for await (const branch of this.all_branches.map(e =>
            this.uploadBranch(e)
          ))
            if (show) console.log(branch)
          for (const branch of this.all_branches)
            for await (const answer of branch.answers.map(e =>
              this.uploadAnswer(branch, e)
            ))
              if (show) console.log(answer)
          for await (const template of this.templates.map(e =>
            this.uploadTemplates(e)
          ))
            if (show) console.log(template)
          new_in_all_branches = {}
          localStorage.setItem("bot", "")
          this.getAllBranches()
          localStorage.setItem("templates", "")
          this.getAllTemplates()
        }
        this.load = false
      } catch {
        this.load = false
        this.error = true
        localStorage.setItem("bot", localStorage.setItem("back_up"))
      }
    },
    uploadTemplates(template) {
      let to_branch = new_in_all_branches[template.to_branch]
      if (!to_branch) to_branch = template.to_branch
      return new Promise((resolve, reject) => {
        if (template.id < 0) {
          this.$axios
            .get(
              `/n_CreateTemplate/123123132/${this.splitingForContent(
                template.title
              )}/${to_branch}/`
            )
            .then(res => {
              template.id = res.data[0]
              template.to_branch = to_branch
              resolve(true)
            })
            .catch(() => reject(false))
        } else {
          this.$axios
            .get(
              `/n_UpdateTemplate/123123132/${
                template.id
              }/${this.splitingForContent(template.title)}/${to_branch}/`
            )
            .then(() => resolve(true))
            .catch(() => reject(false))
        }
      })
    },
    uploadAnswer(branch, answer) {
      if (answer && answer.id && answer.id !== "text") {
        let from = answer.to_branch
        if (branch.for_all) from = branch.for_all
        let to_branch = new_in_all_branches[from]
        if (!to_branch) to_branch = from
        return new Promise((resolve, reject) => {
          if ((answer.id + "").indexOf("-") > -1) {
            this.$axios
              .get(
                `/n_CreateAnswer/123123132/${
                  branch.id
                }/${this.splitingForContent(answer.content)}/${
                  answer.tag_id
                }/${to_branch}/`
              )
              .then(res => {
                answer.id = res.data[0]
                answer.to_branch = to_branch
                resolve(true)
              })
              .catch(() => reject(false))
          } else {
            this.$axios
              .get(
                `/n_UpdateAnswer/123123132/${answer.id}/${
                  branch.id
                }/${this.splitingForContent(answer.content)}/${
                  answer.tag_id
                }/${to_branch}/`
              )
              .then(() => resolve(true))
              .catch(() => reject(false))
          }
        })
      }
    },
    uploadBranch(branch) {
      return new Promise((resolve, reject) => {
        if ((branch.id + "").indexOf("-") > -1) {
          this.$axios
            .get(
              `/n_CreateBranch/123123132/${
                branch.answers_type
              }/${this.splitingForContent(
                branch.is_request
              )}/${this.splitingForContent(branch.title)}/${branch.to_branch}/${
                branch.for_all_active ? branch.for_all : false
              }/`
            )
            .then(res => {
              new_in_all_branches[branch.id] = res.data[0]
              branch.id = res.data[0]
              resolve(true)
            })
            .catch(() => reject(false))
        } else {
          let to_branch = new_in_all_branches[branch.to_branch]
          if (!to_branch) to_branch = branch.to_branch
          let for_all = new_in_all_branches[branch.for_all]
          if (!for_all) for_all = branch.for_all
          this.$axios
            .get(
              `/n_UpdateBranch/123123132/${branch.id}/${
                branch.answers_type
              }/${this.splitingForContent(
                branch.is_request
              )}/${this.splitingForContent(branch.title)}/${to_branch}/${
                branch.for_all ? for_all : false
              }/`
            )
            .then(() => resolve(true))
            .catch(() => reject(false))
        }
      })
    },
    splitingForContent(string) {
      if (typeof string === "string")
        return string
          .split("/")
          .join("*!*")
          .split("?")
          .join("@!@")
      else return string
    },
    getAllTemplates() {
      if (!localStorage.getItem("templates"))
        this.$axios.get(`/n_getTemplateList/123123132/`).then(res => {
          this.templates = res.data
          localStorage.setItem("templates", JSON.stringify(this.templates))
        })
      else this.templates = JSON.parse(localStorage.getItem("templates"))
    },
    getAllBranches() {
      if (
        !localStorage.getItem("bot") ||
        (localStorage.getItem("bot") &&
          !JSON.parse(localStorage.getItem("bot")).length)
      )
        this.$axios.get(`/n_getBranchList/123123132/`).then(res => {
          let all_branches = res.data.map(x => {
            let answers = JSON.parse(x.answers)
            answers.push({
              id: "text",
              content: "",
              to_branch: null
            })
            return {
              ...x,
              answers,
              is_request:
                x.is_request === "undefined" ? undefined : x.is_request,
              answers_type: parseInt(x.answers_type),
              for_all_active: x.for_all && x.for_all !== "false",
              for_all:
                !x.for_all || x.for_all === "false"
                  ? false
                  : parseInt(x.for_all),
              current: undefined
            }
          })
          localStorage.setItem("bot", JSON.stringify(all_branches))
          this.all_branches = all_branches
          this.tree = [this.all_branches[0]]
        })
      else {
        this.all_branches = JSON.parse(localStorage.getItem("bot")).map(x => {
          return {
            ...x,
            current: undefined,
            for_all_active: false
          }
        })
        this.tree = [this.all_branches[0]]
      }
    },
    addCopyBranch(data) {
      if (data) {
        if (data.save_structure) {
          this.checkOnCurrent(data.branch.id)
          this.addBranch()
        } else {
          let branch = JSON.parse(JSON.stringify(data.branch))
          const len = this.tree.length - 1
          branch.id =
            this.tree[len].id +
            "-" +
            this.tree[len].current +
            "-" +
            getRand16bit()
          branch.to_branch = null
          branch.current = undefined
          branch.answers.forEach(x => {
            if (!isNaN(parseInt(x.id)) && parseInt(x.id) > 0) {
              x.id *= -1
              x.id += "backup"
            }
            x.to_branch = null
          })
          this.checkOnCurrent(branch.id)
          this.all_branches.push(branch)
          this.addBranch()
        }
      }
      this.popup_all = false
    },
    redactTemplate(index) {
      this.popup = true
      this.popup_type = 0
      this.redact_template = this.templates[index]
    },
    removeTemplate(index) {
      if (this.templates[index].id > 0)
        this.$axios
          .get(`/n_blockTemplate/123123132/${this.templates[index].id}`)
          .then(res => {
            if (res.status) this.templates.splice(index, 1)
          })
      else this.templates.splice(index, 1)
    },
    addTree() {
      this.templates.push({
        id:
          (Math.abs(
            this.templates.reduce((p, v) =>
              parseInt(p.id) > parseInt(v.id) ? v : p
            ).id
          ) +
            1) *
          -1,
        title: "Новый шаблон",
        to_branch: 0
      })
      this.popup = true
      this.popup_type = 0
      this.redact_template = this.templates[this.templates.length - 1]
    },
    changeTree(index) {
      this.current_template = this.templates[index].id
      console.log(this.templates[index].to_branch)
      if (
        this.templates[index].to_branch &&
        this.templates[index].to_branch !== "0"
      )
        this.tree = [
          this.all_branches[
            this.findInAllBranches(this.templates[index].to_branch)
          ]
        ]
      else this.tree = []
    },
    openAllBranches() {
      this.popup_all = true
    },
    openTemplates() {
      this.popup_templates = true
    },
    checkOnCurrent(id) {
      const len = this.tree.length - 1
      if (this.tree[len].for_all_active) this.tree[len].for_all = id
      else if (this.tree[len].answers_type == 2) this.tree[len].to_branch = id
      else
        this.tree[len].answers[
          this.tree[len].answers.findIndex(x => x.id === this.tree[len].current)
        ].to_branch = id
    },
    async changeOnTemplate(branch_id) {
      this.popup_templates = false
      if (branch_id) {
        this.checkOnCurrent(await this.insertCopyBranch(branch_id))
        this.addBranch(branch_id)
      }
    },
    async insertCopyBranch(id) {
      let b = JSON.parse(
        JSON.stringify(this.all_branches[this.findInAllBranches(id)])
      )
      let branch = {
        ...b,
        answers: b.answers.map(x => {
          return {
            ...x,
            id: Math.abs(x.id) * -1
          }
        }),
        id: b.id + "-!" + this._uid,
        current: undefined
      }
      this.all_branches.push(branch)
      if (branch.to_branch && branch.to_branch !== "undefined")
        branch.to_branch = await this.insertCopyBranch(branch.to_branch)
      for (let answer of branch.answers)
        if (answer.to_branch && answer.to_branch !== "null")
          answer.to_branch = await this.insertCopyBranch(answer.to_branch)
      return branch.id
    },
    changeForAll(branch, bool) {
      branch.for_all_active = bool
      if (bool && branch.for_all) this.addBranch()
      else if (this.tree[this.tree.length - 1].id !== branch.id)
        this.tree.splice(this.tree.length - 1, 1)
    },
    changeTitle(branch_index) {
      this.popup = true
      this.popup_type = 0
      this.current_in_tree = this.tree[branch_index]
      this.current_branch = this.tree[branch_index]
    },
    changeAnswer(branch_index, index) {
      this.popup = true
      this.popup_type = 0
      this.current_in_tree = this.tree[branch_index]
      this.current_branch = this.tree[branch_index]
      this.current_answer = this.current_branch.answers[index]
    },
    changeType(type, i) {
      this.tree[i].current = undefined
      this.tree[i].for_all_active = false
      if (type === 2) this.changeCurrent("text", i)
      if (this.tree[i].answers_type === 2) this.changeCurrent(undefined, i)
      this.tree[i].answers_type = type
    },
    removeAnswer(index, branch) {
      if (branch.current === branch.answers[index].id)
        branch.current = undefined
      if (branch.answers[index].id > 0)
        this.$axios.get(
          `/n_DeleteAnswer/123123123/${branch.answers[index].id}/`
        )
      branch.answers.splice(index, 1)
    },
    addAnswer(branch, e) {
      this.popup = !this.popup
      if (branch) this.current_branch = branch
      if (!this.popup_type && e) {
        if (this.redact_template) {
          this.redact_template.title = e[0]
        } else if (this.current_answer) {
          this.current_answer.content = e[0]
        } else {
          this.current_in_tree.title = e[0]
        }
      } else if (e) {
        for (let x of e)
          this.current_branch.answers.splice(0, 0, {
            id:
              this.current_branch.answers.length > 1
                ? (Math.abs(
                    this.current_branch.answers.reduce((p, v) =>
                      isNaN(parseInt(v.id))
                        ? p
                        : parseInt(p.id) > parseInt(v.id)
                        ? v
                        : p
                    ).id
                  ) +
                    1) *
                  -1
                : -1,
            content: x,
            to_branch:
              this.current_branch.for_all_active &&
              this.current_branch.for_all !== true
                ? this.current_branch.for_all
                : null
          })
      } else {
        this.current_branch = branch
      }
      this.popup_type = 1
      this.redact_template = null
      this.current_answer = null
      this.current_in_tree = null
    },
    changeCurrent(index, i) {
      if (index === "text") {
        this.addBranch()
      }
      this.tree[i].current = index
      this.tree.splice(i + 1, this.tree.length)
      let item = this.tree[i].answers[
        this.tree[i].answers.findIndex(x => x.id === this.tree[i].current)
      ]
      if (item && item.to_branch && item.to_branch !== "null") this.addBranch()
    },
    createBranchTemplate(with_id) {
      let template = JSON.parse(JSON.stringify(this.branch_template))
      template.id = this.current_template + with_id + getRand16bit()
      template.title += " " + template.id
      template.current = undefined
      template.is_request = undefined
      template.for_all = false
      template.for_all_active = false

      this.all_branches.push(template)
      this.tree.push(this.all_branches[this.all_branches.length - 1])

      return template
    },
    addBranch() {
      let me = this.tree[this.tree.length - 1]
      if (me.for_all_active && me.for_all) {
        this.tree.push(this.all_branches[this.findInAllBranches(me.for_all)])
        if (this.all_branches[this.findInAllBranches(me.for_all)])
          this.$nextTick(() => this.addBranch())
      } else if (
        me &&
        me.current &&
        me.answers_type !== 2 &&
        me.answers[me.answers.findIndex(x => x.id === me.current)].to_branch &&
        me.answers[me.answers.findIndex(x => x.id === me.current)].to_branch !==
          "null"
      ) {
        this.all_branches[
          this.findInAllBranches(
            me.answers[me.answers.findIndex(x => x.id === me.current)].to_branch
          )
        ].current = undefined
        let find_branch = this.all_branches[
          this.findInAllBranches(
            me.answers[me.answers.findIndex(x => x.id === me.current)].to_branch
          )
        ]
        if (
          find_branch.answers_type == 2 ||
          (find_branch.for_all && find_branch.for_all_active)
        )
          this.$nextTick(() => this.addBranch())
        this.tree.push(find_branch)
      } else if (me.answers_type == 2 && me.to_branch) {
        this.all_branches[
          this.findInAllBranches(me.to_branch)
        ].current = undefined
        this.tree.push(this.all_branches[this.findInAllBranches(me.to_branch)])
        if (this.all_branches[this.findInAllBranches(me.to_branch)])
          this.$nextTick(() => this.addBranch())
      } else if (!me) {
        // push in template
        let template = this.createBranchTemplate("-" + 0 + "-")
        if (this.tree.length)
          me.answers[me.answers.findIndex(x => x.id === me.current)].to_branch =
            template.id
        this.templates[
          this.templates.findIndex(x => x.id === this.current_template)
        ].to_branch = template.id
      } else if (me.for_all_active) {
        let template = this.createBranchTemplate("-for_all-")
        me.for_all = template.id
      } else if (me.current !== undefined) {
        let template = this.createBranchTemplate("-" + me.current + "-")
        me.answers[me.answers.findIndex(x => x.id === me.current)].to_branch =
          template.id
        if (me.current === "text") me.to_branch = template.id
      }
    },
    findInAllBranches(id) {
      return this.all_branches.findIndex(x => x.id == id)
    }
  }
}
</script>

<style lang="scss">
.template {
  transition: 0.3s;
  &:before {
    content: "";
    position: absolute;
    left: 0;
    top: 0;
    height: 100%;
    transform: scaleY(0);
    width: 6px;
    transition: 0.3s;
    background-color: #008fa0;
    border-radius: 5px;
  }
  &.active {
    box-shadow: 0px 4px 100px rgba(0, 0, 0, 0.1);
    &:before {
      transform: scaleY(1);
    }
  }
}
.type {
  transition: 0.3s;
  &.active {
    box-shadow: 0px 4px 100px rgba(0, 0, 0, 0.2);
  }
}
</style>
