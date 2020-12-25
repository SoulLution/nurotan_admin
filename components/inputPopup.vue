<template>
  <div
    class="popup fixed w-full h-full top-0 left-0 flex justify-center items-center z-50"
  >
    <div
      class="popup-bg bg-black bg-opacity-10 w-full h-full absolute left-0 top-0 z-0"
      @click="$emit('close', false)"
    ></div>
    <div
      class="popup-content px-24 py-15 pt-24 relative z-10 bg-white rounded-20 flex flex-col justify-start items-start"
    >
      <h5 class="font-normal mt-12 text-d_blue">Добавление сообщении</h5>

      <div
        class="flex flex-col w-full rounded-10 border border-black border-opacity-10 mt-9"
      >
        <editor-menu-bar v-slot="{ commands, isActive }" :editor="message">
          <div
            class="flex flex-row w-full justify-start py-4 px-5 border-b border-black border-opacity-10"
          >
            <button
              :class="{ 'is-active': isActive.bold() }"
              @click="commands.bold"
            >
              <svg
                class="cursor-pointer fill-current text-black hover:text-d_blue"
                width="24"
                height="12"
                viewBox="0 0 12 12"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  opacity="0.3"
                  d="M8.00684 5.68066C9.1377 5.94434 9.93164 6.26367 10.3887 6.63867C11.0449 7.17188 11.373 7.86328 11.373 8.71289C11.373 9.60938 11.0127 10.3506 10.292 10.9365C9.40723 11.6455 8.12109 12 6.43359 12H0.37793V11.6748C0.928711 11.6748 1.30078 11.625 1.49414 11.5254C1.69336 11.4199 1.83105 11.2852 1.90723 11.1211C1.98926 10.957 2.03027 10.5527 2.03027 9.9082V2.17383C2.03027 1.5293 1.98926 1.125 1.90723 0.960938C1.83105 0.791016 1.69336 0.65625 1.49414 0.556641C1.29492 0.457031 0.922852 0.407227 0.37793 0.407227V0.0820312H6.09082C7.45605 0.0820312 8.42285 0.205078 8.99121 0.451172C9.55957 0.691406 10.0078 1.05469 10.3359 1.54102C10.6641 2.02148 10.8281 2.53418 10.8281 3.0791C10.8281 3.65332 10.6201 4.16602 10.2041 4.61719C9.78809 5.0625 9.05566 5.41699 8.00684 5.68066ZM4.80762 5.44336C5.63965 5.44336 6.25195 5.34961 6.64453 5.16211C7.04297 4.97461 7.34766 4.71094 7.55859 4.37109C7.76953 4.03125 7.875 3.59766 7.875 3.07031C7.875 2.54297 7.76953 2.1123 7.55859 1.77832C7.35352 1.43848 7.05762 1.18066 6.6709 1.00488C6.28418 0.829102 5.66309 0.744141 4.80762 0.75V5.44336ZM4.80762 6.12891V9.95215L4.79883 10.3916C4.79883 10.708 4.87793 10.9482 5.03613 11.1123C5.2002 11.2705 5.44043 11.3496 5.75684 11.3496C6.22559 11.3496 6.65625 11.2471 7.04883 11.042C7.44727 10.8311 7.75195 10.5293 7.96289 10.1367C8.17383 9.73828 8.2793 9.2959 8.2793 8.80957C8.2793 8.25293 8.15039 7.75488 7.89258 7.31543C7.63477 6.87012 7.28027 6.55957 6.8291 6.38379C6.37793 6.20801 5.7041 6.12305 4.80762 6.12891Z"
                />
              </svg>
            </button>
            <button
              :class="{ 'is-active': isActive.italic() }"
              @click="commands.italic"
            >
              <svg
                class="cursor-pointer fill-current text-black hover:text-d_blue"
                width="24"
                height="12"
                viewBox="0 0 10 12"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  opacity="0.3"
                  d="M3.4873 0.407227L3.58398 0.0820312H9.40234L9.28809 0.407227C8.76074 0.407227 8.35645 0.524414 8.0752 0.758789C7.7998 0.993164 7.55664 1.48242 7.3457 2.22656L5.16602 9.85547C5.00781 10.3945 4.92871 10.7549 4.92871 10.9365C4.92871 11.1475 5.01074 11.3115 5.1748 11.4287C5.38574 11.5811 5.78418 11.6631 6.37012 11.6748L6.28223 12H0.367188L0.463867 11.6748C1.05566 11.6748 1.48926 11.5635 1.76465 11.3408C2.04004 11.1123 2.28906 10.6172 2.51172 9.85547L4.70898 2.22656C4.84375 1.75781 4.91113 1.40332 4.91113 1.16309C4.91113 0.946289 4.8291 0.776367 4.66504 0.65332C4.50098 0.530273 4.1084 0.448242 3.4873 0.407227Z"
                />
              </svg>
            </button>
            <button>
              <twemoji-picker
                class="mt-20"
                :emoji-data="emojiDataAll"
                :emoji-groups="emojiGroups"
                :search-emojis-feat="true"
                :skins-selection="true"
                :picker-width="700"
                picker-placement="bottom"
                search-emoji-placeholder="Поиск..."
                search-emoji-not-found="Эмодзи не найдены"
                is-loading-label="Загрузка..."
                @emojiUnicodeAdded="selectEmoji"
              >
                <template #twemoji-picker-button>
                  <svg
                    class="cursor-pointer fill-current text-black hover:text-d_blue"
                    width="24"
                    height="16"
                    viewBox="0 0 16 16"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <g opacity="0.4">
                      <path
                        d="M8 0C3.58172 0 0 3.58172 0 8C0 12.4183 3.58172 16 8 16C12.4183 16 16 12.4183 16 8C16 3.58172 12.4183 0 8 0ZM8 15C4.134 15 1 11.866 1 8C1 4.134 4.134 1 8 1C11.866 1 15 4.134 15 8C15 11.866 11.866 15 8 15Z"
                      />
                      <path
                        d="M5.5 6.5C6.05228 6.5 6.5 6.05228 6.5 5.5C6.5 4.94772 6.05228 4.5 5.5 4.5C4.94772 4.5 4.5 4.94772 4.5 5.5C4.5 6.05228 4.94772 6.5 5.5 6.5Z"
                        fill="black"
                      />
                      <path
                        d="M10.5 6.5C11.0523 6.5 11.5 6.05228 11.5 5.5C11.5 4.94772 11.0523 4.5 10.5 4.5C9.94772 4.5 9.5 4.94772 9.5 5.5C9.5 6.05228 9.94772 6.5 10.5 6.5Z"
                      />
                      <path
                        d="M11.5 8C11.5 9.933 9.933 11.5 8 11.5C6.067 11.5 4.5 9.933 4.5 8H3.5C3.5 10.4853 5.51472 12.5 8 12.5C10.4853 12.5 12.5 10.4853 12.5 8H11.5Z"
                      />
                    </g>
                  </svg>
                </template>
              </twemoji-picker>
            </button>
          </div>
        </editor-menu-bar>
        <editor-content
          ref="text"
          class=" rounded-b-10 p-4"
          style="height: 50vh; overflow: auto"
          placeholder="Введите сообщениее..."
          :editor="message"
        />
      </div>
      <div class="flex flex-row justify-start items-center mt-10">
        <v-button class="mr-6" title="Сохранить" @click="sendMessage()" />
        <v-radio
          v-if="type"
          class="mr-2"
          :checked="list"
          title="Добавить списком"
          @change="list = !list"
        />
        <svg
          v-if="type"
          class="cursor-pointer fill-current text-cyan hover:text-yellow"
          style="margin-top: 0.25rem"
          width="9"
          height="17"
          viewBox="0 0 9 17"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M8.12846 14.1689C7.93286 14.0091 7.6626 13.9759 7.43512 14.0831C7.40085 14.0993 7.28973 14.1453 7.00004 14.2255C6.80772 14.2783 6.64159 14.3051 6.50602 14.3051C6.22965 14.3051 6.09976 14.2687 6.05501 14.2527C6.04322 14.2167 6.02401 14.134 6.02401 13.9777C6.02401 13.9253 6.03055 13.7664 6.09299 13.4225C6.13971 13.1555 6.19385 12.9139 6.25519 12.7008L7.05899 9.85501C7.15067 9.55222 7.21398 9.21778 7.24673 8.86194C7.27838 8.5299 7.29344 8.29435 7.29344 8.14219C7.29344 7.34844 7.00659 6.69004 6.44075 6.18488C5.89674 5.69937 5.14315 5.45312 4.20073 5.45312C3.7019 5.45312 3.17164 5.5411 2.62523 5.71465C2.12793 5.87205 1.59854 6.06481 1.05169 6.28748C0.857183 6.36651 0.712666 6.53417 0.662674 6.73806L0.44568 7.62263C0.387829 7.85796 0.464891 8.10596 0.645865 8.26728C0.826403 8.42839 1.0816 8.47664 1.30929 8.39281C1.46669 8.33452 1.6433 8.27623 1.83453 8.21991C1.99586 8.17232 2.1502 8.14809 2.29362 8.14809C2.52808 8.14809 2.64924 8.17494 2.70142 8.19131C2.71408 8.23192 2.73263 8.31858 2.73263 8.47642C2.73263 8.63774 2.71233 8.82003 2.67151 9.02065C2.62698 9.24485 2.57 9.48804 2.50123 9.75197L1.69067 12.6205C1.68827 12.629 1.68608 12.6375 1.6839 12.6462C1.60749 12.9658 1.55052 13.2597 1.5145 13.5206C1.47804 13.786 1.4597 14.0523 1.4597 14.3115C1.4597 15.0945 1.75441 15.7507 2.33619 16.2629C2.89352 16.7519 3.65497 16.9999 4.59935 16.9999C5.18223 16.9999 5.70747 16.92 6.16023 16.7624C6.56082 16.6233 7.09195 16.4233 7.73835 16.1679C7.93591 16.09 8.08349 15.9208 8.13413 15.7145L8.35026 14.8308C8.40985 14.5863 8.32384 14.3285 8.12846 14.1689ZM5.94302 8.74013C5.91813 9.00974 5.87185 9.25729 5.80221 9.48782L4.99601 12.3419C4.92266 12.5967 4.85761 12.8844 4.80369 13.1931C4.74365 13.5243 4.7144 13.781 4.7144 13.9779C4.7144 14.5627 4.8814 14.9948 5.21257 15.2641C5.35534 15.3792 5.52889 15.4656 5.73606 15.5237C5.7341 15.5244 5.73191 15.525 5.73017 15.5259C5.41559 15.6353 5.03487 15.6907 4.59892 15.6907C3.98177 15.6907 3.51089 15.5521 3.20046 15.2796C2.90619 15.0205 2.76909 14.7131 2.76909 14.3119C2.76909 14.1117 2.7835 13.9054 2.81166 13.6996C2.84135 13.485 2.88938 13.2376 2.95443 12.9639L3.76478 10.0962C3.84358 9.79476 3.90624 9.5269 3.95557 9.27956C4.01321 8.99576 4.04246 8.72572 4.04246 8.47686C4.04246 7.92586 3.89794 7.50846 3.61196 7.23558C3.47509 7.10547 3.30241 7.00789 3.09109 6.94196C3.48404 6.82342 3.85712 6.76317 4.20095 6.76317C4.81176 6.76317 5.27217 6.89742 5.56862 7.16223C5.85198 7.41502 5.98384 7.72633 5.98384 8.14219C5.98384 8.20398 5.9786 8.36312 5.94302 8.74013Z"
          />
          <path
            d="M5.99557 4.91556C6.69436 4.91556 7.30212 4.67913 7.80029 4.21436C8.30653 3.74479 8.57439 3.13856 8.57439 2.46182C8.57439 1.77852 8.31505 1.18845 7.80334 0.707524C7.30321 0.23817 6.69523 0 5.99578 0C5.2959 0 4.68596 0.237297 4.18255 0.705778C3.67347 1.18059 3.4043 1.78769 3.4043 2.4616C3.4043 3.13878 3.67456 3.74545 4.18517 4.21545C4.68836 4.68001 5.29765 4.91556 5.99557 4.91556ZM5.0752 1.66435C5.33498 1.42269 5.62729 1.30983 5.99557 1.30983C6.36101 1.30983 6.65048 1.42182 6.90655 1.66217C7.15061 1.89161 7.26457 2.14571 7.26457 2.4616C7.26457 2.77748 7.15171 3.02941 6.90808 3.25535C6.65201 3.4944 6.3621 3.60551 5.99557 3.60551C5.62707 3.60551 5.33411 3.4933 5.07258 3.2523C4.82786 3.02701 4.71368 2.77574 4.71368 2.4616C4.71368 2.14746 4.82895 1.89401 5.0752 1.66435Z"
          />
        </svg>
      </div>
    </div>
  </div>
