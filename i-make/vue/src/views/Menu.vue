<template >
    <div id="container">
        <h2 class="title">iMake!</h2>
        <button class="settings" v-on:click="goToSettings">Settings</button>
        <Video class="video" />
        <div class="mode-list">
            <div v-for="(mode, index) in modes" :key="index" class="mode">
                <label class="circle-number">{{index+1}} </label>
                <img :src="mode.icon_path" v-shortkey.once="[(index+1)]" @shortkey="setMode(mode.name)"
                    @click="setMode(mode.name)" role="button" class="mode-button">
            </div>
        </div>
    </div>
</template>

<script>
import Video from '@/components/shared/Video.vue'

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
            this.$router.push("/mode/"+name);
        },
        async getModes() {
            this.modes=await window.eel.get_mode_choices()();
        },
        goToSettings() {
            this.$router.push("/settings");
        }
    },
    created: function () {
        this.getModes();
    },
    components: { Video }
}
</script>

<style scoped>
#container {
    display: grid;
    grid-template-columns: 960px 780px 180px;
    grid-template-rows: 180px 900px;
    grid-template-areas:
        "video title settings"
        "video select-mode select-mode";
}

.title {
    grid-area: title;
    font-size: 120px;
    line-height: 180px;
    margin: 0;
    padding: 0;
}

.settings {
    grid-area: settings;
    font-size: 20px;
    margin: 0;
    padding: 0;
}

.video {
    grid-area: video;
}

.mode-list {
    grid-area: select-mode;
    display: flex;
    flex-direction: column;
}

.mode {
    display: flex;
    flex-direction: row;
    align-items: center;
    margin: 10px;
}

.circle-number {
    display: block;
    width: 100px;
    height: 100px;
    margin: auto 20px;
    font-size: 80px;
    background-color: #aadfec;
    border-radius: 50%;
    text-align: center;
    box-sizing: border-box;
}

.mode-button {
    width: 800px;
    height: auto;
}
</style>
