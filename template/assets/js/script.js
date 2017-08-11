
(function () {
    window.document.body.classList.add('ready')
})()

let light = 'ihui-light'
let dark = 'ihui-dark'

let theme = window.localStorage.getItem('theme')
window.document.body.classList.add(theme || light)

function toggleTheme() {
    window.document.body.classList.toggle(dark)
    window.document.body.classList.toggle(light)
    window.localStorage.setItem('theme', window.document.body.classList.contains(light) ? light : dark)
}