</template>

<script>
import EmojiAllData from "@kevinfaguiar/vue-twemoji-picker/emoji-data/ru/emoji-all-groups.json"
import EmojiGroups from "@kevinfaguiar/vue-twemoji-picker/emoji-data/emoji-groups.json"

import { Editor, EditorContent, EditorMenuBar } from "tiptap"
import {
  Blockquote,
  CodeBlock,
  HardBreak,
  Heading,
  OrderedList,
  BulletList,
  ListItem,
  TodoItem,
  TodoList,
  Bold,
  Code,
  Italic,
  Link,
  Strike,
  Underline,
  History
} from "tiptap-extensions"
import VButton from "./vButton.vue"
import VRadio from "./vRadio.vue"
export default {
  components: {
    EditorContent,
    EditorMenuBar,
    VButton,
    VRadio
  },
  props: {
    type: {
      type: Boolean,
      default: true
    },
    value: {
      type: String,
      default: `
          <em>Yay Headlines!</em>
          <p>All these <strong>cool tags</strong> are working now.</p>
        `
    }
  },
  data() {
    return {
      message: null,
      list: false
    }
  },
  computed: {
    emojiDataAll() {
      return EmojiAllData
    },
    emojiGroups() {
      return EmojiGroups
    }
  },
  mounted() {
    this.message = new Editor({
      extensions: [
        new Blockquote(),
        new CodeBlock(),
        new HardBreak(),
        new Heading({ levels: [1, 2, 3] }),
        new BulletList(),
        new OrderedList(),
        new ListItem(),
        new TodoItem(),
        new TodoList(),
        new Bold(),
        new Code(),
        new Italic(),
        new Link(),
        new Strike(),
        new Underline(),
        new History()
      ],
      content: this.value
    })
  },
  beforeDestroy() {
    this.message.destroy()
  },
  methods: {
    sendMessage() {
      let result = "",
        arr = []
      if (this.list) {
        for (const x of this.message.getJSON().content) {
          if (x.content) {
            for (const y of x.content) {
              if (y.marks && y.marks.length) {
                let mask = ""
                for (const mark of y.marks)
                  switch (mark.type) {
                    case "bold":
                      mask += "<strong>"
                      break
                    case "italic":
                      mask += "<em>"
                      break
                  }
                mask += y.text
                for (let i = y.marks.length - 1; i >= 0; i--)
                  switch (y.marks[i].type) {
                    case "bold":
                      mask += "</strong>"
                      break
                    case "italic":
                      mask += "</em>"
                      break
                  }
                result += mask
              } else {
                result += y.text
              }
            }
            arr.push("<p>" + result + "</p>")
            result = ""
          }
        }
      } else arr.push(this.message.getHTML())
      this.$emit("close", arr)
    },
    selectEmoji(emoji) {
      const transaction = this.message.state.tr.insertText(emoji)
      this.message.view.dispatch(transaction)
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
textarea {
  max-height: 50vh;
}
</style>
