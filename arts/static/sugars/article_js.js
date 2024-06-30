if (typeof window.host_type === 'undefined') {
    window.host_type = 0

    window.video_template = `<div><video loading="lazy" controls onclick="show('{{src}}')"><source src='{{src}}' type='video/mp4'></video></div>`
    window.img_template = `<div><img loading="lazy" src='{{src}}' onclick="show('{{src}}')"></div>`
    window.big_video_template = `<video loading="lazy" controls onclick="show('{{src}}')"><source src='{{src}}' type='video/mp4'></video>`
    window.big_img_template = `<img loading="lazy" src='{{src}}' onclick="show('{{src}}')">`
    window.go_home = `\n\n<button class="go_home" onclick="show('https://lcctoor.github.io/arts')">[作者主页]</button> 👈`

    window.show = (src) => {event.preventDefault(); window.open(src, '_blank')}
    window.bare_dir = decodeURIComponent(new URL('.', 'https://lcctoor.github.io/arts_static1/arts/' + decodeURIComponent(window.location.href.replace('/arts/arts/', '/arts/')).split('/arts/').at(-1)).href)

    window.creat_media = (media) => {
        if (media) {
            let content = []
            let video_suffixes = ['mp4']
            let img_suffixes = ['jpg', 'png', 'jpeg']
            for (let src of media) {
                let suffix = src.match(/\.([^.]+)$/)
                if ((host_type !== 3) && src.startsWith('oas1_')) {src = bare_dir + src}
                if (suffix) {
                    if (video_suffixes.includes(suffix[1]))
                        {content.push(video_template.replace(/{{src}}/g, src))}
                    else if (img_suffixes.includes(suffix[1]))
                        {content.push(img_template.replace(/{{src}}/g, src))}
                }
            }
            let ch_15 = document.createElement('div')
            ch_15.classList.add('ch_15')
            ch_15.innerHTML += content.join('\n')
            document.body.getElementsByTagName('pre')[0].insertBefore(ch_15, document.currentScript)
        }
    }
    
    window.creat_big_media = (media) => {
        if (media) {
            let content = []
            let video_suffixes = ['mp4']
            let img_suffixes = ['jpg', 'png', 'jpeg']
            for (let src of media) {
                let suffix = src.match(/\.([^.]+)$/)
                if ((host_type !== 3) && src.startsWith('oas1_')) {src = bare_dir + src}
                if (suffix) {
                    if (video_suffixes.includes(suffix[1]))
                        {content.push(big_video_template.replace(/{{src}}/g, src))}
                    else if (img_suffixes.includes(suffix[1]))
                        {content.push(big_img_template.replace(/{{src}}/g, src))}
                }
            }
            let ch_16 = document.createElement('div')
            ch_16.classList.add('ch_16')
            ch_16.innerHTML += content.join('\n')
            document.body.getElementsByTagName('pre')[0].insertBefore(ch_16, document.currentScript)
        }
    }
    
    window.clean_text = (text) => text.replace(/\s+$/, '').replace(/[\s\\]*\\[\s\\]*/g, '')
    
    window.render = (author=true) => {
        document.title = decodeURIComponent(document.URL).match(/\/(\d*\s*-\s*)?([^/\\]+)\/?$/)[2]
        let pre = document.body.getElementsByTagName('pre')[0]
        if (author) {
            pre.innerHTML = clean_text(pre.innerHTML) + go_home
        }
        else {
            pre.innerHTML = clean_text(pre.innerHTML)
        }
        pre.addEventListener('dblclick', () => {window.open(document.URL, '_blank')})
    }
}

if (document.currentScript.src.includes('offline_files')) {window.host_type = 3}
else if (document.URL.startsWith('file')) {window.host_type = Math.max(window.host_type, 2)}
else {window.host_type = Math.max(window.host_type, 1)}