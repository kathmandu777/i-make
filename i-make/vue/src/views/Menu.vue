<template >
    <div id="container">
        <Video class="video" />
        <div class="mode-list">
            <div v-for="(mode, i) in modes" :key="i">
                <img :src="mode.icon_path" @click="setMode(mode.name)" role="button" class="mode-button">
            </div>
        </div>
    </div>
</template>

<script>
import Video from '@/components/Video.vue'

export default {
    name: "Menu",
    data: function () {
        return {
            modes: []
        };
    },
    methods: {
        setMode(name) {
            window.eel.set_mode(name)();
            this.$router.push("/mode");
        },
        async getModes() {
            this.modes=await window.eel.get_mode_choices()();
        }
    },
    created: function () {
        this.getModes();
    },
    components: { Video }
}
</script>

<style>
#container {
    display: grid;
    grid-template-columns: 960px 960px;
    grid-template-rows: 1080px;
    grid-template-areas:
        "video select-mode";
}

.video {
    grid-area: video;
}

#mode-list {
    grid-area: select-mode;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 1080px;
    margin: 0;
}

.mode-button {
    width: 960px;
    height: auto;
}
</style>
