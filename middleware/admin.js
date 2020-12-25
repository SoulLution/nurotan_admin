import axios from "axios"
export default function({ store, redirect }) {
  let show = false,
    user = localStorage.getItem("auth")
      ? JSON.parse(localStorage.getItem("auth"))
      : false
  if (show) console.log(store)

  if (!user) {
    return redirect("/sign")
  } else {
    axios
      .get(
        `http://185.22.64.75:3143/n_users/1111111111/${user.email}/${user.password}/`
      )
      .then(res => {
        if (!res.data.length) {
          return redirect("/sign")
        }
        if (res.data[0].is_admin != 1) return redirect("/dialogs")
      })
  }
}
