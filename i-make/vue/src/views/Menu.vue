<template >
    <div id="container">
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
    height: 1080px;
    margin: auto;
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
    margin: auto 5px;
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
