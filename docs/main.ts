import "docsify/lib/docsify.js"
// import "docsify/themes/dark.css"
import "docsify-copy-code/dist/docsify-copy-code.min.js"

import "docsify-themeable/dist/js/docsify-themeable.min.js"
// import "docsify-themeable/dist/css/theme-simple-dark.css"

import "docsify-darklight-theme/dist/style.min.css"
import "docsify-darklight-theme/dist/index.min.js"


interface MsgData {
    type: string,
    [key: string]: any
}


const toggleTheme = () => {
    const themeBtnEl = document.getElementById('docsify-darklight-theme')
    console.log("themeBtnEl", themeBtnEl)
    if (themeBtnEl) {
        themeBtnEl.click()
    } else {
        setTimeout(toggleTheme, 10)
    }
}

window.addEventListener('message', (event: MessageEvent<MsgData>) => {
    if (event.data.type == "THEME") {
        const htmlEl = document.getElementsByTagName("html")
        if (htmlEl.length == 1) {
            const isDark = htmlEl[0].style.colorScheme == 'dark'
            if (isDark != event.data.isDark) {
                toggleTheme()
            }
        }
    }
});

