<template>
    <img width="960" height="1080" :src="videoSrc" />
</template>

<script>
export default {
    name: 'Video',
    data: function () {
        return {
            videoSrc: '/dist/guide.png',
        }
    },
    methods: {
        setVideoSrc(value) {
            this.videoSrc = value
        },
    },
    mounted: function () {
        window.eel.expose(this.setVideoSrc, 'setVideoSrc')
    },
}
</script>
