<template>
    <p id="fps">FPS: {{fps}}</p>
    <img id="python_video" width="860" height="1080" v-bind:src="videosrc">
</template>

<script>
export default {
    name: 'Video',
    data: function () {
        return {
            videosrc: "./image/noimage.png",
            fps: 0
        }
    },
    methods: {
        setFPS(fps) {
            this.fps=fps;
        },
        setBase64Image(base64image) {
            this.videosrc=base64image;
        }
    },
    mounted: function () {
        window.eel.expose(this.setFPS, 'setFPS')
        window.eel.expose(this.setBase64Image, 'setBase64Image')
    }
}
</script>
