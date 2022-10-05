<template>
    <div class="half-HD">
        <h2 class="title">iMake!</h2>
        <img
            class="settings"
            v-on:click="goToSettings()"
            v-shortkey.once="['*']"
            @shortkey="goToSettings()"
            src="/dist/setting.png"
            width="180"
            height="180"
        />
        <div class="mode-list">
            <div v-for="(mode, index) in modes" :key="index" class="mode">
                <!-- <label class="circle-number">{{index+1}} </label> -->
                <img
                    :src="mode.menu_image_path"
                    v-shortkey.once="[index + 1]"
                    @shortkey="setMode(mode)"
                    @click="setMode(mode)"
                    role="button"
                    class="mode-button"
                />
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Menu',
    data: function () {
        return {
            modes: [],
        }
    },
    methods: {
        setMode(mode) {
            const name = mode.name
            window.eel.set_mode(name)()
            this.$emit(
                'update-component',
                name.slice(0, 1).toUpperCase() + name.slice(1).toLowerCase(),
                {
                    modeIconPath: mode.icon_path,
                }
            )
        },
        async getModes() {
            this.modes = await window.eel.get_mode_choices()()
        },
        goToSettings() {
            this.$emit('update-component', 'SkinColor')
        },
    },
    created: function () {
        this.getModes()
    },
}
</script>

<style scoped>
.half-HD {
    display: grid;
    grid-template-columns: 780px 180px;
    grid-template-rows: 180px 900px;
    grid-template-areas:
        'title settings'
        'select-mode select-mode';
}

.title {
    grid-area: title;
    font-size: 120px;
    line-height: 180px;
    margin: 0 20px;
    padding: 0;
}

.settings {
    grid-area: settings;
    font-size: 20px;
    margin: 0;
    padding: 0;
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

/* .circle-number {
    display: block;
    width: 100px;
    height: 100px;
    margin: auto 20px;
    font-size: 80px;
    background-color: #aadfec;
    border-radius: 50%;
    text-align: center;
    box-sizing: border-box;
} */

.mode-button {
    width: calc(100% - 120px);
    height: auto;
    margin: 0 60px;
}
</style>
